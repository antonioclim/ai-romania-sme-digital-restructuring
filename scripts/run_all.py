from __future__ import annotations
import gc
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE_SCRIPTS = [
    '00_validate_inputs.py',
    '01_clean_data.py',
    '02_construct_variables.py',
    '03_descriptive_analysis.py',
    '04_inferential_analysis.py',
    '05_robustness_checks.py',
    '06_generate_figures.py',
    '07_generate_tables.py',
    '08_reference_data_validation.py',
    '12_ecr_economic_evidence.py',
]

def main() -> None:
    for script in CORE_SCRIPTS:
        print(f'\n=== Running {script} ===', flush=True)
        runpy.run_path(str(ROOT / 'scripts' / script), run_name='__main__')
        gc.collect()
    print('\nCore ECR pipeline complete. See outputs/ and outputs/ecr/.', flush=True)

if __name__ == '__main__':
    main()
