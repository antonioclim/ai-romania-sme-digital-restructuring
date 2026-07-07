.PHONY: all test verify-source verify-outputs clean

all:
	python scripts/run_all.py

test:
	python -m compileall scripts tests
	python -m pytest

verify-source:
	python scripts/verify_sha256sums.py SHA256SUMS.txt

verify-outputs:
	python scripts/verify_sha256sums.py SHA256SUMS_GENERATED_OUTPUTS.txt

clean:
	rm -rf outputs/tables/* outputs/figures/* outputs/logs/* outputs/reports/* outputs/analysis_dataset*.csv
