"""Execute the frozen four-stream ODSA simulation protocol."""
from __future__ import annotations
import argparse,csv,hashlib,json,math,shutil,time
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Any,Iterable
import numpy as np
import yaml
ROOT=Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL=ROOT/'simulations'/'manuscript_protocol.yml'
DEFAULT_FREEZE=ROOT/'simulations'/'manuscript_protocol.freeze.json'
DEFAULT_OUTPUT=ROOT/'outputs_v3'/'full_simulation'
COLUMN_NAMES=['cell_id','stream_index','replication_in_stream','scenario_index','sample_size_per_group','allocation_index','misclassification_index','missingness_index','true_total_n','observed_total_n','missing_share','population_active_level','population_broad_level','population_active_cramers_v','population_broad_cramers_v','sampled_true_active_level','sampled_true_broad_level','sampled_true_active_cramers_v','sampled_true_broad_cramers_v','observed_active_level','observed_broad_level','observed_active_cramers_v','observed_broad_cramers_v','delta_level_broad_minus_active','delta_cramers_v_broad_minus_active','cross_definition_pairwise_disagreement_share','cross_definition_strict_reversal_share','added_state_share_of_right_positive','project_share_of_broad_positive','active_level_sampling_error','broad_level_sampling_error','active_level_observation_error','broad_level_observation_error','active_level_total_error','broad_level_total_error','active_association_sampling_error','broad_association_sampling_error','active_association_observation_error','broad_association_observation_error','active_association_total_error','broad_association_total_error','active_order_error_share','broad_order_error_share','max_absolute_group_rate_change','mean_absolute_group_rate_change','undefined_active_association','undefined_broad_association','any_cross_definition_strict_reversal','broad_association_stronger']
COL={name:i for i,name in enumerate(COLUMN_NAMES)}
CONTINUOUS_SUMMARY_METRICS=['delta_level_broad_minus_active','delta_cramers_v_broad_minus_active','cross_definition_pairwise_disagreement_share','cross_definition_strict_reversal_share','added_state_share_of_right_positive','project_share_of_broad_positive','active_level_sampling_error','broad_level_sampling_error','active_level_observation_error','broad_level_observation_error','active_level_total_error','broad_level_total_error','active_association_sampling_error','broad_association_sampling_error','active_association_observation_error','broad_association_observation_error','active_association_total_error','broad_association_total_error','active_order_error_share','broad_order_error_share','max_absolute_group_rate_change','mean_absolute_group_rate_change','missing_share']
EVENT_METRICS={'broad_association_stronger':'broad_association_stronger','any_cross_definition_order_disagreement':'cross_definition_pairwise_disagreement_share','any_cross_definition_strict_reversal':'any_cross_definition_strict_reversal'}
CONVERGENCE_METRICS=['delta_cramers_v_broad_minus_active','cross_definition_pairwise_disagreement_share','any_cross_definition_strict_reversal','active_association_total_error','broad_association_total_error']

def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
    return h.hexdigest()

def write_json(path:Path,payload:Any)->None:
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(payload,indent=2,sort_keys=True,allow_nan=False)+'\n',encoding='utf-8')

def load_and_verify_protocol(protocol_path:Path,freeze_path:Path)->dict[str,Any]:
    actual=sha256_file(protocol_path); freeze=json.loads(freeze_path.read_text()); expected=str(freeze['protocol_sha256'])
    if actual!=expected:raise RuntimeError(f'frozen protocol hash mismatch: expected {expected}, obtained {actual}')
    design=yaml.safe_load(protocol_path.read_text()); execution=design['execution']
    if int(execution['full_cell_count'])*int(execution['full_replications_per_cell'])!=int(execution['full_replicate_row_count']):raise RuntimeError('full replicate-row count is internally inconsistent')
    if int(execution['full_stream_count'])*int(execution['full_replications_per_stream'])!=int(execution['full_replications_per_cell']):raise RuntimeError('stream replication counts do not sum to pooled count')
    if int(design['seed_stream_policy']['root_entropy'])!=int(design['root_seed']):raise RuntimeError('root seed and SeedSequence entropy differ')
    return design
@dataclass(frozen=True)
class Cell:
    cell_id:int; scenario:str; sample_size_per_group:int; allocation_profile:str; misclassification_profile:str; missingness_profile:str; scenario_index:int; allocation_index:int; misclassification_index:int; missingness_index:int

