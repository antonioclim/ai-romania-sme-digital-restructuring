.PHONY: verify-source metadata-check environment-check build verify-outputs audit manifest-write test manifest-check all ci clean

.NOTPARALLEL:

verify-source:
	python scripts/verify_package.py --scope source

metadata-check:
	python scripts/generate_metadata.py --check

environment-check:
	python scripts/check_environment.py

build:
	python scripts/build_aggregate.py

verify-outputs:
	python scripts/verify_package.py --scope outputs

audit:
	python scripts/release_audit.py
	python scripts/scan_package.py

manifest-write:
	python scripts/generate_manifests.py --write

test:
	python -m pytest -q

manifest-check:
	python scripts/generate_manifests.py --check

all:
	$(MAKE) verify-source
	$(MAKE) metadata-check
	$(MAKE) environment-check
	$(MAKE) build
	$(MAKE) verify-outputs
	$(MAKE) audit
	$(MAKE) manifest-write
	$(MAKE) test
	$(MAKE) manifest-check

ci:
	$(MAKE) clean
	$(MAKE) all

clean:
	rm -rf outputs/tables outputs/figures outputs/figure_source_data outputs/reports OUTPUT_SHA256SUMS.txt
