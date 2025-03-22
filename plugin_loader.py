import importlib.util
import os

PLUGINS_DIR = os.path.join(os.path.dirname(__file__), "plugins")
loaded_plugins = []

def load_plugins():
    global loaded_plugins
    loaded_plugins = []

    for file in os.listdir(PLUGINS_DIR):
        if file.endswith(".py"):
            path = os.path.join(PLUGINS_DIR, file)
            spec = importlib.util.spec_from_file_location(file[:-3], path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "JudePlugin"):
                loaded_plugins.append(mod.JudePlugin())
    return loaded_plugins