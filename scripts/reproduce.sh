#!/usr/bin/env bash
# Run from the project root, in the activated Pixi pipeline environment
# or the Docker image built with ENV_NAME=pipeline (which has no Pixi).
set -euo pipefail
python scripts/download_data.py
bash scripts/run_qc.sh
bash scripts/run_variant_calling.sh
python scripts/render_report.py
python scripts/check_variants.py
