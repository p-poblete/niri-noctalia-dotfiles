#!/usr/bin/env python3
"""Export only the reviewed ricing files; never copy entire app profiles."""
import argparse
import json
import re
import shutil
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FILES = [
    *[f'.config/niri/{name}' for name in ('config.kdl', 'noctalia.kdl', 'ricing-windows.kdl', 'ricing-shadow.kdl', 'ricing-fuzzel.kdl', 'dconf-profile')],
    *[f'.local/bin/{name}' for name in ('alacritty', 'ricing-fuzzel', 'niri-session-environment', 'niri-gtk-theme-sync', 'niri-alacritty-theme-sync')],
    *[f'.config/niri-session/noctalia/{name}' for name in ('niri.kdl', 'style.css', 'ricing-fuzzel.toml', 'ricing-shadow.toml', 'brave-theme.toml', 'adaptive-icons.toml', 'templates/ricing-fuzzel.ini', 'templates/ricing-shadow.kdl')],
    '.config/niri-session/alacritty/alacritty.toml',
    '.config/niri-session/alacritty/themes/noctalia.toml',
    '.config/niri-session/fuzzel/fuzzel-base.ini',
    '.config/niri-session/fuzzel/ricing-palette.ini',
    *[f'.config/niri-session/gtk-{v}.0/{name}' for v in (3, 4) for name in ('settings.ini', 'gtk.css', 'noctalia.css')],
    *[f'.config/systemd/user/{name}' for name in ('niri-gtk-theme-sync.service', 'niri-alacritty-theme-sync.service', 'niri.service.d/gtk-theme.conf', 'niri.service.d/session-isolation.conf')],
    '.local/share/ricing-fuzzel/backdrop.c',
    *[f'.local/share/noctalia-icon-sync/{name}' for name in ('build-liquid-clear.py', 'glass_material.py', 'activate-liquid-clear.sh', 'DISABLED')],
    *[f'.local/share/ricing-apps/{name}' for name in ('build-brave-graphite.py', 'build-brave-background.py', 'BRAVE-STATIC')],
]


