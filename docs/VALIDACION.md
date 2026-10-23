# Validación del snapshot inicial

Fecha: 2026-10-23. Pruebas locales, sin sustituir la configuración activa.

- Instalación de 47 archivos en `/tmp/ricing-replica-check`, con usuario y home distintos.
- Ausencia de rutas originales y marcadores pendientes en los archivos instalados.
- `niri validate` correcto sobre la réplica.
- `noctalia config validate` correcto sobre estado y plantillas de la réplica.
- Validación combinada con `XDG_CONFIG_HOME` y `XDG_STATE_HOME` de la réplica: válida, con 12 advertencias por plugins todavía no descargados en ese destino limpio. Hay que instalarlos/activarlos mediante Noctalia para completar la barra.
- Sintaxis Python, shell, TOML y JSON comprobada.
- Compilación del auxiliar GTK4/Fuzzel correcta con las bibliotecas instaladas.
- Generación del tema Brave Graphite y su fondo correcta en el destino temporal.
- Renderizado de una muestra Liquid Clear correcto. No se repitió la generación de los 185 MB del tema completo.
- Segunda instalación: respaldo de los 47 archivos anteriores idéntico byte a byte.
- Revisión de la selección exportada: sin credenciales conocidas, ubicación personal, historial de fondos, notas ni perfiles de aplicaciones.

Pendiente: prueba visual, autenticación del bloqueo e inicio completo en otra máquina. Instalar la configuración no instala ni garantiza las dependencias del sistema.
