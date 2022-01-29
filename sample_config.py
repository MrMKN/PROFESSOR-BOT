import os


class Config(object):
    RemoveBG_API = os.environ.get("RemoveBG_API", "")