def full_cells(design:dict[str,Any])->list[Cell]:
    e=design['execution']; scenarios=list(e['full_scenarios']); ns=[int(x) for x in e['full_sample_sizes_per_group']]; alloc=list(e['full_allocation_profiles']); mis=list(e['full_misclassification_profiles']); miss=list(e['full_missingness_profiles']); cells=[]
    for cid,(s,n,a,m,x) in enumerate(product(scenarios,ns,alloc,mis,miss)):
        cells.append(Cell(cid,s,n,a,m,x,scenarios.index(s),alloc.index(a),mis.index(m),miss.index(x)))
    if len(cells)!=int(e['full_cell_count']):raise RuntimeError('wrong cell count')
    return cells

def rounded_group_sizes(base:int,multipliers:Iterable[float])->np.ndarray:
    sizes=np.floor(base*np.asarray(list(multipliers),float)+0.5).astype(np.int64)
    if (sizes<=1).any():raise RuntimeError('every group size must exceed one')
    return sizes

def batch_cramers_v(positive:np.ndarray,total:np.ndarray)->np.ndarray:
    positive=np.asarray(positive,float); total=np.asarray(total,float)
    if positive.shape!=total.shape or positive.ndim!=2:raise ValueError('arrays must match')
    negative=total-positive; grand=total.sum(1); pm=positive.sum(1); nm=negative.sum(1); result=np.full(positive.shape[0],np.nan)
    valid=(grand>0)&(pm>0)&(nm>0)&(total>0).all(1)
    if valid.any():
        tv=total[valid]; pv=positive[valid]; nv=negative[valid]; gv=grand[valid]; p=pm[valid]; n=nm[valid]
        ep=tv*(p/gv)[:,None]; en=tv*(n/gv)[:,None]; chi=np.sum((pv-ep)**2/ep+(nv-en)**2/en,axis=1); result[valid]=np.sqrt(chi/gv)
    return result

def population_cramers_v(weights:np.ndarray,rates:np.ndarray)->float:
    joint=np.column_stack((weights*rates,weights*(1-rates))); expected=joint.sum(1,keepdims=True)@joint.sum(0,keepdims=True)
    if (expected<=0).any():return float('nan')
    return float(np.sqrt(np.sum((joint-expected)**2/expected)))

def pairwise_order_metrics(left:np.ndarray,right:np.ndarray)->tuple[np.ndarray,np.ndarray]:
    pairs=left.shape[1]*(left.shape[1]-1)//2; d=np.zeros(left.shape[0]); r=np.zeros(left.shape[0])
    for i in range(left.shape[1]-1):
        for j in range(i+1,left.shape[1]):
            ls=np.sign(left[:,i]-left[:,j]); rs=np.sign(right[:,i]-right[:,j]); d+=ls!=rs; r+=(ls*rs)<0
    return d/pairs,r/pairs

def population_order_metrics(pop:np.ndarray,obs:np.ndarray,tol:float)->np.ndarray:
    pairs=obs.shape[1]*(obs.shape[1]-1)//2; d=np.zeros(obs.shape[0])
    for i in range(obs.shape[1]-1):
        for j in range(i+1,obs.shape[1]):
            x=pop[i]-pop[j]; ps=0.0 if abs(x)<=tol else (1.0 if x>0 else -1.0); d+=np.sign(obs[:,i]-obs[:,j])!=ps
    return d/pairs

def apply_observation_process(true:np.ndarray,missing:np.ndarray,matrix:np.ndarray,rng:np.random.Generator)->tuple[np.ndarray,np.ndarray]:
    reps,groups,states=true.shape; retained=np.empty_like(true)
    for s in range(states):retained[:,:,s]=rng.binomial(true[:,:,s],1-float(missing[s]))
    observed=np.zeros_like(retained)
    for source in range(states):
        n=retained[:,:,source]; probs=matrix[source]; remaining=n.copy(); prem=1.0
        for target in range(states-1):
            cp=0.0 if prem<=0 else min(1.0,max(0.0,float(probs[target]/prem))); draw=rng.binomial(remaining,cp); observed[:,:,target]+=draw; remaining-=draw; prem-=float(probs[target])
        observed[:,:,states-1]+=remaining
    return observed,true.sum((1,2))-observed.sum((1,2))

