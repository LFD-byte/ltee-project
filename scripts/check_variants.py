"""Verify the default-depth LTEE variants against the native Pixi baseline.

Run from the project root: python scripts/check_variants.py [VCF_DIRECTORY]
Hashes cover sorted, complete non-header VCF records, including genotypes.
The baseline uses the raw-data checksums and pixi.lock recorded in README.
"""

import csv
import hashlib
import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent.parent
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "results/vcf"
    with (root / "metadata/expected_variants.tsv").open() as fh:
        expected = {row["sample"]: row for row in csv.DictReader(fh, delimiter="\t")}
    suffix = "_final_variants.vcf"
    actual = {p.name[:-len(suffix)]: p for p in folder.glob("*" + suffix)}
    if set(actual) != set(expected):
        sys.exit(f"VCF sample mismatch: expected {sorted(expected)}, found {sorted(actual)}")
    for sample, row in sorted(expected.items()):
        records = sorted(line for line in actual[sample].read_text().splitlines()
                         if line and not line.startswith("#"))
        digest = hashlib.sha256(("\n".join(records) + "\n").encode()).hexdigest()
        if len(records) != int(row["variants"]) or digest != row["records_sha256"]:
            sys.exit(f"FAIL {sample}: count={len(records)}, records_sha256={digest}")
        print(f"OK {sample}: {len(records)} variants, all records match native Pixi")


if __name__ == "__main__":
    main()
