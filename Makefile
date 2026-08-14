PYTHON ?= python

.PHONY: install test study1 simulation v3-all ci legacy-v2

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[test]"

test:
	$(PYTHON) -m pytest -q tests_v3

study1:
	$(PYTHON) scripts/run_study1.py

simulation:
	$(PYTHON) simulations/run_simulation.py --replications 2000 --seed 20260813

v3-all: test study1 simulation

ci: install v3-all
	@test "$$(tr -d '\r\n' < VERSION)" = "3.0.0-rc1"

# The version 2.0.2 workflow remains available during the RC period for
# compatibility and provenance. It is not the canonical v3 methodology build.
legacy-v2:
	$(PYTHON) scripts/build_aggregate.py
