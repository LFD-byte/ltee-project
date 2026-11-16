#!/usr/bin/env bash
# Shared by Pixi and the container reproduction entry point.
set -euo pipefail
mkdir -p results/qc/fastqc
fastqc --quiet --threads 2 --outdir results/qc/fastqc data/raw/fastq/*.fastq
multiqc --force -o results/qc/multiqc results/qc/fastqc
