import argparse
import csv
import re
import subprocess
from pathlib import Path

import requests
from bs4 import BeautifulSoup


CSV_FILE = Path("requiredsoftwares.csv")
REPORT_FILE = Path("version_report.csv")

HEADERS = {
    "User-Agent": "SoftwareVersionTrackingAgent/1.0"
}
TIMEOUT = 20

NO_AUTHOR = "No author name identified"


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

        return [
            {
                "sno": (row.get("sno") or "").strip(),
                "name": (row.get("name") or "").strip(),
                "version": (row.get("version") or "").strip(),
                "url": (row.get("url") or "").strip(),
            }
            for row in reader
            if (row.get("name") or "").strip()
        ]


def get_author(name: str) -> str:
    """Return an explicitly declared author name from a text file."""

    path = Path(name)

    if not path.is_file():
        return NO_AUTHOR

    supported_extensions = {
        ".py", ".txt", ".md", ".rst", ".csv",
        ".yaml", ".yml", ".json", ".ini", ".cfg",
        ".sh", ".js", ".ts", ".html", ".css", ".toml",
    }

    if path.suffix.lower() not in supported_extensions:
        return NO_AUTHOR

    try:
        content = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError):
        return NO_AUTHOR

    patterns = [
        r'^\s*#\s*Author\s*[:=]\s*(.*?)\s*$',
        r'^\s*//\s*Author\s*[:=]\s*(.*?)\s*$',
        r'^\s*/\*\s*Author\s*[:=]\s*(.*?)\s*\*/\s*$',
        r'^\s*<!--\s*Author\s*[:=]\s*(.*?)\s*-->\s*$',
        r'^\s*Author\s*[:=]\s*(.*?)\s*$',
        r'^\s*__author__\s*=\s*["\']([^"\']+)["\']',
        r'^\s*["\']author["\']\s*:\s*["\']([^"\']+)["\']',
    ]

    for line in content.splitlines():
        for pattern in patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                author = match.group(1).strip().strip('"').strip("'")
                if author:
                    return author

    return NO_AUTHOR

def get_latest_version(software_name):
    """Fetch version information from the configured sources."""

    name = software_name.strip().lower()

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

    elif name == "git":
        url = "https://packages.ubuntu.com/noble/git"

        response = subprocess.run(
            ["apt-cache", "policy", "git"],
            capture_output=True,
            text=True,
            check=True,
            timeout=TIMEOUT,
        )

        match = re.search(
            r"^\s*Candidate:\s*(\S+)",
            response.stdout,
            re.MULTILINE,
        )

        if not match or match.group(1) == "(none)":
            raise ValueError(
                "Git candidate version was not found "
                "in Ubuntu repositories."
            )

        version = match.group(1)
        version = re.sub(r"^\d+:", "", version)
        version = re.sub(r"-[^-]+$", "", version)

        return version, url

    elif name in ("node.js", "nodejs"):
        url = "https://nodejs.org/dist/index.json"
        response = requests.get(
            url, headers=HEADERS, timeout=TIMEOUT
        )
        response.raise_for_status()

        releases = response.json()
        stable_versions = []

        for release in releases:
            version = release.get("version", "")

            if (
                release.get("lts") is not False
                and re.fullmatch(r"v\d+\.\d+\.\d+", version)
            ):
                stable_versions.append(version)

        if not stable_versions:
            raise ValueError(
                "No stable Node.js releases were found."
            )

        def version_key(version):
            return tuple(
                int(part)
                for part in version.lstrip("v").split(".")
            )

        latest = max(stable_versions, key=version_key)
        return latest.lstrip("v"), url

    raise ValueError(f"Unsupported software: {software_name}")


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

        except (
            requests.RequestException,
            ValueError,
            KeyError,
            OSError,
            subprocess.SubprocessError,
        ) as error:
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
    """Save the version report to CSV."""

    fieldnames = [
        "name",
        "latest_version",
        "source_url",
        "status",
    ]

    with REPORT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report)

    print(f"\nReport saved to: {REPORT_FILE.resolve()}")


def main():
    """Run the version tracker or author lookup tool."""

    parser = argparse.ArgumentParser(
        description="Software Version Tracker and Author Tool"
    )
    parser.add_argument(
        "--author",
        metavar="FILE",
        help="Find an explicitly declared author in a text file",
    )
    args = parser.parse_args()

    if args.author:
        print(get_author(args.author))
        return

    softwares = read_software_list()

    if not softwares:
        print("No software entries found in the CSV.")
        return

    report = generate_report(softwares)
    save_report(report)


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"Agent failed: {error}")
