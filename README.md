# ward-wise-measure-template

A starter repo for adding a measure to [Ward Wise](https://www.wardwise.org). You compute a fine
layer (points, a raster, or values on census tracts) and describe it in `aggregation_spec.json`.
Penlight reads that folder and aggregates your measure to every ward, community area and grid cell
it holds. You never need access to anything of Penlight's.

The example here counts **12 made-up sample points** per square kilometre. Every point is labelled
`SAMPLE … (made up)` and carries `"sample": true`. None of them is a real place. Replace them.

The full contract is [CONTRACT.md](https://github.com/ward-wise/ward-wise-measures/blob/main/CONTRACT.md)
and the long-form guide is
[ADDING_A_MEASURE.md](https://github.com/ward-wise/ward-wise-measures/blob/main/ADDING_A_MEASURE.md).

## What's here

| Path | What it is |
|---|---|
| `data/raw/sample_sites.csv` | the made-up input. Yours might be a download, a scrape, or nothing (fetched in `build.py`). |
| `build.py` | turns the raw input into the published layer. The one script you rewrite. |
| `data/layers/aggregation_spec.json` | the byop/v1 spec: the layer and one metric, with label, description, methodology, unit, direction and nominator. |
| `data/layers/sample_sites.geojson` | the points layer `build.py` writes. Every file in `data/layers/` is published. |
| `.github/workflows/validate.yml` | runs `byop validate` on every push. |
| `.github/workflows/publish.yml` | on a `v*` tag, validates and attaches `data/layers/` to a GitHub Release. |

## Checklist

Copy this into your first issue or pull request and tick it off.

- [ ] **Ticket:** this measure answers `ward-wise/ideas#N`. Put the link in your repo description too.
- [ ] Click **Use this template** on GitHub and create your repo (public). Name it after the measure, e.g. `sunscore`.
- [ ] In `aggregation_spec.json`, set `source` (short slug, `a-z 0-9 _ -`) and `source_url` (your repo).
- [ ] Delete `caveat` once nothing in the layer is a placeholder. Keep `synthetic_estimate: true` and a `caveat` if your values are modeled.
- [ ] Rewrite `build.py` so it produces your layer, and run it: `python build.py`.
- [ ] Rewrite the metric: `label` (1–3 words), `description` (one sentence a resident understands), `methodology` (1–3 sentences with the data source and date), `unit`, `direction`, `category`.
- [ ] If residents reasonably disagree which way is better, add `"direction_contested": true` and say both readings in `methodology`.
- [ ] Put your name and ward in `nominator`, or delete it.
- [ ] Validate locally (below) until it prints `ok:`.
- [ ] Tag and push a release (below). Check the Actions run and copy the sha256 pins from its summary.
- [ ] Open a pull request to [ward-wise/ward-wise-measures](https://github.com/ward-wise/ward-wise-measures) adding your entry to `measures.json`. Link the ideas ticket in the PR.

## Validate

```bash
python -m venv .venv && source .venv/bin/activate
pip install git+https://github.com/HarryBrisson/ward-wise-measures
byop validate data/layers
```

It checks the schema, that every file exists and parses, and that the fields each metric names exist
on the layer. With this template unchanged it prints:

```
ok: measure-template — 1 metrics over 1 layers
```

## Publish

```bash
git tag v2026.11.10
git push --tags
```

The `publish` workflow validates again, creates the release, uploads every file in `data/layers/`,
and prints a `sha256` for each one in the run summary.

If your layers are too big to commit, build them on your machine and publish from there instead:

```bash
byop publish data/layers --repo you/your-measure --tag v2026.11.10 --targets ward,community_area,chi --dry-run
byop publish data/layers --repo you/your-measure --tag v2026.11.10 --targets ward,community_area,chi
```

## Add it to measures.json

`byop publish --dry-run` prints the entry for you. Paste it into `measures.json` in
ward-wise-measures and open a pull request:

```json
{
  "name": "measure-template",
  "repo": "you/your-measure",
  "tag": "v2026.11.10",
  "assets": {
    "aggregation_spec.json": "sha256:…",
    "sample_sites.geojson": "sha256:…"
  },
  "targets": ["ward", "community_area", "chi"],
  "confidence": "low"
}
```

`confidence` is `high`, `medium` or `low`. Modeled estimates are `low` with
`"allocation_method": "modeled_synthetic_sae"`. CI checks the pins against your release; a
maintainer merges, and the next pipeline run puts your measure on the map with your methodology and
your name.

## Rules

- **No keys or credentials in this repo, ever.** Read them from environment variables in `build.py`
  and from repository secrets in workflows. `.env` and `creds.json` are in `.gitignore` for that reason.
- Everything in `data/layers/` is public once you tag. Don't put personal data there; publish a
  documented sample if the full layer is sensitive or huge.
