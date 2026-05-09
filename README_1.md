# Day Trading Test

This repository includes a helper for creating a local development checkout and Python environment for the canonical `the-aisle` repo.

## Source repository

The setup is locked to this repo only:

```text
https://github.com/seanyofthedead/the-aisle
```

The script will clone from that URL when `the-aisle/` does not exist. If `the-aisle/` already exists, the script verifies that its `origin` points to the same approved repo before running a fast-forward-only pull.

## Create the `the-aisle` environment

From this repository root, run:

```bash
scripts/setup_the_aisle_env.sh
```

By default, the script:

1. clones or updates `./the-aisle` from `https://github.com/seanyofthedead/the-aisle`;
2. creates `./the-aisle/.venv-the-aisle` with the activation prompt `the-aisle`;
3. installs `./the-aisle/requirements.txt` if that file exists in the cloned repo.

Activate the environment with:

```bash
source the-aisle/.venv-the-aisle/bin/activate
```

## Optional paths

You can override the checkout and virtual environment locations without changing the source repository:

```bash
scripts/setup_the_aisle_env.sh /path/to/the-aisle /path/to/the-aisle/.venv-the-aisle
```

The source repository remains locked to `https://github.com/seanyofthedead/the-aisle` even when custom paths are supplied.
