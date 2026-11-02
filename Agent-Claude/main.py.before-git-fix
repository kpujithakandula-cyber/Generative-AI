
import csv
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup


CSV_FILE = Path("requiredsoftwares.csv")
REPORT_FILE = Path("version_report.csv")

HEADERS = {
    "User-Agent": "SoftwareVersionTrackingAgent/1.0"
}

TIMEOUT = 20


def read_software_list():
    """Read and validate the software list from CSV."""

    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"CSV file not found: {CSV_FILE.resolve()}"
        )

    with CSV_FILE.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)

        required_columns = {"sno", "name", "version", "url"}

        if (
            not reader.fieldnames
            or not required_columns.issubset(reader.fieldnames)
        ):
            raise ValueError(
                "CSV must contain: sno, name, version, url"
            )

        softwares = []

        for row in reader:
            name = (row.get("name") or "").strip()

            if not name:
                continue

            softwares.append({
                "sno": (row.get("sno") or "").strip(),
                "name": name,
                "version": (row.get("version") or "").strip(),
                "url": (row.get("url") or "").strip(),
            })

        return softwares


def get_latest_version(software_name):
    """Fetch the latest stable version from an official source."""

    name = software_name.strip().lower()

    # Python: Official downloads page
    if name == "python":
        url = "https://www.python.org/downloads/"

        response = requests.get(
            url, headers=HEADERS, timeout=TIMEOUT
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        match = re.search(
            r"Download Python\s+(\d+\.\d+\.\d+)",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1), url

        raise ValueError(
            "Could not extract Python's latest version."
        )

    # uv: Official GitHub Releases API
    elif name == "uv":
        url = (
            "https://api.github.com/repos/"
            "astral-sh/uv/releases/latest"
        )

        response = requests.get(
            url, headers=HEADERS, timeout=TIMEOUT
        )
        response.raise_for_status()

        tag = response.json().get("tag_name")

        if not tag:
            raise ValueError("uv release version was not found.")

        return tag.lstrip("v"), url

    # Git for Windows: Official GitHub Releases API
    elif name == "git":
        url = (
            "https://api.github.com/repos/"
            "git-for-windows/git/releases/latest"
        )

        response = requests.get(
            url, headers=HEADERS, timeout=TIMEOUT
        )
        response.raise_for_status()

        tag = response.json().get("tag_name")

        if not tag:
            raise ValueError("Git release version was not found.")

        return tag.lstrip("v"), url

    # Node.js: Official release index
    elif name in ("node.js", "nodejs"):
        url = "https://nodejs.org/dist/index.json"

        response = requests.get(
            url, headers=HEADERS, timeout=TIMEOUT
        )
        response.raise_for_status()

        releases = response.json()

        # Select the highest stable release version.
        stable_versions = []

        for release in releases:
            version = release.get("version", "")

            if release.get("lts") is not False and version:
                if re.fullmatch(r"v\d+\.\d+\.\d+", version):
                    stable_versions.append(version)

        if not stable_versions:
            raise ValueError(
                "No stable Node.js releases were found."
            )

        def version_key(version):
            return tuple(
                int(part) for part in version.lstrip("v").split(".")
            )

        latest = max(stable_versions, key=version_key)

        return latest.lstrip("v"), url

    else:
        raise ValueError(
            f"Unsupported software: {software_name}"
        )


def generate_report(softwares):
    """Fetch the latest version for every software."""

    report = []

    print("\nSoftware Latest Version Report")
    print("=" * 75)

    for software in softwares:
        name = software["name"]

        try:
            latest, source_url = get_latest_version(name)

            result = {
                "name": name,
                "latest_version": latest,
                "source_url": source_url,
                "status": "Success",
            }

        except (requests.RequestException, ValueError, KeyError) as error:
            result = {
                "name": name,
                "latest_version": "",
                "source_url": software["url"],
                "status": f"Failed: {error}",
            }

        report.append(result)

        print(f"\nSoftware: {result['name']}")
        print(
            f"Latest version: "
            f"{result['latest_version'] or 'Unavailable'}"
        )
        print(f"Status: {result['status']}")
        print("-" * 75)

    return report


def save_report(report):
    """Save the results to a CSV file."""

    fieldnames = [
        "name",
        "latest_version",
        "source_url",
        "status",
    ]

    with REPORT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=fieldnames
        )
        writer.writeheader()
        writer.writerows(report)

    print(f"\nReport saved to: {REPORT_FILE.resolve()}")


def main():
    """Run the software version tracking agent."""

    try:
        softwares = read_software_list()

        if not softwares:
            print("No software entries found in the CSV.")
            return

        report = generate_report(softwares)
        save_report(report)

    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"Agent failed: {error}")


if __name__ == "__main__":
    main()
