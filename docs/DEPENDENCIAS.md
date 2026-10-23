# Dependencias

Base verificada: Linux Mint 22.3 / Ubuntu noble, Python 3.12, Wayland. No es un instalador de sistema completo.

## Componentes principales

| Componente | Versión de origen | Instalación/referencia |
| --- | --- | --- |
| Niri | `26.04 (v26.04-31-g6f1a2c5f)` | https://github.com/niri-wm/niri — necesita blur/background-effect y noise/saturation compatibles |
| Noctalia | `v5.3.0` | https://github.com/noctalia-dev/noctalia — binario nativo v5, no la edición legacy v4/Quickshell |
| Alacritty | `0.13.2` | Paquete `alacritty` |
| Fuzzel | `1.9.2` | Paquete `fuzzel` |
| Mint-Y | `mint-y-icons 1.9.1` | Base del generador Liquid Clear |
| Fuentes | `fonts-ubuntu 0.869+git20240321` | Ubuntu Sans, Sans Mono y Ubuntu Mono |
| GTK4 | `4.14.5` | GTK4 + GTK4 layer shell para el auxiliar Fuzzel |

El checkout local de Noctalia al exportar era `1d17e1d1f543c97952d1260f571ba40699a27c1d`; la versión del ejecutable instalado es la referencia de funcionamiento. No se incluyen ejecutables compilados.

Los atajos y scripts esperan el ejecutable Noctalia en `~/.local/bin/noctalia`. Al instalarlo, coloca allí el binario o un enlace a su ubicación real. El servicio base de Niri debe apuntar a la ubicación donde lo hayas instalado.

## Paquetes de usuario y compilación

En Mint/Ubuntu, revisa e instala con el gestor de paquetes:

```text
git python3 python3-pil python3-gi python3-cairo
build-essential pkg-config libgtk-4-dev
alacritty fuzzel mint-y-icons fonts-ubuntu yaru-theme-icon
dconf-cli libglib2.0-bin libgtk-3-bin
xdg-desktop-portal xdg-desktop-portal-gnome xdg-desktop-portal-gtk
pipewire wireplumber playerctl brightnessctl
nemo xwayland kdeconnect
```

También necesitas **gtk4-layer-shell** con cabeceras y archivo pkg-config `gtk4-layer-shell-0`. Su nombre/disponibilidad depende de la distribución; en el equipo original está instalado fuera de los paquetes consultados. Fuente e instrucciones: https://github.com/wmww/gtk4-layer-shell. Compruébalo con:

```sh
pkg-config --modversion gtk4-layer-shell-0 gtk4
```

El tema GTK `adw-gtk3` y `adw-gtk3-dark` debe estar disponible: https://github.com/lassekongo83/adw-gtk3. Niri y Noctalia se instalan siguiendo sus instrucciones oficiales y deben proporcionar la sesión y el servicio `niri.service`.

No se intenta instalar ni sustituir componentes del sistema automáticamente. Las integraciones opcionales pueden necesitar mpvpaper, herramientas OCR, wvkbd, CodexBar y Obsidian Flatpak (`md.obsidian.Obsidian`). Desactiva los widgets/plugins que no uses.

Los iconos se generan desde `/usr/share/icons/Mint-Y`; el generador conserva la atribución de `/usr/share/doc/mint-y-icons/copyright`. Los recursos originales de terceros no se redistribuyen aquí.
