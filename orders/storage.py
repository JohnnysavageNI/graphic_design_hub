from django.core.files.storage import FileSystemStorage
from django.conf import settings


class ProtectedStorage(FileSystemStorage):
    def __init__(self, **kwargs):
        kwargs.setdefault("location", str(settings.PROTECTED_MEDIA_ROOT))
        super().__init__(**kwargs)
