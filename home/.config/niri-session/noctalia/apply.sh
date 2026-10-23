#!/bin/sh
set -eu
case "${1:-apply}" in
  output) printf '%s\n' "$HOME/.config/niri/noctalia.kdl" ;;
  apply) : ;; # config.kdl already includes noctalia.kdl
  *) exit 2 ;;
esac
