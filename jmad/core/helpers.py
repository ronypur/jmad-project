import json

from django.core.exceptions import ImproperlyConfigured


def get_secret(setting, source_location, source = 'secrets.json'):
    """ read secrets json file from site root and return it """

    source_path = source_location + '/' + source

    try:
        open(source_path)
    except OSError as err:
        print(err)

    with open(source_path) as f:
        secrets = json.loads(f.read())

    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Set the {} environment variable.'.format(setting)
        raise ImproperlyConfigured(error_msg)