def cell_population_registry(design:dict[str,Any],cells:list[Cell])->list[dict[str,Any]]:
    groups=list(design['groups']); states=list(design['states']); ai=states.index('active_use'); pi=states.index('project_stage'); rows=[]
    for c in cells:
        sizes=rounded_group_sizes(c.sample_size_per_group,design['allocation_profiles'][c.allocation_profile]); w=sizes/sizes.sum(); p=np.asarray([design['scenarios'][c.scenario]['probabilities'][g] for g in groups],float); ar=p[:,ai]; br=p[:,ai]+p[:,pi]; av=population_cramers_v(w,ar); bv=population_cramers_v(w,br)
        rows.append({'cell_id':c.cell_id,'scenario':c.scenario,'sample_size_per_group':c.sample_size_per_group,'allocation_profile':c.allocation_profile,'misclassification_profile':c.misclassification_profile,'missingness_profile':c.missingness_profile,'small_n':int(sizes[0]),'medium_n':int(sizes[1]),'large_n':int(sizes[2]),'population_active_level':float(np.dot(w,ar)),'population_broad_level':float(np.dot(w,br)),'population_active_cramers_v':av,'population_broad_cramers_v':bv,'population_delta_cramers_v':bv-av,'small_active_rate':float(ar[0]),'medium_active_rate':float(ar[1]),'large_active_rate':float(ar[2]),'small_broad_rate':float(br[0]),'medium_broad_rate':float(br[1]),'large_broad_rate':float(br[2])})
    return rows

def simulate_cell(design:dict[str,Any],cell:Cell,stream_index:int,reps:int,seed:np.random.SeedSequence)->np.ndarray:
    groups=list(design['groups']); states=list(design['states']); ai=states.index('active_use'); pi=states.index('project_stage'); sizes=rounded_group_sizes(cell.sample_size_per_group,design['allocation_profiles'][cell.allocation_profile]); total_n=int(sizes.sum()); w=sizes/total_n; probs=np.asarray([design['scenarios'][cell.scenario]['probabilities'][g] for g in groups],float); par=probs[:,ai]; pbr=probs[:,ai]+probs[:,pi]; pal=float(np.dot(w,par)); pbl=float(np.dot(w,pbr)); pav=population_cramers_v(w,par); pbv=population_cramers_v(w,pbr); rng=np.random.default_rng(seed)
    true=np.empty((reps,len(groups),len(states)),np.int64)
    for gi,n in enumerate(sizes):true[:,gi,:]=rng.multinomial(int(n),probs[gi],size=reps)
    missing=np.asarray(design['missingness_profiles'][cell.missingness_profile]['state_probabilities'],float); mis=np.asarray(design['misclassification_profiles'][cell.misclassification_profile]['matrix'],float); obs,missing_total=apply_observation_process(true,missing,mis,rng)
    tt=true.sum(2); ot=obs.sum(2); otn=ot.sum(1); tap=true[:,:,ai]; tbp=true[:,:,ai]+true[:,:,pi]; oap=obs[:,:,ai]; opp=obs[:,:,pi]; obp=oap+opp; tar=tap/tt; tbr=tbp/tt; oar=np.divide(oap,ot,out=np.full_like(oap,np.nan,dtype=float),where=ot>0); obr=np.divide(obp,ot,out=np.full_like(obp,np.nan,dtype=float),where=ot>0); tal=tap.sum(1)/total_n; tbl=tbp.sum(1)/total_n; oal=np.divide(oap.sum(1),otn,out=np.full(reps,np.nan),where=otn>0); obl=np.divide(obp.sum(1),otn,out=np.full(reps,np.nan),where=otn>0); tav=batch_cramers_v(tap,tt); tbv=batch_cramers_v(tbp,tt); oav=batch_cramers_v(oap,ot); obv=batch_cramers_v(obp,ot); disagree,strict=pairwise_order_metrics(oar,obr); tol=float(design['order_policy']['population_tie_tolerance']); aoe=population_order_metrics(par,oar,tol); boe=population_order_metrics(pbr,obr,tol); broad_total=obp.sum(1); project_total=opp.sum(1); project=np.divide(project_total,broad_total,out=np.full(reps,np.nan),where=broad_total>0); changes=obr-oar; maxchg=np.nanmax(np.abs(changes),1); meanchg=np.nanmean(np.abs(changes),1)
    x=np.empty((reps,len(COLUMN_NAMES)),np.float64); x[:,COL['cell_id']]=cell.cell_id; x[:,COL['stream_index']]=stream_index; x[:,COL['replication_in_stream']]=np.arange(reps); x[:,COL['scenario_index']]=cell.scenario_index; x[:,COL['sample_size_per_group']]=cell.sample_size_per_group; x[:,COL['allocation_index']]=cell.allocation_index; x[:,COL['misclassification_index']]=cell.misclassification_index; x[:,COL['missingness_index']]=cell.missingness_index; x[:,COL['true_total_n']]=total_n; x[:,COL['observed_total_n']]=otn; x[:,COL['missing_share']]=missing_total/total_n; x[:,COL['population_active_level']]=pal; x[:,COL['population_broad_level']]=pbl; x[:,COL['population_active_cramers_v']]=pav; x[:,COL['population_broad_cramers_v']]=pbv; x[:,COL['sampled_true_active_level']]=tal; x[:,COL['sampled_true_broad_level']]=tbl; x[:,COL['sampled_true_active_cramers_v']]=tav; x[:,COL['sampled_true_broad_cramers_v']]=tbv; x[:,COL['observed_active_level']]=oal; x[:,COL['observed_broad_level']]=obl; x[:,COL['observed_active_cramers_v']]=oav; x[:,COL['observed_broad_cramers_v']]=obv; x[:,COL['delta_level_broad_minus_active']]=obl-oal; x[:,COL['delta_cramers_v_broad_minus_active']]=obv-oav; x[:,COL['cross_definition_pairwise_disagreement_share']]=disagree; x[:,COL['cross_definition_strict_reversal_share']]=strict; x[:,COL['added_state_share_of_right_positive']]=project; x[:,COL['project_share_of_broad_positive']]=project; x[:,COL['active_level_sampling_error']]=tal-pal; x[:,COL['broad_level_sampling_error']]=tbl-pbl; x[:,COL['active_level_observation_error']]=oal-tal; x[:,COL['broad_level_observation_error']]=obl-tbl; x[:,COL['active_level_total_error']]=oal-pal; x[:,COL['broad_level_total_error']]=obl-pbl; x[:,COL['active_association_sampling_error']]=tav-pav; x[:,COL['broad_association_sampling_error']]=tbv-pbv; x[:,COL['active_association_observation_error']]=oav-tav; x[:,COL['broad_association_observation_error']]=obv-tbv; x[:,COL['active_association_total_error']]=oav-pav; x[:,COL['broad_association_total_error']]=obv-pbv; x[:,COL['active_order_error_share']]=aoe; x[:,COL['broad_order_error_share']]=boe; x[:,COL['max_absolute_group_rate_change']]=maxchg; x[:,COL['mean_absolute_group_rate_change']]=meanchg; x[:,COL['undefined_active_association']]=~np.isfinite(oav); x[:,COL['undefined_broad_association']]=~np.isfinite(obv); x[:,COL['any_cross_definition_strict_reversal']]=strict>0; x[:,COL['broad_association_stronger']]=obv>oav
    return x

