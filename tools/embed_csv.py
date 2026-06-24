#!/usr/bin/env python3
"""Validate a UTF-8 CSV and embed it into index.html between data markers."""

from __future__ import annotations

import csv
import json
import pathlib
import sys


FIELDS = [
    "id", "name", "district", "address", "lng", "lat", "coord_system",
    "type", "rating", "reviews", "avg_price", "tags", "description", "image",
]
OPTIONAL_FIELDS = ["bean_flavor", "social", "space", "service", "location_accuracy"]
START = "/* DATA_START */"
END = "/* DATA_END */"


def main() -> int:
    if len(sys.argv) != 3:
        print("用法: python3 tools/embed_csv.py data/shops.csv index.html")
        return 2

    csv_path = pathlib.Path(sys.argv[1])
    html_path = pathlib.Path(sys.argv[2])
    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = [field for field in FIELDS if field not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit("CSV 缺少字段: " + ", ".join(missing))
        rows = []
        for row_number, row in enumerate(reader, start=2):
            item = {field: (row.get(field) or "").strip() for field in FIELDS}
            item.update({field: (row.get(field) or "").strip() for field in OPTIONAL_FIELDS})
            for key in ("lng", "lat", "rating", "avg_price"):
                item[key] = float(item[key]) if item[key] else None
            item["reviews"] = int(float(item["reviews"])) if item["reviews"] else None
            if not item["id"] or not item["name"]:
                raise SystemExit(f"第 {row_number} 行缺少 id 或 name")
            rows.append(item)

    html = html_path.read_text(encoding="utf-8")
    begin = html.index(START) + len(START)
    finish = html.index(END, begin)
    payload = "\nconst RAW_SHOPS = " + json.dumps(rows, ensure_ascii=False, indent=2) + ";\n"
    html_path.write_text(html[:begin] + payload + html[finish:], encoding="utf-8")
    print(f"已嵌入 {len(rows)} 家门店到 {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
