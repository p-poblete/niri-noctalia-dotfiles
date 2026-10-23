# Referencias consultadas

Consulta: 2026-10-23.

- Ejemplo de dotfiles Niri + Noctalia con árbol de configuraciones e instalación: https://github.com/ni9aii/niri-dotfiles
- Otro ricing Niri + Noctalia con README y archivos por aplicación: https://github.com/noclueatthis/niri-noctalia-dotfiles
- GNU Stow: organiza paquetes y crea enlaces simbólicos al árbol de destino. https://www.gnu.org/software/stow/manual/stow.html
- Chezmoi: guarda dotfiles en Git, permite plantillas y adapta diferencias entre máquinas. https://www.chezmoi.io/user-guide/setup/ y https://www.chezmoi.io/user-guide/manage-machine-to-machine-differences/
- Noctalia v5 en Niri y efectos de fondo: https://docs.noctalia.dev/noctalia/compositor-settings/niri/

Decisión para este repositorio: guardar configuración seleccionada, scripts fuente y documentación; generar los iconos y el tema de Brave localmente; instalar por copia con respaldo y sustitución de rutas. No se necesita adoptar un gestor de dotfiles adicional, y Noctalia puede seguir escribiendo sus archivos. Git mantiene el historial de snapshots revisados.
