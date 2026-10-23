#!/usr/bin/env python3
"""Preview by default; --apply installs files with a timestamped backup."""
import argparse
import datetime
import getpass
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, default=Path.home())
    parser.add_argument('--user', default=getpass.getuser())
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    target = args.target.resolve()
    if any(c in str(target) + args.user for c in ('"', "'", '\\', '\n', '\r')):
        parser.error('Home/user must not contain quotes, backslashes or line breaks')
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup = target / '.local/share/ricing-backups' / (stamp + '-dotfiles-install')
    files = json.loads((ROOT / 'manifest.json').read_text())
    plan = []
    for name in files:
        rel = Path(name)
        if rel.is_absolute() or '..' in rel.parts:
            raise ValueError(f'Unsafe manifest path: {name}')
        source = ROOT / 'home' / rel
        destination = target / rel
        if not destination.parent.resolve().is_relative_to(target):
            raise ValueError(f'Destination parent points outside target: {name}')
        data = source.read_text().replace('__HOME__', str(target)).replace('__USER__', args.user)
        if '__HOME__' in data or '__USER__' in data:
            raise ValueError(f'Unresolved placeholder in {name}')
        plan.append((source, destination, data, name))
    records = []
    for source, destination, data, name in plan:
        exists = os.path.lexists(destination)
        print(('REPLACE ' if exists else 'CREATE  ') + name)
        if not args.apply:
            continue
        backup.mkdir(parents=True, exist_ok=True)
        if exists:
            saved = backup / name
            saved.parent.mkdir(parents=True, exist_ok=True)
            if destination.is_dir() and not destination.is_symlink():
                raise ValueError(f'Expected a file, found directory: {destination}')
            shutil.copy2(destination, saved, follow_symlinks=False)
            destination.unlink()
        records.append({'path': name, 'previously_existed': exists})
        # Update the recovery record before writing each destination.
        (backup / 'restore-manifest.json').write_text(json.dumps(records, indent=2) + '\n')
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(data)
        destination.chmod(source.stat().st_mode & 0o777)
    if args.apply:
        print(f'Backup and recovery manifest: {backup}')
        print('Next: install dependencies, run scripts/build-assets.sh, validate, then log in to Niri.')
    else:
        print('Preview only. Add --apply to install; existing files will be backed up.')


if __name__ == '__main__':
    main()
