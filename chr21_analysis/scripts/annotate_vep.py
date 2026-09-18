#!/usr/bin/env python3
"""Resumable Ensembl VEP annotation for the ERR297183 chr21 portfolio project."""

import argparse
import collections
import gzip
import hashlib
import json
import pathlib
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path("chr21_analysis")
INPUT = ROOT / "results/variants/ERR297183_chr21.normalized.vcf.gz"
OUT = ROOT / "results/annotation"
BATCH_DIR = OUT / "vep_batches"
URL = "https://rest.ensembl.org/vep/homo_sapiens/region?hgvs=1&mane=1"
BATCH_SIZE = 100


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
    temporary.replace(path)


def read_variants():
    if not INPUT.is_file():
        raise FileNotFoundError(f"Input VCF not found: {INPUT}")

    variants = []
    with gzip.open(INPUT, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) < 8:
                raise ValueError("Malformed VCF record")
            if fields[0] not in ("21", "chr21"):
                raise ValueError(f"Unexpected chromosome: {fields[0]}")
            if "," in fields[4]:
                raise ValueError(
                    "Multiallelic VCF record detected; split alleles before annotation"
                )
            fields[0] = "21"
            variants.append(" ".join(fields[:8]))

    if not variants:
        raise ValueError("VCF contains no variants")
    return variants


def variant_key(record):
    fields = record.split()
    if len(fields) < 5:
        raise ValueError(f"Invalid VCF input in VEP response: {record!r}")
    return tuple(fields[:5])


def validate_response(requested, response):
    if not isinstance(response, list):
        raise ValueError("VEP response is not a JSON array")
    if len(response) != len(requested):
        raise ValueError(
            f"Count mismatch: sent {len(requested)}, received {len(response)}"
        )

    received = []
    for item in response:
        if not isinstance(item, dict) or not isinstance(item.get("input"), str):
            raise ValueError("VEP result has no valid input identifier")
        if "most_severe_consequence" not in item:
            raise ValueError("VEP result has no consequence annotation")
        received.append(variant_key(item["input"]))

    if collections.Counter(received) != collections.Counter(
        variant_key(item) for item in requested
    ):
        raise ValueError("Input/output variant identity mismatch")


def request_vep(batch):
    payload = json.dumps({"variants": batch}).encode("utf-8")
    for attempt in range(1, 6):
        request = urllib.request.Request(
            URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "chr21-portfolio-vep/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                result = json.load(response)
            validate_response(batch, result)
            return result
        except urllib.error.HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504):
                raise
            retry_after = error.headers.get("Retry-After", "")
            delay = int(retry_after) if retry_after.isdigit() else min(60, 2**attempt)
            print(
                f"HTTP {error.code}; retry {attempt}/5 in {delay}s",
                file=sys.stderr,
                flush=True,
            )
        except (urllib.error.URLError, TimeoutError) as error:
            delay = min(60, 2**attempt)
            print(
                f"Network error: {error}; retry {attempt}/5 in {delay}s",
                file=sys.stderr,
                flush=True,
            )
        if attempt < 5:
            time.sleep(delay)
    raise RuntimeError("VEP request failed after five attempts")


def text(value):
    if value is None:
        return ""
    if isinstance(value, list):
        return ",".join(str(item) for item in value)
    return str(value)


def write_tsv(results, destination):
    columns = [
        "input", "chromosome", "position", "ref", "alt",
        "most_severe_consequence", "gene_symbol", "gene_id",
        "transcript_id", "biotype", "consequence_terms",
        "hgvsc", "hgvsp", "impact", "mane_select",
        "canonical", "protein_start", "protein_end",
        "amino_acids", "codons",
    ]
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        handle.write("\t".join(columns) + "\n")
        for result in results:
            fields = result["input"].split()
            base = {
                "input": result["input"],
                "chromosome": fields[0],
                "position": fields[1],
                "ref": fields[3],
                "alt": fields[4],
                "most_severe_consequence": result.get("most_severe_consequence"),
            }
            transcripts = result.get("transcript_consequences") or [{}]
            for transcript in transcripts:
                row = {
                    **base,
                    "gene_symbol": transcript.get("gene_symbol"),
                    "gene_id": transcript.get("gene_id"),
                    "transcript_id": transcript.get("transcript_id"),
                    "biotype": transcript.get("biotype"),
                    "consequence_terms": transcript.get("consequence_terms"),
                    "hgvsc": transcript.get("hgvsc"),
                    "hgvsp": transcript.get("hgvsp"),
                    "impact": transcript.get("impact"),
                    "mane_select": transcript.get("mane_select"),
                    "canonical": transcript.get("canonical"),
                    "protein_start": transcript.get("protein_start"),
                    "protein_end": transcript.get("protein_end"),
                    "amino_acids": transcript.get("amino_acids"),
                    "codons": transcript.get("codons"),
                }
                handle.write(
                    "\t".join(text(row.get(column)).replace("\t", " ") for column in columns)
                    + "\n"
                )
    temporary.replace(destination)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full",
        action="store_true",
        help="Annotate all variants; without this flag only the first 100 are tested",
    )
    args = parser.parse_args()

    variants = read_variants()
    selected = variants if args.full else variants[:BATCH_SIZE]

    OUT.mkdir(parents=True, exist_ok=True)
    BATCH_DIR.mkdir(parents=True, exist_ok=True)

    all_results = []
    total_batches = (len(selected) + BATCH_SIZE - 1) // BATCH_SIZE

    for index in range(total_batches):
        batch = selected[index * BATCH_SIZE:(index + 1) * BATCH_SIZE]
        fingerprint = hashlib.sha256(
            json.dumps({"url": URL, "variants": batch}).encode("utf-8")
        ).hexdigest()[:16]
        path = BATCH_DIR / f"batch_{index + 1:04d}_{fingerprint}.json"

        if path.exists():
            try:
                with path.open(encoding="utf-8") as handle:
                    result = json.load(handle)
                validate_response(batch, result)
                status = "REUSED"
            except (ValueError, json.JSONDecodeError, KeyError):
                print(f"Invalid cached batch: {path}", file=sys.stderr)
                raise
        else:
            result = request_vep(batch)
            atomic_json(path, result)
            status = "SAVED"

        all_results.extend(result)
        print(
            f"[{index + 1}/{total_batches}] {status}: {len(batch)} variants",
            flush=True,
        )
        if status == "SAVED":
            time.sleep(1)

    validate_response(selected, all_results)

    prefix = "ERR297183_chr21.vep_full" if args.full else "ERR297183_chr21.vep_test100"
    json_path = OUT / f"{prefix}.json"
    tsv_path = OUT / f"{prefix}.tsv"
    atomic_json(json_path, all_results)
    write_tsv(all_results, tsv_path)

    print(f"SUCCESS: {len(selected)} input variants; {len(all_results)} VEP results")
    print(f"JSON: {json_path}")
    print(f"TSV:  {tsv_path}")
    if not args.full:
        print("TEST ONLY: full annotation has NOT been started.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
