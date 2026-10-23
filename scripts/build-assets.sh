#!/bin/sh
# Run AFTER install.py --apply, as the desktop user. No sudo or downloads.
set -eu
pkg-config --exists gtk4-layer-shell-0 gtk4
python3 -c 'from PIL import Image'
test -d /usr/share/icons/Mint-Y
mkdir -p "$HOME/.local/share/icons" "$HOME/Imágenes"
cc -Wall -Wextra -O2 "$HOME/.local/share/ricing-fuzzel/backdrop.c" \
  -o "$HOME/.local/share/ricing-fuzzel/backdrop" \
  $(pkg-config --cflags --libs gtk4-layer-shell-0 gtk4) \
  -Wl,-rpath,/usr/local/lib/x86_64-linux-gnu
python3 "$HOME/.local/share/noctalia-icon-sync/build-liquid-clear.py"
python3 "$HOME/.local/share/ricing-apps/build-brave-graphite.py"
python3 "$HOME/.local/share/ricing-apps/build-brave-background.py"
python3 "$HOME/.local/bin/ricing-fuzzel" --prepare-only
printf '%s\n' 'Assets generated. Validate Niri and Noctalia before starting the session.'
