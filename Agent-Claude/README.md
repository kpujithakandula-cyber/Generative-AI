# Software Version Tracking Agent

## Overview

This Python application reads software names from `requiredsoftwares.csv`, retrieves their latest versions from configured release sources, and saves the results to `version_report.csv`.

## Prerequisites

- Python
- uv
- Internet connectivity

## Project Files

- `main.py` — Main application logic.
- `requiredsoftwares.csv` — List of software to track.
- `version_report.csv` — Generated version report.
- `pyproject.toml` — Project dependencies and configuration.
- `uv.lock` — Locked dependency versions.

## Input Format

The `requiredsoftwares.csv` file uses these columns:

- `sno` — Serial number.
- `name` — Software name.
- `version` — Optional reference version.
- `url` — Optional software URL.

## Run the Application

From the project directory, execute:

```powershell
uv run main.py
```

## Output

The application displays the lookup results and generates `version_report.csv` with these columns:

- `name`
- `latest_version`
- `source_url`
- `status`

## Currently Supported Software

- Python
- uv
- Git for Windows
- Node.js

## Notes

The application requires internet access to retrieve release information. A successful lookup means a version was retrieved; it does not independently guarantee that the version is the newest release.
