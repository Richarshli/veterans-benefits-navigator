# Maintenance Guide

## Run locally

```bash
python -m http.server 8000
```

## Update source health

```bash
python scripts/update_information.py
```

## Run debugger and tests

```bash
python scripts/automated_debugger.py
python -m unittest discover -s tests
```

Review failed links manually before changing or removing benefit information.