def write_rows_csv(path:Path,rows:list[dict[str,Any]],fieldnames:list[str]|None=None)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:raise ValueError('empty CSV')
    if fieldnames is None:fieldnames=list(rows[0])
    with path.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fieldnames); w.writeheader(); w.writerows(rows)

def summarise_cell(matrix:np.ndarray,registry:dict[str,Any])->dict[str,Any]:
    row=dict(registry); row['replications']=int(matrix.shape[0]); row['undefined_active_association_fraction']=float(np.mean(matrix[:,COL['undefined_active_association']])); row['undefined_broad_association_fraction']=float(np.mean(matrix[:,COL['undefined_broad_association']])); row['undefined_association_fraction']=float(np.mean(np.maximum(matrix[:,COL['undefined_active_association']],matrix[:,COL['undefined_broad_association']])) )
    for metric in CONTINUOUS_SUMMARY_METRICS:
        values=matrix[:,COL[metric]]; finite=values[np.isfinite(values)]; row[f'defined_{metric}']=int(finite.size); row[f'undefined_{metric}']=int(values.size-finite.size)
        if finite.size:
            sd=float(np.std(finite,ddof=1)) if finite.size>1 else 0.0; row[f'mean_{metric}']=float(np.mean(finite)); row[f'sd_{metric}']=sd; row[f'mean_mcse_{metric}']=sd/math.sqrt(finite.size) if finite.size>1 else 0.0; row[f'q05_{metric}']=float(np.quantile(finite,.05)); row[f'median_{metric}']=float(np.quantile(finite,.5)); row[f'q95_{metric}']=float(np.quantile(finite,.95))
        else:
            for s in ('mean','sd','mean_mcse','q05','median','q95'):row[f'{s}_{metric}']=''
    for out,source in EVENT_METRICS.items():
        src=matrix[:,COL[source]]; vals=(src>0).astype(float) if out=='any_cross_definition_order_disagreement' else src.astype(float); finite=vals[np.isfinite(vals)]
        if finite.size:
            p=float(np.mean(finite)); row[f'probability_{out}']=p; row[f'mcse_{out}']=math.sqrt(p*(1-p)/finite.size); row[f'defined_{out}']=int(finite.size)
        else:row[f'probability_{out}']=''; row[f'mcse_{out}']=''; row[f'defined_{out}']=0
    return row

