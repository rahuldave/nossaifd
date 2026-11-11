"""Print the record of the declaude copy: the commit, the version and the git blob id of each file.

`just declaude-copy` writes it to sources/declaude.json, and tests/test_declaude.py compares the copy with it.
A git blob id is the SHA-1 of "blob <size>\\0" and the bytes, so `just declaude-verify` can compare the
record with the tree of the commit on GitHub. The LICENSE comes from the root of that repository.

The copy changes the files that sources/declaude.patch names. "files" keeps the ids of the files of the
commit, before the patch, and "changed" gives the ids of the changed files after it. With a second argument,
a record of the copy before the patch, the script takes "files" from that record.
"""
import hashlib
import json
from pathlib import Path
import re
import sys

SKILL = Path(__file__).resolve().parents[1] / '.agents/skills/declaude'


def digests():
    found = {}
    for path in sorted(SKILL.rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts and path.name != '.DS_Store':
            data = path.read_bytes()
            found[path.relative_to(SKILL).as_posix()] = hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()
    return found


def version():
    return re.search(r'^  version: (\S+)$', (SKILL / 'SKILL.md').read_text(), re.M).group(1)


if __name__ == '__main__':
    now = digests()
    files = json.loads(Path(sys.argv[2]).read_text())['files'] if len(sys.argv) > 2 else now
    changed = {path: digest for path, digest in now.items() if files.get(path) != digest}
    print(json.dumps({'commit': sys.argv[1], 'version': version(), 'files': files, 'changed': changed}, indent=2))
