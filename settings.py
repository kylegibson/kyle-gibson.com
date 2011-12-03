import django_settings_yaml
from path import path
context = {
    "PROJECT_ROOT" : path(__file__).abspath().dirname()
}
settings = django_settings_yaml.load(context, ["settings.yaml"])
globals().update(settings)
