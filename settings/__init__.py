import sys
import yaml
import string
from path import path

def load_yaml_settings(context, *paths):
    settings = {}
    for p in paths:
        with open(p) as fd:
            t = string.Template(fd.read())
            y = yaml.load(t.safe_substitute(context))
            settings.update(y)
    return settings
def read_write_secret_key_file(settings):
    try:
        settings["SECRET_KEY"] = path("SECRET_KEY_FILE").bytes().strip()
    except IOError:
        try:
            from random import choice
            settings["SECRET_KEY"] = ''.join([choice(string.letters + string.digits + string.punctuation) for i in range(50)])
            path(settings["SECRET_KEY_FILE"]).write_bytes(settings["SECRET_KEY"])
        except IOError:
            pass
context = {
    "PROJECT_ROOT" : path(__file__).abspath().dirname().dirname()
}
settings = load_yaml_settings(context, "settings/config.yaml")
if "SECRET_KEY" not in settings and "SECRET_KEY_FILE" in settings:
    read_write_secret_key_file(settings)
if "pythonpath" in settings:
    sys.path.extend([pp for pp in settings["pythonpath"]])
for key in settings:
    globals()[key.upper()] = settings[key]

