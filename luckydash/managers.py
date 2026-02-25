from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        self.update(deleted_at=timezone.now())


class SoftDeleteManager(models.Manager):
    _queryset_class = SoftDeleteQuerySet

    def get_queryset(self):
        kwargs = {"model": self.model, "using": self.db}
        return self._queryset_class(**kwargs).filter(deleted_at__isnull=True)

    def soft_delete(self):
        return super().get_queryset().filter(deleted_at__isnull=False)
