from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

import logging

def _ensure_parent_dir(path: Path) -> None:
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

def _normalize_records(records: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for record in records:
        normalized.append(dict(record))
    return normalized

def export_data(
    records: Iterable[Mapping[str, Any]],
    output_path: str,
    output_format: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
) -> None:
    """
    Export scraped records to disk in a given format.

    Args:
        records: Iterable of mapping objects (dict-like).
        output_path: Destination file path.
        output_format: One of 'json', 'jsonl', 'csv'. If None, inferred from extension.
        logger: Optional logger instance.
    """
    log = logger or logging.getLogger("facebook_following_scraper")
    path = Path(output_path)

    if output_format is None:
        ext = path.suffix.lower().lstrip(".")
        output_format = ext or "json"

    output_format = output_format.lower()
    supported = {"json", "jsonl", "csv"}
    if output_format not in supported:
        raise ValueError(f"Unsupported output format '{output_format}'. Supported: {sorted(supported)}")

    records_list = _normalize_records(records)
    log.debug(
        "Exporting %d record(s) to %s as %s",
        len(records_list),
        path,
        output_format,
    )

    _ensure_parent_dir(path)

    if output_format == "json":
        _export_json(records_list, path)
    elif output_format == "jsonl":
        _export_jsonl(records_list, path)
    elif output_format == "csv":
        _export_csv(records_list, path)

    log.info("Export complete: %s (%s)", path, output_format.upper())

def _export_json(records: List[Dict[str, Any]], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def _export_jsonl(records: List[Dict[str, Any]], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            json_line = json.dumps(record, ensure_ascii=False)
            f.write(json_line + "\n")

def _export_csv(records: List[Dict[str, Any]], path: Path) -> None:
    if not records:
        # Create an empty file
        path.touch()
        return

    # Collect all fieldnames across records
    fieldnames = set()
    for record in records:
        fieldnames.update(record.keys())

    ordered_fields = sorted(fieldnames)

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ordered_fields)
        writer.writeheader()
        for record in records:
            writer.writerow(record)