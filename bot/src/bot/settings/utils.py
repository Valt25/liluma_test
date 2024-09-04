import os

def get_setting(name: str, default = None, required: bool = False):
    value = os.environ.get(name)
    if value is None and default is not None:
        value = default
    if value is None and required:
        raise Exception(f"setting {name} is required but not provided")
    return value