def clean_state(text):
    # Preserve GUI layouts verbatim, remove local identity, media paths and history.
    parsed = tomllib.loads(text)
    sensitive_keys = {'token', 'api_key', 'apikey', 'password', 'secret', 'client_secret',
                      'access_token', 'refresh_token', 'authorization', 'cookie', 'auth_token'}
    def check_keys(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key.lower() in sensitive_keys and child:
                    raise ValueError('Credential-like setting found; review the snapshot allowlist')
                check_keys(child)
        elif isinstance(value, list):
            for child in value:
                check_keys(child)
    check_keys(parsed)
    allowed_roots = {'accessibility', 'backdrop', 'bar', 'desktop_widgets', 'dock',
                     'lockscreen', 'lockscreen_widgets', 'notification', 'plugin_settings',
                     'plugins', 'shell', 'theme', 'widget'}
    # Split on EVERY table, including array tables, without matching leading newlines.
    sections = re.split(r'(?=^[ \t]*\[)', text, flags=re.M)
    kept = []
    for block in sections:
        header = block.strip().splitlines()[0] if block.strip() else ''
        if header.startswith('['):
            root = header.lstrip('[').split('.')[0].rstrip(']')
            if root not in allowed_roots:
                continue
        if header.startswith(('[location]', '[wallpaper', '[[wallpaper', '[[plugins.source]]')):
            continue
        block = re.sub(r'^([ \t]*title = )"scoria"$', r'\1"__USER__"', block, flags=re.M)
        block = re.sub(r'^([ \t]*image_path = ).*$', r'\1""', block, flags=re.M)
        kept.append(block)
    result = ''.join(kept)
    # Third-party stickers are excluded, retained as disabled layout placeholders.
    result = re.sub(r'(^[ \t]*type = "sticker"$)', r'\1\n    enabled = false', result, flags=re.M)
    result += '''\n[wallpaper]
directory = "__HOME__/Imágenes"
transition = ["fade"]
transition_on_startup = true
[wallpaper.default]
path = "__HOME__/Imágenes/Brave-Liquid-Graphite.png"
[[plugins.source]]
kind = "git"
location = "https://github.com/noctalia-dev/official-plugins"
name = "official"
[[plugins.source]]
kind = "git"
location = "https://github.com/noctalia-dev/community-plugins"
name = "community"
'''
    tomllib.loads(result)
    return result


def portable(text, home):
    return text.replace(str(home), '__HOME__')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, default=Path.home())
    args = parser.parse_args()
    home = args.home.resolve()
    payload = REPO / 'home'
    # Only this generated directory is replaced; the live desktop is read-only.
    if payload.exists():
        shutil.rmtree(payload)
    manifest = []
    for name in FILES:
        source = home / name
        text = portable(source.read_text(), home)
        if name.endswith('niri/config.kdl'):
            text = '\n'.join(line for line in text.splitlines() if 'openjarvis-palmadas' not in line) + '\n'
            text = text.replace('spawn-at-startup "noctalia"', 'spawn-at-startup "__HOME__/.local/bin/noctalia"')
        # Use distribution portals: the original custom portal also depends on a local .so.
        text = '\n'.join(
            line.replace(' XDG_DESKTOP_PORTAL_DIR', '') if line.startswith('dbus-update-activation-environment') else line
            for line in text.splitlines()
            if 'XDG_DESKTOP_PORTAL_DIR' not in line or line.startswith('dbus-update-activation-environment')
        ) + '\n'
        # No accidental dependency on Cinnamon's local session profile when stopping Niri.
        text = text.replace('DCONF_PROFILE=__HOME__/.config/session-profiles/cinnamon', 'DCONF_PROFILE=user')
        text = '\n'.join(line.rstrip() for line in text.splitlines()) + '\n'
        target = payload / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        target.chmod(source.stat().st_mode & 0o777)
        manifest.append(name)
    name = '.local/state/noctalia/settings.toml'
    target = payload / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(portable(clean_state((home / name).read_text()), home))
    manifest.append(name)
    # Keep the same source for future palette updates, without carrying obsolete templates.
    (payload / '.config/niri-session/noctalia/apply.sh').write_text('''#!/bin/sh
set -eu
case "${1:-apply}" in
  output) printf '%s\\n' "$HOME/.config/niri/noctalia.kdl" ;;
  apply) : ;; # config.kdl already includes noctalia.kdl
  *) exit 2 ;;
esac
''')
    manifest.append('.config/niri-session/noctalia/apply.sh')
    (payload / manifest[-1]).chmod(0o755)
    # systemd can also look under the alternate XDG_CONFIG_HOME of this session.
    for name in list(manifest):
        if name.startswith('.config/systemd/user/'):
            session_name = name.replace('.config/systemd/', '.config/niri-session/systemd/', 1)
            target = payload / session_name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(payload / name, target)
            manifest.append(session_name)
    REPO.joinpath('manifest.json').write_text(json.dumps(sorted(manifest), indent=2) + '\n')
    extras = REPO / 'extras/obsidian'
    vault = home / 'Documentos/Obsidian Vault/.obsidian'
    for name in ('appearance.json', 'snippets/noctalia.css', 'snippets/segundo-cerebro-colores.css'):
        target = extras / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text((vault / name).read_text())
    # Only visual keys, never VS Code's full settings or account storage.
    (REPO / 'extras/vscode-settings.json').write_text(json.dumps({
        'workbench.colorTheme': 'NoctaliaTheme',
        'editor.fontFamily': "'Ubuntu Sans Mono', monospace",
        'terminal.integrated.fontFamily': 'Ubuntu Sans Mono',
    }, indent=2) + '\n')
    print(f'Exported {len(manifest)} reviewed files into {payload}')


if __name__ == '__main__':
    main()
