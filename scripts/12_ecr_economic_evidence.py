from __future__ import annotations
from pathlib import Path
import math, textwrap, hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
from statsmodels.stats.proportion import proportion_confint
import statsmodels.api as sm
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'
ECR_OUT = OUT / 'ecr'
TAB_DIR = ECR_OUT / 'tables'
FIG_DIR = ECR_OUT / 'figures'
SRC_DIR = ECR_OUT / 'figure_source_data'
for d in [TAB_DIR, FIG_DIR, SRC_DIR]: d.mkdir(parents=True, exist_ok=True)
def pct(n,d): return round(100*n/d,1) if d else np.nan
def wilson(n,d):
    lo, hi = proportion_confint(n,d,alpha=0.05,method='wilson') if d else (np.nan,np.nan)
    return round(lo*100,1), round(hi*100,1)
def wcsv(df, path):
    path.parent.mkdir(parents=True, exist_ok=True); df.to_csv(path,index=False,encoding='utf-8-sig')
def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()
def wrap_labels(vals,width=34): return ['\n'.join(textwrap.wrap(str(v), width=width, break_long_words=False)) for v in vals]
def horizontal_bar(df,label_col,pct_col,n_col,d_col,path,title=None):
    local=df.copy().iloc[::-1]
    fig, ax=plt.subplots(figsize=(9.5,max(3.2,.52*len(local)+1.2)))
    y=np.arange(len(local)); ax.barh(y,local[pct_col],height=.58,color='#4D4D4D')
    ax.set_yticks(y); ax.set_yticklabels(wrap_labels(local[label_col].tolist()),fontsize=9)
    ax.set_xlim(0,100); ax.set_xlabel('Per cent of respondents',fontsize=10)
    if title: ax.set_title(title,fontsize=11,loc='left',pad=8)
    ax.grid(axis='x',alpha=.25,linewidth=.6); ax.spines[['top','right','left']].set_visible(False); ax.tick_params(axis='y',length=0)
    for i,(_,r) in enumerate(local.iterrows()): ax.text(min(r[pct_col]+1.6,104),i,f"{r[pct_col]:.1f}% ({int(r[n_col])}/{int(r[d_col])})",va='center',fontsize=8.5)
    fig.tight_layout(); fig.savefig(path,dpi=300,bbox_inches='tight'); plt.close(fig)
def ci_bar(df,label_col,pct_col,lo_col,hi_col,n_col,d_col,path,title=None):
    local=df.copy(); fig, ax=plt.subplots(figsize=(8.8,max(3.2,.56*len(local)+1.2)))
    y=np.arange(len(local)); vals=local[pct_col].values
    ax.barh(y, vals, color='#4D4D4D',height=.54); ax.errorbar(vals,y,xerr=np.vstack([vals-local[lo_col].values,local[hi_col].values-vals]),fmt='none',ecolor='black',capsize=3,elinewidth=.9)
    ax.set_yticks(y); ax.set_yticklabels(wrap_labels(local[label_col].tolist(),32),fontsize=9); ax.set_xlim(0,100); ax.set_xlabel('Per cent of respondents',fontsize=10)
    if title: ax.set_title(title,fontsize=11,loc='left',pad=8)
    ax.grid(axis='x',alpha=.25,linewidth=.6); ax.spines[['top','right','left']].set_visible(False); ax.tick_params(axis='y',length=0)
    for i,(_,r) in enumerate(local.iterrows()): ax.text(min(r[pct_col]+2,102),i,f"{r[pct_col]:.1f}%",va='center',fontsize=8.5)
    fig.tight_layout(); fig.savefig(path,dpi=300,bbox_inches='tight'); plt.close(fig)
