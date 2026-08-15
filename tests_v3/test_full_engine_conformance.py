from pathlib import Path
import hashlib,json,numpy as np
from simulations.run_frozen_full_protocol import batch_cramers_v,full_cells,load_and_verify_protocol,pairwise_order_metrics,population_cramers_v,simulate_cell,COL
ROOT=Path(__file__).resolve().parents[1]; PROTOCOL=ROOT/'simulations'/'manuscript_protocol.yml'; FREEZE=ROOT/'simulations'/'manuscript_protocol.freeze.json'
def test_frozen_protocol_hash_and_cell_count():
 d=load_and_verify_protocol(PROTOCOL,FREEZE); f=json.loads(FREEZE.read_text()); assert hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()==f['protocol_sha256']; assert len(full_cells(d))==432
def test_batch_cramers_v_matches_population():
 w=np.array([1/3]*3); r=np.array([.1,.25,.4]); assert np.isclose(population_cramers_v(w,r),batch_cramers_v(np.array([[10,25,40]]),np.array([[100,100,100]]))[0],atol=1e-12)
def test_tie_aware_order():
 l=np.array([[.2,.2,.2],[.4,.2,.1]]); r=np.array([[.2,.3,.1],[.1,.2,.4]]); d,s=pairwise_order_metrics(l,r); assert np.isclose(d[0],1); assert np.isclose(s[0],0); assert np.isclose(d[1],1); assert np.isclose(s[1],1)
def test_cell_deterministic_and_nested():
 d=load_and_verify_protocol(PROTOCOL,FREEZE); c=full_cells(d)[0]; a=simulate_cell(d,c,1,20,np.random.SeedSequence(12345)); b=simulate_cell(d,c,1,20,np.random.SeedSequence(12345)); assert np.array_equal(a,b,equal_nan=True); assert np.all(a[:,COL['observed_broad_level']]>=a[:,COL['observed_active_level']])
