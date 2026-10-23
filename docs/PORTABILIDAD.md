# Qué adaptar en otra máquina

- **Usuario y rutas:** el instalador sustituye `__HOME__` y `__USER__`. No presupone `/home/scoria`.
- **Configuración aislada:** Niri utiliza `~/.config/niri-session` como `XDG_CONFIG_HOME`, y el perfil dconf `~/.config/niri/dconf-profile`. Se incluyen las unidades/drop-ins de sincronización en las dos rutas de búsqueda de usuario. El servicio base de Niri y el archivo de sesión deben proceder de su instalación.
- **Pantallas:** los widgets de escritorio y bloqueo mantienen la disposición manual actual y sus referencias de tamaño. Cambia los conectores `eDP-1` / `HDMI-A-1` con el editor. Los widgets que no coincidan con una pantalla no aparecerán.
- **Dock:** el snapshot actual tiene fondo prácticamente opaco, sombra desactivada y magnificación 1.4. Se conservan los valores reales, aunque algunas notas antiguas registraban 0.90, sombra activa y magnificación 1.25. Inactivos: 0.88; iconos: 32 px.
- **Fondos:** el original actual era Wallhaven `yqg2og` (https://wallhaven.cc/w/yqg2og). Por no redistribuir arte ajeno, la réplica usa el fondo grafito de nuestro generador. Puedes elegir el original manualmente y regenerar la paleta; los colores cambiarán con el fondo.
- **Stickers:** sus imágenes personales/ajenas no se suben. Se conserva posición/tamaño y se desactivan; selecciona imágenes propias y actívalos si quieres.
- **Jarvis/palmadas:** se excluyen inicio y atajos de ese proyecto personal. No forma parte del ricing.
- **Portales:** se excluye la variable que fijaba un directorio privado de portales y el parche `.so` local del selector. Se usa la instalación de portales del sistema. El selector podrá tener diferencias visuales respecto al original.
- **Plugins:** se conservan los IDs habilitados y la disposición de la barra, con los dos repositorios oficiales/comunitarios. Se omite la fuente local `mis-plugins`. Revisa su disponibilidad en Ajustes → Plugins y desactiva los que necesiten programas que no hayas instalado. No se guardan sus caches ni datos personales.
- **Aplicaciones compartidas:** no se crean enlaces a perfiles completos de Brave/Code. La apariencia de Obsidian y VS Code se aplica desde `extras/` mediante fusión manual.
- **Seguridad del bloqueo:** la copia conserva el diseño y transición, pero el funcionamiento de autenticación depende de instalar correctamente Noctalia y su integración PAM según su documentación. No se sustituyen archivos de autenticación del sistema.

## Recuperar los archivos previos

Cada ejecución con `--apply` deja un directorio de respaldo y `restore-manifest.json`. Para cada entrada con `previously_existed=true`, restaura el archivo de la misma ruta desde el respaldo; para las entradas con `false`, elimina solo el archivo creado. No borres directorios completos. Hazlo fuera de la sesión Niri si estás restaurando su configuración.
