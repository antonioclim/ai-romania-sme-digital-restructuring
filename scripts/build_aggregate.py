from __future__ import annotations
import hashlib, json, math, shutil, textwrap
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data"/"aggregate"; TABLES=ROOT/"outputs"/"tables"; FIGSRC=ROOT/"outputs"/"figure_source_data"; FIGURES=ROOT/"outputs"/"figures"; REPORTS=ROOT/"outputs"/"reports"
def sha256(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()
def pct(n,d): return round(100*n/d,1)
def wilson(n,d,z=1.959963984540054):
 p=n/d; den=1+z*z/d; c=(p+z*z/(2*d))/den; h=z*math.sqrt(p*(1-p)/d+z*z/(4*d*d))/den
 return round(100*(c-h),1),round(100*(c+h),1)
def write(df,p): p.parent.mkdir(parents=True,exist_ok=True); df.to_csv(p,index=False,encoding="utf-8",lineterminator="\n")
def pdisp(p): return "<0.001" if p<.001 else f"{p:.3f}"
def add_stats(df):
 rows=[]
 for _,r in df.iterrows():
  lo,hi=wilson(int(r.n),int(r.denominator)); rows.append({**r.to_dict(),"percent":pct(int(r.n),int(r.denominator)),"ci95_low":lo,"ci95_high":hi})
 return pd.DataFrame(rows)
def bar(frame,label,value,path,xlabel):
 local=frame.iloc[::-1].copy(); fig,ax=plt.subplots(figsize=(8.6,max(3.4,.55*len(local)+1.1))); y=np.arange(len(local)); ax.barh(y,local[value],height=.58)
 ax.set_yticks(y); ax.set_yticklabels(["\n".join(textwrap.wrap(str(v),34,break_long_words=False)) for v in local[label]],fontsize=9); ax.set_xlim(0,100); ax.set_xlabel(xlabel); ax.grid(axis="x",alpha=.25,linewidth=.6); ax.spines[["top","right","left"]].set_visible(False); ax.tick_params(axis="y",length=0)
 for i,(_,r) in enumerate(local.iterrows()): ax.text(min(float(r[value])+1.3,96),i,f"{r[value]:.1f}% ({int(r['n'])}/{int(r['denominator'])})",va="center",fontsize=8.3)
 fig.tight_layout(); fig.savefig(path,dpi=300,bbox_inches="tight",metadata={"Software":"Matplotlib"}); plt.close(fig)
def grouped(frame,path):
 order=["Micro (1–9)","Small (10–49)","Medium (50–249)"]; local=frame.set_index("employee_band").loc[order].reset_index(); x=np.arange(len(local)); w=.23; fig,ax=plt.subplots(figsize=(8.7,4.9))
 series=[("active_use_percent","Reported active AI use",-w),("project_engagement_percent","Project-stage category",0),("active_or_project_percent","Active use or project-stage engagement",w)]
 for col,label,off in series: ax.bar(x+off,local[col],w,label=label)
 ax.set_xticks(x); ax.set_xticklabels(order); ax.set_ylim(0,100); ax.set_ylabel("Per cent of responses"); ax.grid(axis="y",alpha=.25,linewidth=.6); ax.spines[["top","right"]].set_visible(False); ax.legend(frameon=False,fontsize=8,loc="upper left")
 for col,label,off in series:
  for xx,v in zip(x+off,local[col]): ax.text(xx,min(float(v)+2,97),f"{v:.1f}%",ha="center",fontsize=7.7,rotation=0)
 fig.tight_layout(); fig.savefig(path,dpi=300,bbox_inches="tight",metadata={"Software":"Matplotlib"}); plt.close(fig)
def manifest():
 rows=[]
 for p in sorted(x for x in (ROOT/"outputs").rglob("*") if x.is_file()):
  rel=p.relative_to(ROOT).as_posix()
  if rel=="outputs/reports/output_manifest.csv": continue
  rows.append({"path":rel,"size_bytes":p.stat().st_size,"sha256":sha256(p)})
 write(pd.DataFrame(rows),REPORTS/"output_manifest.csv")
 with (ROOT/"OUTPUT_SHA256SUMS.txt").open("w",encoding="utf-8",newline="\n") as f:
  for r in rows: f.write(f"{r['sha256']}  {r['path']}\n")
def main():
 for d in [TABLES,FIGSRC,FIGURES,REPORTS]:
  if d.exists():
   shutil.rmtree(d)
  d.mkdir(parents=True,exist_ok=True)
 sample=pd.read_csv(SOURCE/"sample_scope_counts.csv"); stages=add_stats(pd.read_csv(SOURCE/"engagement_stage_counts.csv")); constraints=add_stats(pd.read_csv(SOURCE/"constraint_counts.csv")); core=add_stats(pd.read_csv(SOURCE/"core_indicator_counts.csv")); workforce=add_stats(pd.read_csv(SOURCE/"workforce_measure_counts.csv")); overlap=add_stats(pd.read_csv(SOURCE/"workforce_overlap_counts.csv")); missing=pd.read_csv(SOURCE/"missingness_counts.csv"); missing["missing_percent"]=[pct(int(n),int(d)) for n,d in zip(missing.missing_n,missing.N)]
 size=pd.read_csv(SOURCE/"employee_band_counts.csv")
 for stem in ["active_use","project_engagement","active_or_project","workforce","workforce_conservative","both_constraints"]:
  size[f"{stem}_percent"]=[pct(int(n),int(d)) for n,d in zip(size[f"{stem}_n"],size.n)]
  cis=[wilson(int(n),int(d)) for n,d in zip(size[f"{stem}_n"],size.n)]; size[f"{stem}_ci95_low"]=[x[0] for x in cis]; size[f"{stem}_ci95_high"]=[x[1] for x in cis]
 write(sample,TABLES/"table_1_sample_scope.csv"); write(core,TABLES/"table_2_core_estimates.csv"); write(workforce,TABLES/"table_s6_workforce_preparation.csv"); write(overlap,TABLES/"table_s7_workforce_overlap_sensitivity.csv"); write(missing,TABLES/"table_s5_main_variable_missingness.csv"); write(stages,TABLES/"table_s10_ai_response_categories.csv"); write(constraints,TABLES/"table_s11_reported_constraints.csv"); write(size,TABLES/"table_s12_employee_band_patterns.csv")
 cont=pd.read_csv(SOURCE/"association_contingencies.csv"); results=[]; diagnostics=[]
 for tid in cont.test_id.drop_duplicates():
  sub=cont[cont.test_id==tid]; tab=sub.pivot(index="row_level",columns="column_level",values="n").fillna(0).astype(int); chi,p,dof,expected=chi2_contingency(tab,correction=False); denom=min(tab.shape[0]-1,tab.shape[1]-1); v=math.sqrt(chi/(tab.to_numpy().sum()*denom)); fp=None
  if tab.shape==(2,2): fp=float(fisher_exact(tab.to_numpy(),alternative="two-sided")[1])
  base={"test_id":tid,"test":sub.test_label.iloc[0],"n":int(tab.to_numpy().sum()),"chi_square":round(float(chi),3),"df":int(dof),"p_value":round(float(p),10),"p_display":pdisp(float(p)),"cramers_v":round(float(v),3),"minimum_expected_count":round(float(expected.min()),2)}
  results.append(base); diagnostics.append({**base,"table_shape":f"{tab.shape[0]}x{tab.shape[1]}","all_expected_at_least_5":bool((expected>=5).all()),"fisher_two_sided_p":fp,"fisher_p_display":"NA" if fp is None else pdisp(fp)})
 write(pd.DataFrame(results),TABLES/"table_s8_exploratory_association_tests.csv"); write(pd.DataFrame(diagnostics),TABLES/"table_s8b_association_diagnostics.csv")
 write(stages,FIGSRC/"figure_1_ai_response_categories.csv"); write(constraints,FIGSRC/"figure_2_reported_constraints.csv"); write(size,FIGSRC/"figure_3_outcome_definition_sensitivity.csv")
 bar(stages,"stage","percent",FIGURES/"Figure_1_AI_response_categories.png","Per cent of SME-classified responses"); bar(constraints,"constraint","percent",FIGURES/"Figure_2_reported_constraints.png","Per cent of SME-classified responses"); grouped(size,FIGURES/"Figure_3_outcome_definition_sensitivity.png")
 checks={"sample_212":int(sample.loc[sample.scope=="All completed responses","n"].iloc[0])==212,"sme_172":int(sample.loc[sample.scope=="SME-classified responses","n"].iloc[0])==172,"active_use_54":int(core.loc[core.indicator=="Active AI use","n"].iloc[0])==54,"project_51":int(core.loc[core.indicator=="Project-stage category (planning, testing or deployment)","n"].iloc[0])==51,"active_or_project_105":int(core.loc[core.indicator=="Active use or project-stage engagement","n"].iloc[0])==105,"workforce_134":int(core.loc[core.indicator=="At least one workforce-preparation measure","n"].iloc[0])==134,"workforce_conservative_121":int(core.loc[core.indicator.str.startswith("Workforce preparation excluding"),"n"].iloc[0])==121,"minimum_expected":float(pd.DataFrame(diagnostics).minimum_expected_count.min())==7.95}
 if not all(checks.values()): raise ValueError(checks)
 report={"status":"PASS","checks":checks,"aggregate_source_files":len(list(SOURCE.glob("*.csv"))),"generated_tables":len(list(TABLES.glob("*.csv"))),"generated_figures":len(list(FIGURES.glob("*.png"))),"respondent_level_data_present":False,"association_statistics_recomputed_from_contingency_counts":True}
 (REPORTS/"aggregate_validation.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8"); manifest(); print(json.dumps(report,indent=2,sort_keys=True))
if __name__=="__main__": main()