def run_stream(design,cells,registry_rows,output,stream_index,stream_seed):
    reps=int(design['execution']['full_replications_per_stream']); d=output/f'stream_{stream_index:02d}'; d.mkdir(parents=True,exist_ok=True); path=d/'replicates.npy'; expected=len(cells)*reps; m=np.lib.format.open_memmap(path,mode='w+',dtype=np.float64,shape=(expected,len(COLUMN_NAMES))); seeds=stream_seed.spawn(len(cells)); summaries=[]; started=time.perf_counter()
    for c,r,s in zip(cells,registry_rows,seeds,strict=True):
        a=c.cell_id*reps; b=a+reps; cm=simulate_cell(design,c,stream_index,reps,s); m[a:b,:]=cm; summaries.append(summarise_cell(cm,r))
    m.flush(); del m; write_rows_csv(d/'cell_summary.csv',summaries); audit={'status':'PASS','role':'independent full-simulation seed stream','stream_index':stream_index,'spawn_key':list(stream_seed.spawn_key),'cell_count':len(cells),'replications_per_cell':reps,'replicate_row_count':expected,'column_count':len(COLUMN_NAMES),'matrix_filename':path.name,'matrix_size_bytes':path.stat().st_size,'matrix_sha256':sha256_file(path),'cell_summary_sha256':sha256_file(d/'cell_summary.csv'),'elapsed_seconds':time.perf_counter()-started,'manuscript_evidence':True}; write_json(d/'stream_audit.json',audit); return audit

def pooled_cell_summaries(registry,matrices,reps):
    return [summarise_cell(np.concatenate([m[i*reps:(i+1)*reps,:] for m in matrices],axis=0),r) for i,r in enumerate(registry)]

def convergence_audit(registry,matrices,reps):
    rows=[]; maxz=0.; warnings=failures=0
    for cid,r in enumerate(registry):
        for metric in CONVERGENCE_METRICS:
            streams=[]
            for m in matrices:
                v=m[cid*reps:(cid+1)*reps,COL[metric]]; streams.append(v[np.isfinite(v)])
            pooled=np.concatenate(streams)
            if pooled.size<=1:continue
            pm=float(np.mean(pooled)); ps=float(np.std(pooled,ddof=1))
            for idx,v in enumerate(streams,1):
                sm=float(np.mean(v)) if v.size else float('nan')
                if not v.size:z=float('inf')
                elif ps==0:z=0. if sm==pm else float('inf')
                else:z=abs(sm-pm)/math.sqrt(max(ps*ps*(1/v.size-1/pooled.size),1e-30))
                status='FAIL' if z>5 else ('WARNING' if z>4 else 'PASS'); failures+=status=='FAIL'; warnings+=status=='WARNING'; maxz=max(maxz,z); rows.append({'cell_id':cid,'scenario':r['scenario'],'sample_size_per_group':r['sample_size_per_group'],'allocation_profile':r['allocation_profile'],'misclassification_profile':r['misclassification_profile'],'missingness_profile':r['missingness_profile'],'metric':metric,'stream_index':idx,'stream_mean':sm,'pooled_mean':pm,'standardised_stream_deviation':z,'status':status})
    return rows,{'status':'PASS' if failures==0 else 'FAIL','warning_threshold':4.0,'failure_threshold':5.0,'warning_count':warnings,'failure_count':failures,'maximum_standardised_stream_deviation':maxz,'comparison_count':len(rows)}

