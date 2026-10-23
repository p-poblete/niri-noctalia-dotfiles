#include <gtk/gtk.h>
#include <gtk4-layer-shell.h>
#include <glib-unix.h>
#include <signal.h>
#include <sys/wait.h>

static GMainLoop *loop;
static GPid child;
static GPtrArray *windows;
static char **command;
static gboolean stop(gpointer data) {
    (void)data;
    if (child > 0) kill(child, SIGTERM);
    g_main_loop_quit(loop);
    return G_SOURCE_REMOVE;
}
static void finished(GPid pid, gint status, gpointer data) {
    (void)status; (void)data;
    g_spawn_close_pid(pid);
    child = 0;
    g_main_loop_quit(loop);
}
static gboolean launch(gpointer data) {
    (void)data;
    GError *error = NULL;
    if (!g_spawn_async(NULL, command, NULL, G_SPAWN_SEARCH_PATH | G_SPAWN_DO_NOT_REAP_CHILD,
                      NULL, NULL, &child, &error)) {
        g_printerr("Fuzzel: %s\n", error->message);
        g_clear_error(&error);
        g_main_loop_quit(loop);
    } else g_child_watch_add(child, finished, NULL);
    return G_SOURCE_REMOVE;
}
static void clicked(GtkGestureClick *gesture, gint presses, gdouble x, gdouble y, gpointer data) {
    (void)gesture; (void)presses; (void)x; (void)y; (void)data;
    stop(NULL);
}
int main(int argc, char **argv) {
    if (argc < 2) return 2;
    command = &argv[1];
    gtk_init();
    if (!gtk_layer_is_supported()) {
        g_printerr("Layer shell unavailable\n");
        return 3;
    }
    loop = g_main_loop_new(NULL, FALSE);
    windows = g_ptr_array_new();
    GtkCssProvider *css = gtk_css_provider_new();
    gtk_css_provider_load_from_string(css,
        "window.ricing-backdrop { background-color: rgba(0,0,0,0.10); box-shadow: none; }");
    GdkDisplay *display = gdk_display_get_default();
    gtk_style_context_add_provider_for_display(display, GTK_STYLE_PROVIDER(css), GTK_STYLE_PROVIDER_PRIORITY_APPLICATION);
    GListModel *monitors = gdk_display_get_monitors(display);
    for (guint i = 0; i < g_list_model_get_n_items(monitors); i++) {
        GdkMonitor *monitor = g_list_model_get_item(monitors, i);
        GtkWindow *window = GTK_WINDOW(gtk_window_new());
        gtk_widget_add_css_class(GTK_WIDGET(window), "ricing-backdrop");
        gtk_layer_init_for_window(window);
        gtk_layer_set_namespace(window, "ricing-fuzzel-backdrop");
        gtk_layer_set_layer(window, GTK_LAYER_SHELL_LAYER_OVERLAY);
        gtk_layer_set_monitor(window, monitor);
        gtk_layer_set_keyboard_mode(window, GTK_LAYER_SHELL_KEYBOARD_MODE_NONE);
        gtk_layer_set_exclusive_zone(window, -1);
        for (int edge = 0; edge < GTK_LAYER_SHELL_EDGE_ENTRY_NUMBER; edge++)
            gtk_layer_set_anchor(window, edge, TRUE);
        GtkGesture *click = gtk_gesture_click_new();
        g_signal_connect(click, "pressed", G_CALLBACK(clicked), NULL);
        gtk_widget_add_controller(GTK_WIDGET(window), GTK_EVENT_CONTROLLER(click));
        gtk_window_present(window);
        g_ptr_array_add(windows, window);
        g_object_unref(monitor);
    }
    /* Map the background first so the subsequently mapped Fuzzel is above it. */
    g_timeout_add(100, launch, NULL);
    g_unix_signal_add(SIGTERM, stop, NULL);
    g_unix_signal_add(SIGINT, stop, NULL);
    g_main_loop_run(loop);
    if (child > 0) {
        kill(child, SIGTERM);
        waitpid(child, NULL, 0);
        g_spawn_close_pid(child);
    }
    for (guint i = 0; i < windows->len; i++) gtk_window_destroy(g_ptr_array_index(windows,i));
    g_ptr_array_unref(windows);
    g_object_unref(css);
    g_main_loop_unref(loop);
    return 0;
}
