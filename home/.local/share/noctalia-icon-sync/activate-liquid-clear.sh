#!/bin/sh
set -eu
export XDG_CONFIG_HOME=__HOME__/.config/niri-session
export DCONF_PROFILE=__HOME__/.config/niri/dconf-profile
gsettings set org.gnome.desktop.interface icon-theme Mint-Y-Liquid-Clear-v1
__HOME__/.local/bin/noctalia msg dock-reload
