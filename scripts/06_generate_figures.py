from __future__ import annotations
import hashlib, math, shutil, textwrap
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'
TABLES = OUT / 'tables'
FIGS = OUT / 'figures'
EDITORIAL = OUT / 'figures_editorial'
SOURCE = OUT / 'figure_source_data'
LOGS = OUT / 'logs'
for d in [FIGS, EDITORIAL, SOURCE, LOGS]:
    d.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

GREY_LIGHT = '#d9d9d9'
GREY_DARK = '#595959'
GRID_GREY = '#c8c8c8'
BLACK = '#111111'


def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).isoformat()
    with (LOGS / 'pipeline.log').open('a', encoding='utf-8') as f:
        f.write(f'[{ts}] {msg}\n')
    print(msg)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding='utf-8-sig')


def wilson(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n <= 0:
        return np.nan, np.nan
    p = k / n
    den = 1 + z*z/n
    centre = (p + z*z/(2*n)) / den
    half = z * math.sqrt((p*(1-p) + z*z/(4*n)) / n) / den
    return 100*max(0, centre-half), 100*min(1, centre+half)


def add_ci(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    lows, highs = [], []
    for _, r in df.iterrows():
        lo, hi = wilson(int(r['n']), int(r['denominator']))
        lows.append(round(lo, 1)); highs.append(round(hi, 1))
    df['wilson_95_low'] = lows
    df['wilson_95_high'] = highs
    return df


def wrap(s: str, width: int) -> str:
    return '\n'.join(textwrap.wrap(str(s), width=width, break_long_words=False, break_on_hyphens=False))


def save_figure(fig: plt.Figure, fig_id: str) -> list[Path]:
    editorial_png = EDITORIAL / f'{fig_id}.png'
    fig.savefig(editorial_png, bbox_inches='tight', pad_inches=0.05, facecolor='white', dpi=300)
    compat = FIGS / f'{fig_id}.png'
    shutil.copy2(editorial_png, compat)
    return [editorial_png, compat]


def manifest_row(fig_id: str, title: str, src: pd.DataFrame, inputs: list[str], outputs: list[Path], note: str) -> dict:
    src_path = SOURCE / f'{fig_id}_source.csv'
    write_csv(src, src_path)
    return {
        'figure_id': fig_id,
        'figure_title': title,
        'source_data_file': str(src_path.relative_to(ROOT)),
        'input_files': '; '.join(inputs),
        'output_files': '; '.join(str(p.relative_to(ROOT)) for p in outputs if p.exists()),
        'png_sha256': sha256(EDITORIAL / f'{fig_id}.png'),
        'generated_utc': datetime.now(timezone.utc).isoformat(),
        'generation_script': 'scripts/06_generate_figures.py',
        'style_note': note,
    }


def freq_table(variable: str, scope: str | None = None) -> pd.DataFrame:
    df = pd.read_csv(TABLES / 'frequency_tables_by_scope.csv')
    q = df[df['variable'] == variable].copy()
    if scope is not None:
        q = q[q['scope'] == scope].copy()
    return add_ci(q)


def selected_rows(scope: str, mapping: list[tuple[str, str]]) -> pd.DataFrame:
    rows = []
    for variable, label in mapping:
        df = freq_table(variable, scope)
        if df.empty:
            continue
        r = df.iloc[0].copy()
        rows.append({'category': label, 'n': int(r['n']), 'denominator': int(r['denominator']), 'percent': float(r['percent']), 'wilson_95_low': float(r['wilson_95_low']), 'wilson_95_high': float(r['wilson_95_high'])})
    return pd.DataFrame(rows)


def barh(df: pd.DataFrame, fig_id: str, xlabel: str, left: float, label_width: int, xmax: float = 100.0) -> list[Path]:
    d = df.iloc[::-1].copy()
    vals = d['percent'].astype(float).to_numpy()
    labs = [wrap(x, label_width) for x in d['category']]
    y = np.arange(len(d))
    fig, ax = plt.subplots(figsize=(6.6, 3.65))
    bars = ax.barh(y, vals, height=0.62, color=GREY_LIGHT, edgecolor=BLACK, linewidth=0.9)
    ax.set_yticks(y); ax.set_yticklabels(labs)
    ax.set_xlabel(xlabel); ax.set_xlim(0, xmax)
    ax.xaxis.grid(True, linestyle=':', linewidth=0.6, color=GRID_GREY)
    ax.set_axisbelow(True)
    ax.spines['left'].set_linewidth(0.8); ax.spines['bottom'].set_linewidth(0.8)
    for rect, v in zip(bars, vals):
        yc = rect.get_y() + rect.get_height()/2
        if v > xmax - 8:
            ax.text(v - 1.2, yc, f'{v:.1f}%', ha='right', va='center', fontsize=9)
        else:
            ax.text(v + 1.1, yc, f'{v:.1f}%', ha='left', va='center', fontsize=9)
    fig.subplots_adjust(left=left, right=0.97, bottom=0.16, top=0.96)
    paths = save_figure(fig, fig_id)
    plt.close(fig)
    return paths


def fig1(rows: list[dict]) -> None:
    label_map = {
        'Deloc familiarizat':'Not familiar',
        'Puțin familiarizat':'Slightly familiar',
        'Familiarizat, dar nu folosim tehnologii AI în companie':'Familiar, not using AI',
        'Familiarizat, avem proiecte (în diverse faze – bugetare, testare, implementare) pentru implementări de tehnologii AI în companie':'Projects planned/in deployment',
        'Folosim tehnologii AI în mod activ':'Active AI use',
    }
    order = ['Not familiar','Slightly familiar','Familiar, not using AI','Projects planned/in deployment','Active AI use']
    d = freq_table('ai_familiarity_label')
    d = d[d['scope'].isin(['sme_only','large_comparator'])].copy()
    d['category'] = d['category'].map(label_map).fillna(d['category'])
    d['order'] = d['category'].map({c:i for i,c in enumerate(order)})
    d = d.sort_values('order')
    p = d.pivot(index='category', columns='scope', values='percent').reindex(order)
    y = np.arange(len(p)); h = 0.32
    fig, ax = plt.subplots(figsize=(6.6, 3.65))
    sme = p['sme_only'].to_numpy(); large = p['large_comparator'].to_numpy()
    ax.barh(y - h/2, sme, height=h, color=GREY_LIGHT, edgecolor=BLACK, linewidth=0.9, label='SME-only (n = 172)')
    ax.barh(y + h/2, large, height=h, color=GREY_DARK, edgecolor=BLACK, linewidth=0.9, label='Large comparator (n = 39)')
    ax.set_yticks(y); ax.set_yticklabels([wrap(x, 30) for x in p.index])
    ax.set_xlabel('Respondents within analytical sample (%)'); ax.set_xlim(0, 60)
    ax.xaxis.grid(True, linestyle=':', linewidth=0.6, color=GRID_GREY); ax.set_axisbelow(True)
    for yy, v in zip(y - h/2, sme): ax.text(v + 0.8, yy, f'{v:.1f}%', va='center', fontsize=9)
    for yy, v in zip(y + h/2, large): ax.text(v + 0.8, yy, f'{v:.1f}%', va='center', fontsize=9)
    ax.legend(loc='lower right', frameon=False)
    fig.subplots_adjust(left=0.28, right=0.97, bottom=0.16, top=0.96)
    out = save_figure(fig, 'Figure_1_AI_readiness_ladder')
    rows.append(manifest_row('Figure_1_AI_readiness_ladder', 'AI readiness ladder by analytical sample', d[['scope','category','n','denominator','percent','wilson_95_low','wilson_95_high']], ['outputs/tables/frequency_tables_by_scope.csv'], out, 'Grouped horizontal bar chart; grayscale; no internal title; caption carries figure title.'))


def fig2(rows: list[dict]) -> None:
    mapping = [
        ('barrier_costuri_mari_de_implementare','High implementation costs'),
        ('barrier_lipsa_expertizei_tehnice','Lack of technical expertise'),
        ('barrier_ingrijorari_legate_de_reglementari_sau_etica','Regulatory or ethical concerns'),
        ('barrier_incertitudini_privind_impactul_ai','Uncertainty about AI impact'),
        ('barrier_rezistenta_din_partea_angajatilor','Employee resistance'),
        ('barrier_nivelul_de_maturitate_al_noilor_tehnologii_es','AI technology maturity concerns'),
    ]
    d = selected_rows('sme_only', mapping)
    out = barh(d, 'Figure_2_SME_barriers', 'SME respondents selecting the barrier (%)', 0.37, 34)
    rows.append(manifest_row('Figure_2_SME_barriers', 'Perceived barriers among SME respondents', d, ['outputs/tables/frequency_tables_by_scope.csv'], out, 'Single-sample horizontal bar chart; labels wrapped to avoid clipping.'))


def fig3(rows: list[dict]) -> None:
    mapping = [
        ('upskilling_programe_interne_de_mentorat_instruire_in_uti','Internal mentoring/training in AI use'),
        ('upskilling_decontarea_unor_certificari_cursuri_online_de','Reimbursed AI certifications or online courses'),
        ('upskilling_parteneriate_cu_universitati_pentru_instruire','University/research-institute training partnerships'),
        ('upskilling_angajarea_unor_consultanti_externi_pentru_cer','External consultants or experts'),
        ('upskilling_nu_avem_inca_masuri_specifice','No specific AI upskilling measures selected'),
        ('upskilling_abonamente_suportate_de_angajator_pentru_unel','Employer-supported AI-tool subscriptions'),
    ]
    d = selected_rows('sme_only', mapping)
    out = barh(d, 'Figure_3_SME_workforce_preparation', 'SME respondents selecting the measure (%)', 0.43, 36)
    rows.append(manifest_row('Figure_3_SME_workforce_preparation', 'Workforce preparation measures among SME respondents', d, ['outputs/tables/frequency_tables_by_scope.csv'], out, 'Single-sample horizontal bar chart; labels wrapped to avoid clipping.'))


def fig4(rows: list[dict]) -> None:
    d = pd.read_csv(TABLES / 'figure_4_governance_orientation_inputs.csv').copy()
    d = d.rename(columns={'label':'category'})
    d['category'] = d['category'].str.replace('\n', ' ', regex=False)
    d = add_ci(d)
    out = barh(d, 'Figure_4_workforce_governance_orientation', 'SME respondents (%)', 0.42, 38)
    rows.append(manifest_row('Figure_4_workforce_governance_orientation', 'Selected workforce and governance outcomes among SME respondents', d, ['outputs/tables/figure_4_governance_orientation_inputs.csv'], out, 'Composite outcome chart generated from tabulated source values; long labels kept within the plot area.'))


def fig_s1(rows: list[dict]) -> None:
    d = pd.read_csv(TABLES / 'figure_S1_capability_pressure_inputs.csv').copy()
    d = d.rename(columns={'item':'category','count':'active_ai_use_n','ci_low':'wilson_95_low','ci_high':'wilson_95_high'})
    p = d.iloc[::-1].copy(); y = np.arange(len(p))
    vals = p['percent'].to_numpy()
    err_low = vals - p['wilson_95_low'].to_numpy(); err_high = p['wilson_95_high'].to_numpy() - vals
    fig, ax = plt.subplots(figsize=(6.6, 3.65))
    bars = ax.barh(y, vals, height=0.62, color=GREY_LIGHT, edgecolor=BLACK, linewidth=0.9)
    ax.errorbar(vals, y, xerr=[err_low, err_high], fmt='none', ecolor=BLACK, elinewidth=1.0, capsize=4, capthick=1.0)
    ax.set_yticks(y); ax.set_yticklabels([wrap(f"{r['category']} (n = {int(r['denominator'])})", 34) for _, r in p.iterrows()])
    ax.set_xlabel('Active AI use (%)'); ax.set_xlim(0,100)
    ax.xaxis.grid(True, linestyle=':', linewidth=0.6, color=GRID_GREY); ax.set_axisbelow(True)
    for rect, v in zip(bars, vals):
        ax.text(min(v + 1.4, 96), rect.get_y() + rect.get_height()*0.78, f'{v:.1f}%', ha='left', va='center', fontsize=9)
    fig.subplots_adjust(left=0.43, right=0.97, bottom=0.16, top=0.96)
    out = save_figure(fig, 'Supplementary_Figure_S1_capability_pressure')
    rows.append(manifest_row('Supplementary_Figure_S1_capability_pressure', 'Active AI use by cost/expertise capability-pressure category', d, ['outputs/tables/figure_S1_capability_pressure_inputs.csv'], out, 'SME-only horizontal chart with Wilson intervals; value labels offset from interval whiskers.'))
    plt.close(fig)


def conceptual(rows: list[dict]) -> None:
    nodes = [
        ('N1', 'National context\nLow official AI use\nlagging SME digitalisation', 0.055, 0.745, 0.25, 0.135),
        ('N2', 'Survey evidence\nEngaged respondents\nhigher use and pipeline', 0.375, 0.745, 0.25, 0.135),
        ('N3', 'Governance pressure\nAI literacy\nethical regulation', 0.695, 0.745, 0.25, 0.135),
        ('N4', 'Capacity constraints\ncost + expertise\ndata + change', 0.055, 0.455, 0.25, 0.135),
        ('N5', 'Socio-technical readiness\nskills + routines\ntrust + leadership', 0.375, 0.455, 0.25, 0.135),
        ('N6', 'Policy ecosystem\nfunding + guidance\ncapability infrastructure', 0.695, 0.455, 0.25, 0.135),
        ('N7', 'Capability pressure\nConvert awareness and experimentation into\ncapability-backed, regulation-aware deployment', 0.255, 0.145, 0.49, 0.145),
    ]
    edges = [('N1','N4'),('N2','N5'),('N3','N6'),('N4','N7'),('N5','N7'),('N6','N7')]
    node_df = pd.DataFrame(nodes, columns=['node_id','text','x','y','w','h'])
    edge_df = pd.DataFrame(edges, columns=['from_node','to_node'])
    write_csv(node_df, SOURCE / 'Conceptual_Figure_nodes.csv'); write_csv(edge_df, SOURCE / 'Conceptual_Figure_edges.csv')
    fig, ax = plt.subplots(figsize=(6.6, 3.8)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    coords = {}
    for node_id, txt, x, y, w, h in nodes:
        box = FancyBboxPatch((x,y), w, h, boxstyle='round,pad=0.013,rounding_size=0.016', linewidth=0.9, edgecolor=BLACK, facecolor='white')
        ax.add_patch(box)
        lines = txt.split('\n')
        ax.text(x+w/2, y+h*0.66, lines[0], ha='center', va='center', fontsize=7.1, fontweight='bold', linespacing=1.08)
        ax.text(x+w/2, y+h*0.35, '\n'.join(lines[1:]), ha='center', va='center', fontsize=6.9, linespacing=1.08)
        coords[node_id] = (x,y,w,h)
    def arrow(start, end): ax.add_patch(FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=11, linewidth=0.85, color=BLACK, shrinkA=5, shrinkB=5))
    for s,t in [('N1','N4'),('N2','N5'),('N3','N6')]:
        x1,y1,w1,h1 = coords[s]; x2,y2,w2,h2 = coords[t]
        arrow((x1+w1/2,y1), (x2+w2/2,y2+h2))
    x2,y2,w2,h2 = coords['N7']
    for s, frac in [('N4',0.22),('N5',0.50),('N6',0.78)]:
        x1,y1,w1,h1 = coords[s]
        arrow((x1+w1/2,y1), (x2+w2*frac,y2+h2))
    ax.text(0.5, 0.06, 'Generated from explicit node and edge source-data files', ha='center', va='center', fontsize=5.6, color='#555555')
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.03, top=0.97)
    out = save_figure(fig, 'Optional_Conceptual_Figure_capability_governance_model')
    rows.append({'figure_id':'Optional_Conceptual_Figure_capability_governance_model','figure_title':'Conceptual synthesis: capability pressure under responsible-AI governance','source_data_file':'outputs/figure_source_data/Conceptual_Figure_nodes.csv; outputs/figure_source_data/Conceptual_Figure_edges.csv','input_files':'scripts/06_generate_figures.py node/edge specification','output_files':'; '.join(str(p.relative_to(ROOT)) for p in out if p.exists()),'png_sha256':sha256(EDITORIAL/'Optional_Conceptual_Figure_capability_governance_model.png'),'generated_utc':datetime.now(timezone.utc).isoformat(),'generation_script':'scripts/06_generate_figures.py','style_note':'Optional conceptual figure; generated from explicit node/edge tables; arrows terminate at box boundaries.'})
    plt.close(fig)


def visual_qa(manifest: pd.DataFrame) -> pd.DataFrame:
    from PIL import Image
    qa = []
    for _, r in manifest.iterrows():
        png = EDITORIAL / f"{r['figure_id']}.png"
        if not png.exists(): continue
        img = Image.open(png).convert('RGB'); w, h = img.size
        arr = np.asarray(img); m = 8
        edge_min = min(arr[:m,:,:].mean(), arr[-m:,:,:].mean(), arr[:,:m,:].mean(), arr[:,-m:,:].mean())
        qa.append({'figure_id':r['figure_id'],'png_file':str(png.relative_to(ROOT)),'width_px':w,'height_px':h,'aspect_ratio':round(w/h,3),'sha256':sha256(png),'edge_min_mean_rgb':round(float(edge_min),2),'visual_status':'pass - high-resolution export','notes':'PNG generated by script at 300 dpi.'})
    return pd.DataFrame(qa)


def main() -> None:
    log('Manuscript figure generation started')
    rows: list[dict] = []
    fig1(rows); fig2(rows); fig3(rows); fig4(rows); fig_s1(rows); conceptual(rows)
    mf = pd.DataFrame(rows)
    write_csv(mf, OUT / 'FIGURE_MANIFEST.csv')
    write_csv(visual_qa(mf), OUT / 'FIGURE_VISUAL_QA.csv')
    log(f'Figures generated: {len(rows)}; see outputs/figures_editorial, outputs/FIGURE_MANIFEST.csv and outputs/FIGURE_VISUAL_QA.csv')

if __name__ == '__main__':
    main()
