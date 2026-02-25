from django.core import checks, exceptions
from django.db import models, transaction
from django.utils import timezone
from ulid import ULID

from luckydash.managers import SoftDeleteManager


class UIDField(models.CharField):
    def __init__(self, prefix, *args, **kwargs):
        self.prefix = prefix
        kwargs.setdefault("db_index", True)
        kwargs.setdefault("auto_created", True)
        kwargs.setdefault("unique", True)
        kwargs.setdefault("editable", False)
        kwargs.setdefault("max_length", 255)
        super(UIDField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(UIDField, self).deconstruct()
        if self.prefix:
            kwargs["prefix"] = self.prefix
        return name, path, args, kwargs

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_prefix())
        return errors

    def _check_prefix(self):
        if not isinstance(self.prefix, str):
            return [
                checks.Error(
                    hint=(
                        "Pass a string or alternatively remove the argument to disable prefixing."
                    ),
                    obj=self,
                    id="UIDField.E001",
                )
            ]
        return []

    def validate(self, value, model_instance):
        if not isinstance(value, str):
            raise exceptions.ValidationError(
                self.error_messages["invalid_type"],
                code="invalid_type",
            )

        if self.prefix and not value.startswith(self.prefix):
            raise exceptions.ValidationError(
                self.error_messages["invalid_prefix"],
                code="invalid_prefix",
                params={"value": value, "prefix": self.prefix},
            )

        return super().validate(value, model_instance)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if add and not value:
            value = f"{self.prefix}_{str(ULID())}"
            setattr(model_instance, self.attname, value)
        return value

    @property
    def non_db_attrs(self):
        return super().non_db_attrs + ("prefix",)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, editable=False)

    objects = SoftDeleteManager()
    raw_objects = models.Manager()

    def __repr__(self):
        return f"<{self.__class__.__name__} {self}>"

    def __str__(self):
        return f"{self.uid}"

    def delete(self):
        if self.deleted_at:
            return

        with transaction.atomic():
            self.deleted_at = timezone.now()
            self.save(update_fields=["updated_at", "deleted_at"])

            for related in self._meta.related_objects:
                if issubclass(related.related_model, BaseModel):
                    related_name = related.get_accessor_name()
                    if related.one_to_many:
                        manager = getattr(self, related_name)
                        manager.all().delete()
                    elif related.one_to_one:
                        try:
                            obj = getattr(self, related_name)
                            obj.delete()
                        except related.related_model.DoesNotExist:
                            pass

    def save_without_signals(self):
        try:
            self._disable_signals = True
            self.save()
        finally:
            self._disable_signals = False
