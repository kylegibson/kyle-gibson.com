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
        settings["secret_key"] = path(settings["secret_key_file"]).bytes().strip()
    except IOError:
        try:
            from random import choice
            settings["secret_key"] = ''.join([choice(string.letters + string.digits + string.punctuation) for i in range(50)])
            path(settings["secret_key_file"]).write_bytes(settings["secret_key"])
        except IOError:
            pass
context = {
    "PROJECT_ROOT" : path(__file__).abspath().dirname().dirname()
}
settings = load_yaml_settings(context, "settings/common.yaml")
if "secret_key" not in settings and "secret_key_file" in settings:
    read_write_secret_key_file(settings)
if "pythonpath" in settings:
    sys.path.extend([pp for pp in settings["pythonpath"]])
for key in settings:
    globals()[key.upper()] = settings[key]

