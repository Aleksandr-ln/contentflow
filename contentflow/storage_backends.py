import os
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = None
    file_overwrite = True
    custom_domain = os.getenv('AWS_S3_CUSTOM_DOMAIN')


class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = None
    file_overwrite = False
    custom_domain = os.getenv('AWS_S3_CUSTOM_DOMAIN')
