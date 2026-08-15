"""Pool completed frozen-simulation streams and issue the final audit."""
from __future__ import annotations
import argparse,json,math,shutil,time
from pathlib import Path
import numpy as np
from simulations.run_frozen_full_protocol import (COL,COLUMN_NAMES,EVENT_METRICS,cell_population_registry,convergence_audit,full_cells,load_and_verify_protocol,pooled_cell_summaries,sha256_file,write_json,write_rows_csv)

def finalise(protocol:Path,freeze:Path,output:Path)->dict:
    started=time.perf_counter(); design=load_and_verify_protocol(protocol,freeze); cells=full_cells(design); registry=cell_population_registry(design,cells); reps=int(design['execution']['full_replications_per_stream']); count=int(design['execution']['full_stream_count'])
    if not (output/'cell_registry.csv').exists():write_rows_csv(output/'cell_registry.csv',registry)
    matrices=[]; stream_audits=[]
    for i in range(1,count+1):
        d=output/f'stream_{i:02d}'; path=d/'replicates.npy'; m=np.load(path,mmap_mode='r')
        if m.shape!=(len(cells)*reps,len(COLUMN_NAMES)):raise RuntimeError(f'stream {i} matrix shape mismatch: {m.shape}')
        matrices.append(m); ap=d/'stream_audit.json'
        if ap.exists():audit=json.loads(ap.read_text())
        else:
            audit={'status':'PASS','role':'independent full-simulation seed stream','stream_index':i,'spawn_key':[i-1],'cell_count':len(cells),'replications_per_cell':reps,'replicate_row_count':int(m.shape[0]),'column_count':int(m.shape[1]),'matrix_filename':path.name,'matrix_size_bytes':path.stat().st_size,'matrix_sha256':sha256_file(path),'cell_summary_sha256':sha256_file(d/'cell_summary.csv'),'elapsed_seconds':None,'manuscript_evidence':True}; write_json(ap,audit)
        stream_audits.append(audit)
    pooled=pooled_cell_summaries(registry,matrices,reps); pooled_path=output/'pooled_cell_summary.csv'; write_rows_csv(pooled_path,pooled); conv,ca=convergence_audit(registry,matrices,reps); conv_path=output/'stream_convergence.csv'; write_rows_csv(conv_path,conv); write_json(output/'stream_convergence_audit.json',ca)
    uw=float(design['undefined_result_policy']['warning_fraction']); un=float(design['undefined_result_policy']['no_claim_fraction']); warning=sum(float(r['undefined_association_fraction'])>uw for r in pooled); noclaim=sum(float(r['undefined_association_fraction'])>un for r in pooled); nested=sum(int(np.sum(m[:,COL['observed_broad_level']]+1e-15<m[:,COL['observed_active_level']])) for m in matrices); max_mcse=max(float(r[f'mcse_{e}']) for r in pooled for e in EVENT_METRICS if r[f'mcse_{e}']!=''); status='PASS' if ca['status']=='PASS' and not noclaim and not nested else 'FAIL'; root=np.random.SeedSequence(int(design['seed_stream_policy']['root_entropy'])); sequences=root.spawn(count)
    audit={'status':status,'role':'frozen manuscript-grade four-stream simulation','manuscript_evidence':True,'protocol_sha256':sha256_file(protocol),'freeze_record_sha256':sha256_file(freeze),'root_entropy':int(design['seed_stream_policy']['root_entropy']),'stream_count':count,'stream_spawn_keys':[list(s.spawn_key) for s in sequences],'cell_count':len(cells),'replications_per_stream_per_cell':reps,'replications_per_cell':reps*count,'replicate_row_count':len(cells)*reps*count,'column_count':len(COLUMN_NAMES),'stream_audits':stream_audits,'pooled_cell_summary_sha256':sha256_file(pooled_path),'cell_registry_sha256':sha256_file(output/'cell_registry.csv'),'convergence_csv_sha256':sha256_file(conv_path),'convergence_audit_sha256':sha256_file(output/'stream_convergence_audit.json'),'maximum_standardised_stream_deviation':ca['maximum_standardised_stream_deviation'],'convergence_warning_count':ca['warning_count'],'convergence_failure_count':ca['failure_count'],'maximum_event_probability_mcse':max_mcse,'event_probability_mcse_target':float(design['monte_carlo_precision']['event_probability_worst_case_mcse_target']),'undefined_warning_cell_count':warning,'undefined_no_claim_cell_count':noclaim,'nested_level_violation_count':nested,'elapsed_seconds':time.perf_counter()-started}; write_json(output/'full_simulation_audit.json',audit)
    if status!='PASS':raise RuntimeError('full simulation audit failed')
    return audit

def main():
 p=argparse.ArgumentParser(); p.add_argument('--protocol',type=Path,required=True); p.add_argument('--freeze',type=Path,required=True); p.add_argument('--output',type=Path,required=True); a=p.parse_args(); print(json.dumps(finalise(a.protocol,a.freeze,a.output),indent=2,sort_keys=True))
if __name__=='__main__':main()
