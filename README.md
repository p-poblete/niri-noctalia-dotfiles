# Niri + Noctalia · Liquid Clear

Mi ricing para **Linux Mint 22.3**, Niri sobre Wayland y **Noctalia v5.3.0**. Configuraciones seleccionadas, fuentes de los recursos personalizados e instrucciones para volver a montarlo. Idioma y teclado: español.

- Ventanas: gaps de 12 px, esquinas de 14 px, sin borde, sombra que sigue la paleta.
- Animaciones: apertura 240 ms, cierre 180 ms, desplazamiento con resortes.
- Fuzzel con fondo del escritorio desenfocado mientras está abierto.
- Ubuntu Sans y Ubuntu Sans Mono; cursor Yaru 24.
- Iconos Liquid Clear generados desde Mint-Y, sin recoloreado de aplicaciones en Noctalia.
- Dock a la izquierda con autoocultamiento; se conserva el ajuste manual exportado.
- Bloqueo con disposición manual, reloj vertical y fundido de 650 ms; notificaciones adaptables.
- Tema fijo Liquid Clear Graphite para Brave e integración de paleta con GTK y Alacritty.

## Qué contiene

```text
home/           Archivos que se instalarán bajo el directorio personal
extras/         Apariencia de Obsidian y fragmento visual de VS Code
scripts/        Exportación, instalación con respaldo y generación de recursos
docs/           Dependencias, diferencias de máquina y referencias
manifest.json   Lista exacta de archivos instalables
```

No se copian perfiles completos de aplicaciones. La bóveda de Obsidian, cuentas, tokens, historial, claves, plugins descargados, binarios y fondos de terceros quedan fuera. Los stickers conservan su geometría como marcadores desactivados. El fondo predeterminado de la réplica es un grafito generado localmente.

## Replicar

1. Instala las [dependencias y versiones compatibles](docs/DEPENDENCIAS.md). El instalador no instala paquetes del sistema ni Niri/Noctalia.
2. Clona el repositorio y revisa la vista previa:

   ```sh
   git clone https://github.com/p-poblete/niri-noctalia-dotfiles.git
   cd niri-noctalia-dotfiles
   python3 scripts/install.py
   ```

3. Instala los archivos y genera los recursos como tu usuario:

   ```sh
   python3 scripts/install.py --apply
   sh scripts/build-assets.sh
   ```

   Se sustituyen las rutas `__HOME__` y la etiqueta `__USER__` por las tuyas. Cada archivo sustituido se respalda en `~/.local/share/ricing-backups/<fecha>-dotfiles-install/`; `restore-manifest.json` indica qué archivos existían y cuáles se crearon. No se modifica el escritorio de la máquina de origen al preparar este repo.

4. Comprueba la configuración antes de entrar a Niri:

   ```sh
   niri validate --config "$HOME/.config/niri/config.kdl"
   XDG_CONFIG_HOME="$HOME/.config/niri-session" "$HOME/.local/bin/noctalia" config validate
   systemctl --user daemon-reload
   ```

5. Inicia Niri mediante su sesión instalada. Noctalia arranca desde `config.kdl`. Los dos sincronizadores de tema están asociados a `niri.service`; su activación requiere una sesión que use ese servicio. No ejecutes otra instancia de Noctalia si ya está funcionando.

Revisa [los ajustes por máquina](docs/PORTABILIDAD.md): pantallas, plugins, aplicaciones opcionales y fondo original. Los widgets guardan nombres de conectores `eDP-1` y `HDMI-A-1`; en otro equipo hay que adaptarlos con el editor de Noctalia.

## Aplicaciones

- **Brave:** abre `brave://extensions`, activa modo desarrollador y carga `~/.local/share/noctalia/brave-theme`. Para la nueva pestaña elige `~/Imágenes/Brave-Liquid-Graphite.png` en Personalizar. El tema representa cristal mediante imágenes; no refracta el escritorio.
- **Obsidian:** copia o fusiona `extras/obsidian/appearance.json` y sus snippets en `.obsidian` de tu bóveda. Conserva cualquier otro ajuste personal. El snippet `segundo-cerebro-colores` mantiene los colores de carpetas del segundo cerebro. Las notas no forman parte de este repositorio.
- **VS Code:** fusiona `extras/vscode-settings.json` con tus ajustes. El tema `NoctaliaTheme` necesita la integración de Noctalia; no se incluye el perfil de Code.
- **Paleta:** ejecuta `noctalia msg templates-apply` dentro de tu sesión tras configurar las plantillas de aplicaciones. La configuración conserva los IDs de plantillas comunitarias y plugins; se descargan mediante Noctalia y requieren red.

## Actualizar el respaldo

Desde la máquina donde mantienes este ricing:

```sh
python3 scripts/snapshot.py
git diff
git add home extras manifest.json
git commit -m "Actualizar ricing"
git push
```

`snapshot.py` lee una lista explícita de archivos. Reemplaza solo `home/` dentro del repositorio; elimina ubicación, historial de fondos, fuentes locales de plugins y rutas de stickers antes de exportar. Revisa siempre el diff si añades nuevos archivos a esa lista.

## Referencias y validación

Estructura inspirada en repositorios de dotfiles y herramientas habituales: [referencias consultadas](docs/REFERENCIAS.md). El modelo elegido es un árbol equivalente a `$HOME` y un instalador por copia con respaldo; los archivos que Noctalia regenera pueden seguir siendo archivos normales.

La réplica se verifica instalándola en un directorio temporal, comprobando sustitución de rutas, respaldos, TOML/JSON, Niri y Noctalia. Eso no sustituye una prueba visual o de inicio de sesión en otra máquina.
