#!/usr/bin/env bash
# Copy the nossaifd skill into a target repository: scripts/install.sh TARGET [--dry-run] [--source-commit REV]
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for tool in python3 git; do # git --version and python3 run the repository installer
  if ! command -v "$tool" >/dev/null 2>&1; then
    printf 'Missing executable for the installer: %s\n' "$tool" >&2
    exit 1
  fi
done
if ! command -v python3 >/dev/null 2>&1 || ! python3 -c 'import sys; sys.exit(sys.version_info < (3, 11))'; then
  echo 'Required executable: python3 3.11 or later. The checker of the skill needs it.' >&2
fi
exec python3 "$repo_root/scripts/install_package.py" --source "$repo_root" "$@"
