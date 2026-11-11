"""Build the published layer: data/raw/ -> data/layers/sample_sites.geojson.

This is the one script you replace. The template turns a CSV of made-up sample points into the
GeoJSON points layer that data/layers/aggregation_spec.json names. Your version does whatever
your measure needs (download a city dataset, geocode a list, run a model) and ends by writing
the layer files next to the spec.

Standard library only, so `python build.py` works on a fresh machine. Add dependencies to
requirements.txt if you need them.

Keys and credentials: read them from the environment (os.environ["MY_API_KEY"]), never from a
file in this repo, and never write them into a layer. Everything in data/layers/ is published.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw" / "sample_sites.csv"
LAYER = ROOT / "data" / "layers" / "sample_sites.geojson"

# Rough Chicago bounding box. A point outside it is almost always a swapped lat/lon.
LAT_RANGE = (41.64, 42.03)
LON_RANGE = (-87.95, -87.52)


def load_rows() -> list[dict[str, str]]:
    # >>> Replace this with your source: an API call, a city data portal export, a scrape.
    with RAW.open(newline="") as f:
        return list(csv.DictReader(f))


def to_feature(row: dict[str, str]) -> dict:
    lat, lon = float(row["lat"]), float(row["lon"])
    if not (LAT_RANGE[0] <= lat <= LAT_RANGE[1] and LON_RANGE[0] <= lon <= LON_RANGE[1]):
        raise ValueError(f"{row['site_id']}: ({lat}, {lon}) is outside Chicago; lat/lon swapped?")
    return {
        "type": "Feature",
        # GeoJSON order is [longitude, latitude].
        "geometry": {"type": "Point", "coordinates": [round(lon, 6), round(lat, 6)]},
        # >>> Every property a metric names (numerator, denominator, flag, value) must be here.
        "properties": {
            "site_id": row["site_id"],
            "name": row["name"],
            "kind": row["kind"],
            "sample": True,
        },
    }


def main() -> None:
    rows = load_rows()
    layer = {"type": "FeatureCollection", "features": [to_feature(r) for r in rows]}
    LAYER.parent.mkdir(parents=True, exist_ok=True)
    LAYER.write_text(json.dumps(layer, indent=1) + "\n")
    print(f"wrote {len(rows)} points to {LAYER.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