def test_chi(sub,row,col,label):
    table=pd.crosstab(sub[row], sub[col]); chi,p,dof,exp=chi2_contingency(table, correction=False); v=math.sqrt(chi/(table.values.sum()*min(table.shape[0]-1,table.shape[1]-1))) if min(table.shape[0]-1,table.shape[1]-1)>0 else np.nan
    return {'test_label':label,'scope_n':int(table.values.sum()),'row_variable':row,'column_variable':col,'chi_square':round(float(chi),4),'df':int(dof),'p_value':round(float(p),6),'cramers_v':round(v,4),'min_expected':round(float(exp.min()),4),'admissibility':'exploratory association only; no causal interpretation'}
def main():
    df=pd.read_csv(OUT/'analysis_dataset_constructed.csv'); sme=df[df['is_sme']==1].copy(); full=df.copy(); large=df[df['analysis_scope_large_comparator']==1].copy()
    wcsv(pd.DataFrame([{'scope':'Full completed responses','n':len(full),'share_of_full_percent':pct(len(full),len(full))},{'scope':'SME-only analytical sample','n':len(sme),'share_of_full_percent':pct(len(sme),len(full))},{'scope':'Large-firm comparator','n':len(large),'share_of_full_percent':pct(len(large),len(full))},{'scope':'Missing firm-size category','n':int(df['firm_size_category'].isna().sum()),'share_of_full_percent':pct(int(df['firm_size_category'].isna().sum()),len(full))}]), TAB_DIR/'ECR_sample_scope.csv')
    stage_order=[('Not familiar at all','Deloc familiarizat'),('Slightly familiar','Puțin familiarizat'),('Familiar, not yet using AI','Familiarizat, dar nu folosim tehnologii AI în companie'),('Projects in planning, testing or deployment','Familiarizat, avem proiecte (în diverse faze – bugetare, testare, implementare) pentru implementări de tehnologii AI în companie'),('Active AI use','Folosim tehnologii AI în mod activ')]
    ladder=[]
    for label,raw in stage_order:
        n=int((sme['ai_familiarity_label']==raw).sum()); d=len(sme); lo,hi=wilson(n,d); ladder.append({'stage':label,'n':n,'denominator':d,'percent':pct(n,d),'wilson_95_low':lo,'wilson_95_high':hi})
    ladder=pd.DataFrame(ladder); wcsv(ladder,TAB_DIR/'ECR_SME_AI_restructuring_ladder.csv'); wcsv(ladder,SRC_DIR/'ECR_Figure_1_SME_AI_restructuring_ladder_source.csv')
    barrier_map=[('High implementation costs','barrier_costuri_mari_de_implementare'),('Lack of technical expertise','barrier_lipsa_expertizei_tehnice'),('Regulatory or ethical concerns','barrier_ingrijorari_legate_de_reglementari_sau_etica'),('Uncertainty about AI impact','barrier_incertitudini_privind_impactul_ai'),('Employee resistance','barrier_rezistenta_din_partea_angajatilor'),('Immature or low-maturity technology','barrier_nivelul_de_maturitate_al_noilor_tehnologii_es')]
    bar=[]
    for label,col in barrier_map:
        n=int(sme[col].sum()); d=len(sme); lo,hi=wilson(n,d); bar.append({'constraint':label,'n':n,'denominator':d,'percent':pct(n,d),'wilson_95_low':lo,'wilson_95_high':hi})
    bar=pd.DataFrame(bar).sort_values('percent',ascending=False); wcsv(bar,TAB_DIR/'ECR_SME_capability_constraints.csv'); wcsv(bar,SRC_DIR/'ECR_Figure_2_SME_capability_constraints_source.csv')
    up_map=[('Internal mentoring or training','upskilling_programe_interne_de_mentorat_instruire_in_uti'),('Online courses or certifications reimbursed','upskilling_decontarea_unor_certificari_cursuri_online_de'),('University or institute partnerships','upskilling_parteneriate_cu_universitati_pentru_instruire'),('External consultants or experts','upskilling_angajarea_unor_consultanti_externi_pentru_cer'),('Employer-supported AI tools/subscriptions','upskilling_abonamente_suportate_de_angajator_pentru_unel'),('No specific measures yet','upskilling_nu_avem_inca_masuri_specifice')]
    up=[]
    for label,col in up_map:
        n=int(sme[col].sum()); d=len(sme); lo,hi=wilson(n,d); up.append({'measure':label,'n':n,'denominator':d,'percent':pct(n,d),'wilson_95_low':lo,'wilson_95_high':hi})
    up=pd.DataFrame(up).sort_values('percent',ascending=False); wcsv(up,TAB_DIR/'ECR_SME_skill_formation_measures.csv'); wcsv(up,SRC_DIR/'ECR_Figure_3_SME_skill_formation_source.csv')
    policy=[]
    for label,n in [('Government support very or moderately important', int(sme['government_support_role_label'].str.contains('Foarte important|Moderat important',regex=True,na=False).sum())),('Government support essential', int(sme['government_support_role_label'].str.contains('Foarte important',na=False).sum())),('Stricter ethical AI regulation supported', int(sme['governance_support_strict_regulation'].sum())),('Romania perceived as behind in AI adoption', int(sme['romania_ai_competitiveness_label'].str.contains('în urmă',na=False).sum())),('Romania perceived as moderately competitive but investment-constrained', int(sme['romania_ai_competitiveness_label'].str.contains('moderat competitiv',na=False).sum()))]:
        d=len(sme); lo,hi=wilson(n,d); policy.append({'orientation':label,'n':n,'denominator':d,'percent':pct(n,d),'wilson_95_low':lo,'wilson_95_high':hi})
    policy=pd.DataFrame(policy).sort_values('percent',ascending=False); wcsv(policy,TAB_DIR/'ECR_SME_policy_governance_orientation.csv'); wcsv(policy,SRC_DIR/'ECR_Figure_4_SME_policy_governance_orientation_source.csv')
    order=[('Micro SMEs','micro_1_9'),('Small SMEs','small_10_49'),('Medium SMEs','medium_50_249'),('Large comparator','large_250_plus')]
    grad=[]
    for label,cat in order:
        sub=df[df['firm_size_category']==cat]; d=len(sub)
        for ycol,ylab in [('adoption_binary_active','Active AI use'),('adoption_binary_active_or_planning','Active use or planning/testing/deployment')]:
            n=int(sub[ycol].sum()); lo,hi=wilson(n,d); grad.append({'firm_size':label,'outcome':ylab,'n':n,'denominator':d,'percent':pct(n,d),'wilson_95_low':lo,'wilson_95_high':hi})
    grad=pd.DataFrame(grad); wcsv(grad,TAB_DIR/'ECR_firm_size_gradient.csv'); wcsv(grad,SRC_DIR/'ECR_Figure_5_firm_size_gradient_source.csv')
    # Key, tests, logit, decisions, ledger
    key=pd.DataFrame([
    {'metric':'Completed survey responses','value':len(full),'interpretation':'Total finalised responses in the cleaned dataset.','recommended_manuscript_use':'Methods/sample description only; not SME denominator.'},
    {'metric':'SME-only analytical sample','value':len(sme),'interpretation':'Micro, small and medium firms after excluding large comparator and unknown size.','recommended_manuscript_use':'Primary denominator for SME claims.'},
    {'metric':'Large-firm comparator','value':len(large),'interpretation':'Large firms retained only for contrast and robustness.','recommended_manuscript_use':'Comparator only; never folded into SME claims.'},
    {'metric':'SME active AI use','value':f"{int(sme.adoption_binary_active.sum())}/{len(sme)} = {pct(int(sme.adoption_binary_active.sum()),len(sme))}%",'interpretation':'Current active use in the SME-only engaged sample.','recommended_manuscript_use':'Evidence of adoption frontier; not national prevalence.'},
    {'metric':'SME active use or planning/testing/deployment','value':f"{int(sme.adoption_binary_active_or_planning.sum())}/{len(sme)} = {pct(int(sme.adoption_binary_active_or_planning.sum()),len(sme))}%",'interpretation':'Broad frontier of AI-related digital restructuring in the engaged sample.','recommended_manuscript_use':'Use as readiness/restructuring frontier, with sample caveat.'},
    {'metric':'SME high implementation costs','value':f"{int(sme.barrier_costuri_mari_de_implementare.sum())}/{len(sme)} = {pct(int(sme.barrier_costuri_mari_de_implementare.sum()),len(sme))}%",'interpretation':'Dominant economic constraint.','recommended_manuscript_use':'Core capability-pressure finding.'},
    {'metric':'SME lack of technical expertise','value':f"{int(sme.barrier_lipsa_expertizei_tehnice.sum())}/{len(sme)} = {pct(int(sme.barrier_lipsa_expertizei_tehnice.sum()),len(sme))}%",'interpretation':'Dominant skill/capability constraint.','recommended_manuscript_use':'Core skill-formation finding.'},
    {'metric':'SME any positive upskilling measure','value':f"{int(sme.has_any_upskilling_measure.sum())}/{len(sme)} = {pct(int(sme.has_any_upskilling_measure.sum()),len(sme))}%",'interpretation':'Many engaged SMEs have begun skill formation, but not necessarily systematic AI capability.','recommended_manuscript_use':'Use cautiously; multiple response with overlap.'},
    {'metric':'SME support for government role, very or moderately important','value':f"{int(sme['government_support_role_label'].str.contains('Foarte important|Moderat important',regex=True,na=False).sum())}/{len(sme)} = {pct(int(sme['government_support_role_label'].str.contains('Foarte important|Moderat important',regex=True,na=False).sum()),len(sme))}%",'interpretation':'Near-universal preference for some public support among engaged SMEs.','recommended_manuscript_use':'Use as institutional-support demand, not policy evaluation.'},
    {'metric':'SME stricter ethical regulation support','value':f"{int(sme.governance_support_strict_regulation.sum())}/{len(sme)} = {pct(int(sme.governance_support_strict_regulation.sum()),len(sme))}%",'interpretation':'Governance demand coexists with capability pressure.','recommended_manuscript_use':'Use for responsible-AI governance framing.'}])
    wcsv(key,TAB_DIR/'ECR_key_economic_metrics.csv')
    assoc=pd.DataFrame([test_chi(df[df['firm_size_category'].notna()],'firm_size_category','adoption_binary_active_or_planning','Full sample firm-size gradient: active or planning'),test_chi(df[df['firm_size_category'].notna()],'firm_size_category','adoption_binary_active','Full sample firm-size gradient: active use'),test_chi(sme,'firm_size_category','adoption_binary_active_or_planning','SME-only size strata: active or planning'),test_chi(sme,'firm_size_category','adoption_binary_active','SME-only size strata: active use'),test_chi(sme,'has_any_upskilling_measure','adoption_binary_active','SME-only upskilling and active use'),test_chi(sme,'has_any_upskilling_measure','adoption_binary_active_or_planning','SME-only upskilling and active/planning frontier'),test_chi(sme,'governance_support_strict_regulation','adoption_binary_active','SME-only stricter regulation and active use')])
    wcsv(assoc,TAB_DIR/'ECR_exploratory_association_tests.csv')
    model_rows=[]; mod=sme.copy(); mod['small']=(mod['firm_size_category']=='small_10_49').astype(int); mod['medium']=(mod['firm_size_category']=='medium_50_249').astype(int)
    for outcome, desc in [('adoption_binary_active','Active AI use'),('adoption_binary_active_or_planning','Active use or planning/testing/deployment')]:
        X=sm.add_constant(mod[['small','medium','has_any_upskilling_measure','resource_constraint_count','governance_support_strict_regulation']]); y=mod[outcome]; result=sm.Logit(y,X).fit(disp=0,maxiter=100); conf=result.conf_int()
        for term in result.params.index:
            model_rows.append({'model':'SME parsimonious logit','outcome':desc,'term':term,'odds_ratio':round(float(np.exp(result.params[term])),3),'ci_95_low':round(float(np.exp(conf.loc[term,0])),3),'ci_95_high':round(float(np.exp(conf.loc[term,1])),3),'p_value':round(float(result.pvalues[term]),6),'n':int(result.nobs),'events':int(y.sum()),'pseudo_r2_mcfadden':round(float(1-result.llf/result.llnull),3),'admissibility_note':'Exploratory robustness model; association only; not causal; avoid main-text overinterpretation.'})
    wcsv(pd.DataFrame(model_rows),TAB_DIR/'ECR_parsimonious_logit_models.csv')
    wcsv(pd.DataFrame([
    {'candidate':'Descriptive SME-only evidence','decision':'Main text eligible','rationale':'All denominators are transparent and aligned to the SME research object; best fit for survey design.'},{'candidate':'Firm-size cross-tabulations with effect sizes','decision':'Main text eligible if concise','rationale':'Strongly relevant to capability and restructuring gradients; no causal claim required.'},{'candidate':'Chi-square/Fisher association tests','decision':'Appendix or compact methods/results eligible','rationale':'Useful for disciplined exploratory inference; p-values must be secondary to effect sizes and denominators.'},{'candidate':'Parsimonious logistic regression','decision':'Supplementary robustness only at this stage','rationale':'Events-per-variable is borderline but acceptable for a small model; explanatory variables are self-reported and cross-sectional, so causal interpretation is inadmissible.'},{'candidate':'High-dimensional sectoral or interaction models','decision':'Reject','rationale':'Sample size, multi-response sectors and sparse cells make these fragile for a Q1 economics submission.'},{'candidate':'Causal policy evaluation','decision':'Reject','rationale':'No experimental, quasi-experimental or longitudinal identification exists in the survey.'},{'candidate':'Population prevalence estimates for Romanian SMEs','decision':'Reject','rationale':'Non-probability engaged sample; official statistics should provide population context, not be replaced by this survey.'}]), TAB_DIR/'ECR_model_admissibility_decision.csv')
    wcsv(pd.DataFrame([
    {'claim_boundary':'Operational deployment is approximately 15-17%.','decision':'not used in the current manuscript','approved_statement':'SME active AI use is 54/172 = 31.4%; full-sample active AI use is 73/212 = 34.4%.','basis':'Appendix values and sample-scope counts do not support the earlier denominator.'},
    {'claim_boundary':'The completed sample can be treated as SMEs only.','decision':'not used in the current manuscript','approved_statement':'The full completed sample is N=212; the SME-only analytical sample is n=172; n=39 large firms are retained only as comparator; one case has missing firm size.','basis':'Firm-size records include large firms and one missing size case.'},
    {'claim_boundary':'The engaged SME sample shows nationally representative AI prevalence.','decision':'not used in the current manuscript','approved_statement':'In a low-adoption national context, the engaged SME sample shows a sizeable frontier of active use and planning but persistent capability constraints.','basis':'The survey is non-probability-based and reports higher AI use than national official data.'},
    {'claim_boundary':'Upskilling can be inferred as the complement of no specific measures.','decision':'not used in the current manuscript','approved_statement':'Positive upskilling selections and no-specific-measures selections overlap; report both and avoid complement logic.','basis':'The multiple-response design permits overlap.'}
    ]), TAB_DIR/'ECR_claim_boundary_decisions.csv')
    wcsv(pd.DataFrame([
    {'claim_id':'ECR-C01','allowed_public_wording':'The cleaned survey contains 212 complete responses, of which 172 are SMEs; 39 large firms are retained only as a comparator and one case lacks firm-size information.','evidence_file':'outputs/ecr/tables/ECR_sample_scope.csv','status':'allowed','forbidden_wording':'The study surveyed 212 Romanian SMEs.'},{'claim_id':'ECR-C02','allowed_public_wording':'In the SME-only engaged sample, 31.4% report active AI use and 61.0% report either active use or projects in planning, testing or deployment.','evidence_file':'outputs/ecr/tables/ECR_key_economic_metrics.csv; outputs/ecr/tables/ECR_SME_AI_restructuring_ladder.csv','status':'allowed with sampling caveat','forbidden_wording':'31.4% of all Romanian SMEs use AI.'},{'claim_id':'ECR-C03','allowed_public_wording':'Cost and technical expertise are the dominant reported capability constraints among surveyed SMEs, selected by 87.2% and 79.7%, respectively.','evidence_file':'outputs/ecr/tables/ECR_SME_capability_constraints.csv','status':'allowed','forbidden_wording':'Cost and expertise are statistically proven causes of non-adoption.'},{'claim_id':'ECR-C04','allowed_public_wording':'Most surveyed SMEs report at least one positive workforce-preparation measure, but no-specific-measures responses are not the complement of positive upskilling because the item was multiple-response.','evidence_file':'outputs/ecr/tables/ECR_SME_skill_formation_measures.csv','status':'allowed','forbidden_wording':'Only 22.1% of SMEs have no upskilling.'},{'claim_id':'ECR-C05','allowed_public_wording':'Public-support demand is high in the engaged SME sample: 98.3% describe government support as very or moderately important.','evidence_file':'outputs/ecr/tables/ECR_SME_policy_governance_orientation.csv','status':'allowed with sample caveat','forbidden_wording':'Romanian SMEs unanimously demand public intervention.'},{'claim_id':'ECR-C06','allowed_public_wording':'Association tests suggest a firm-size gradient in the broader active-or-planning frontier, but these results are exploratory and non-causal.','evidence_file':'outputs/ecr/tables/ECR_exploratory_association_tests.csv','status':'allowed if effect sizes and caveats are reported','forbidden_wording':'Firm size causes AI adoption.'},{'claim_id':'ECR-C07','allowed_public_wording':'A parsimonious SME-only logit is admissible only as supplementary robustness; the main article should rely primarily on descriptive and cross-tabulated evidence.','evidence_file':'outputs/ecr/tables/ECR_parsimonious_logit_models.csv; outputs/ecr/tables/ECR_model_admissibility_decision.csv','status':'allowed as methodological decision','forbidden_wording':'The model identifies causal determinants of AI adoption.'}]), TAB_DIR/'ECR_claim_evidence_ledger.csv')
    horizontal_bar(ladder,'stage','percent','n','denominator',FIG_DIR/'ECR_Figure_1_SME_AI_restructuring_ladder.png','SME AI restructuring ladder (n=172)')
    horizontal_bar(bar,'constraint','percent','n','denominator',FIG_DIR/'ECR_Figure_2_SME_capability_constraints.png','Capability constraints reported by SMEs (n=172)')
    horizontal_bar(up,'measure','percent','n','denominator',FIG_DIR/'ECR_Figure_3_SME_skill_formation.png','Skill-formation measures reported by SMEs (n=172)')
    horizontal_bar(policy,'orientation','percent','n','denominator',FIG_DIR/'ECR_Figure_4_SME_policy_governance_orientation.png','Institutional and governance orientation among SMEs (n=172)')
    ci_bar(grad[grad['outcome']=='Active use or planning/testing/deployment'],'firm_size','percent','wilson_95_low','wilson_95_high','n','denominator',FIG_DIR/'ECR_Figure_5_firm_size_gradient_active_or_planning.png','AI-restructuring frontier by firm size')
    fig_manifest=[]
    for p in sorted(FIG_DIR.glob('*.png')): fig_manifest.append({'figure_file':str(p.relative_to(ROOT)),'sha256':sha256(p),'status':'generated_from_csv_by_script'})
    wcsv(pd.DataFrame(fig_manifest), TAB_DIR/'ECR_figure_manifest.csv')
    reg=[]
    for p in sorted(TAB_DIR.glob('*.csv')): reg.append({'table_file':str(p.relative_to(ROOT)),'rows':len(pd.read_csv(p)),'sha256':sha256(p)})
    wcsv(pd.DataFrame(reg), TAB_DIR/'ECR_table_register.csv')
    print('ECR economic evidence outputs generated in', ECR_OUT)
if __name__ == '__main__': main()