def run_full(protocol:Path,freeze:Path,output:Path,overwrite=False):
    if output.exists():
        if not overwrite:raise FileExistsError(output)
        shutil.rmtree(output)
    output.mkdir(parents=True); started=time.perf_counter(); design=load_and_verify_protocol(protocol,freeze); cells=full_cells(design); registry=cell_population_registry(design,cells); write_rows_csv(output/'cell_registry.csv',registry); shutil.copy2(protocol,output/'manuscript_protocol.yml'); shutil.copy2(freeze,output/'manuscript_protocol.freeze.json'); write_json(output/'replicate_matrix_columns.json',{'schema_version':'1.0','dtype':'float64','column_count':len(COLUMN_NAMES),'columns':[{'index':i,'name':n} for i,n in enumerate(COLUMN_NAMES)]})
    root=np.random.SeedSequence(int(design['seed_stream_policy']['root_entropy'])); count=int(design['execution']['full_stream_count']); sequences=root.spawn(count); audits=[run_stream(design,cells,registry,output,i,s) for i,s in enumerate(sequences,1)]; paths=[output/f'stream_{i:02d}'/'replicates.npy' for i in range(1,count+1)]; matrices=[np.load(p,mmap_mode='r') for p in paths]; reps=int(design['execution']['full_replications_per_stream']); pooled=pooled_cell_summaries(registry,matrices,reps); pooled_path=output/'pooled_cell_summary.csv'; write_rows_csv(pooled_path,pooled); conv,ca=convergence_audit(registry,matrices,reps); conv_path=output/'stream_convergence.csv'; write_rows_csv(conv_path,conv); write_json(output/'stream_convergence_audit.json',ca); uw=float(design['undefined_result_policy']['warning_fraction']); un=float(design['undefined_result_policy']['no_claim_fraction']); warning=sum(float(r['undefined_association_fraction'])>uw for r in pooled); noclaim=sum(float(r['undefined_association_fraction'])>un for r in pooled); nested=sum(int(np.sum(m[:,COL['observed_broad_level']]+1e-15<m[:,COL['observed_active_level']])) for m in matrices); max_mcse=max(float(r[f'mcse_{e}']) for r in pooled for e in EVENT_METRICS if r[f'mcse_{e}']!=''); status='PASS' if ca['status']=='PASS' and not noclaim and not nested else 'FAIL'; audit={'status':status,'role':'frozen manuscript-grade four-stream simulation','manuscript_evidence':True,'protocol_sha256':sha256_file(protocol),'freeze_record_sha256':sha256_file(freeze),'root_entropy':int(design['seed_stream_policy']['root_entropy']),'stream_count':count,'stream_spawn_keys':[list(s.spawn_key) for s in sequences],'cell_count':len(cells),'replications_per_stream_per_cell':reps,'replications_per_cell':reps*count,'replicate_row_count':len(cells)*reps*count,'column_count':len(COLUMN_NAMES),'stream_audits':audits,'pooled_cell_summary_sha256':sha256_file(pooled_path),'cell_registry_sha256':sha256_file(output/'cell_registry.csv'),'convergence_csv_sha256':sha256_file(conv_path),'convergence_audit_sha256':sha256_file(output/'stream_convergence_audit.json'),'maximum_standardised_stream_deviation':ca['maximum_standardised_stream_deviation'],'convergence_warning_count':ca['warning_count'],'convergence_failure_count':ca['failure_count'],'maximum_event_probability_mcse':max_mcse,'event_probability_mcse_target':float(design['monte_carlo_precision']['event_probability_worst_case_mcse_target']),'undefined_warning_cell_count':warning,'undefined_no_claim_cell_count':noclaim,'nested_level_violation_count':nested,'elapsed_seconds':time.perf_counter()-started}; write_json(output/'full_simulation_audit.json',audit)
    if status!='PASS':raise RuntimeError('full simulation audit failed')
    return audit

def main():
    p=argparse.ArgumentParser(); p.add_argument('--protocol',type=Path,default=DEFAULT_PROTOCOL); p.add_argument('--freeze',type=Path,default=DEFAULT_FREEZE); p.add_argument('--output',type=Path,default=DEFAULT_OUTPUT); p.add_argument('--overwrite',action='store_true'); a=p.parse_args(); print(json.dumps(run_full(a.protocol,a.freeze,a.output,a.overwrite),indent=2,sort_keys=True))
if __name__=='__main__':main()
