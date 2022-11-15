# https://stackoverflow.com/questions/65011159/importerror-cannot-import-name-celery
from celeryapp import app as celeryapp


__all__ = ("celeryapp",)
