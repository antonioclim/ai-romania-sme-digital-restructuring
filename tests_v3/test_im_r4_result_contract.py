from __future__ import annotations
import csv,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'outputs_v3'/'full_simulation'
SPEC=ROOT/'simulations'/'im_r4_reporting_specification.yml'
LOCK=ROOT/'simulations'/'im_r4_reporting_specification.lock.json'
def test_reporting_specification_lock():
 lock=json.loads(LOCK.read_text()); assert hashlib.sha256(SPEC.read_bytes()).hexdigest()==lock['specification_sha256']; assert lock['source_protocol_sha256']=='157bc88f41ff68261253fb19e79cc2c0aeebe63a4687d1f1073edd25ecc0b8f3'
def test_full_execution_audit_and_gate():
 audit=json.loads((RESULTS/'full_simulation_audit.json').read_text()); gate=json.loads((RESULTS/'IM_R4_GATE.json').read_text()); assert audit['status']=='PASS'; assert audit['stream_count']==4; assert audit['cell_count']==432; assert audit['replications_per_cell']==4000; assert audit['replicate_row_count']==1_728_000; assert audit['undefined_no_claim_cell_count']==0; assert audit['nested_level_violation_count']==0; assert gate['gate']=='GO'; assert gate['submission_gate']=='NO-GO'; assert gate['core_rerun_byte_identical'] is True
def test_reference_mechanisms_preserve_expected_signs():
 with (RESULTS/'reference_process_n250.csv').open(newline='',encoding='utf-8') as f:rows={r['scenario']:r for r in csv.DictReader(f)}
 assert float(rows['aligned_gradient']['population_delta_cramers_v'])>0
 assert float(rows['project_only_gradient']['population_delta_cramers_v'])>0
 assert float(rows['compensating_gradient']['population_delta_cramers_v'])<0
 assert float(rows['rank_reversal']['population_delta_cramers_v'])<0
 assert float(rows['mixed_order']['population_delta_cramers_v'])<0
 assert abs(float(rows['null_same_mixture']['population_delta_cramers_v']))<1e-12
 assert float(rows['rank_reversal']['probability_any_strict_reversal'])==1.0
