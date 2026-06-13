# Agent instructions for `scikit-hep`

This repository is a **metapackage**. It does not contain application code beyond
a small `skhep` package that provides `show_versions()` and version constants.

## What the repo actually does

- `skhep/__init__.py` exposes `show_versions`, `__version__`, and project URLs.
- `skhep/_show_versions.py` reports Python, scientific, and Scikit-HEP package
  versions using `importlib.metadata`.
- The real payload is `requirements.txt`, the list of pinned/lower-bound
  Scikit-HEP packages the metapackage installs.

## Key files

| File | Purpose |
|------|---------|
| `requirements.txt` | Runtime dependencies and package versions |
| `requirements_current_release.txt` | Upgrade pins used by the “Current releases” job |
| `skhep/_version.py` | Single source of truth for `__version__` |
| `pyproject.toml` | Build config, dynamic deps/version, pytest options |
| `scripts/skhep-info` | CLI helper script (shipped in sdist) |

## Development commands

```bash
# Editable install with test deps
python -m pip install -e .[test]

# Run tests
pytest tests

# Lint / format (uses ruff-format via pre-commit)
pre-commit run -a
```

## Release/version behavior

- Uses **Calendar Versioning** (`YYYY.MM.PATCH`).
- `__version__` is maintained in `skhep/_version.py`; do not add it elsewhere.
- CD builds an sdist + wheel on every push to `main` and publishes only on
  GitHub Releases.

## CI notes

- `ci.yml` tests on Python 3.10–3.13 with `pytest tests` after `pip install .[test]`.
- `current_releases.yml` installs the metapackage then upgrades dependencies to
  the versions listed in `requirements_current_release.txt` to catch upstream
  breakages early.

## When editing this repo

- Keep `requirements.txt` and `requirements_current_release.txt` consistent;
  the latter is the “latest known good” set the CI uses.
- Any new dependency listed in `requirements.txt` must usually also be reported
  in `skhep/_show_versions.py` under `skhep_deps`.
- Tests are minimal; verify `show_versions()` runs without raising and prints
  expected dependency versions.
