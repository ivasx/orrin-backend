from django.db import models
from slugify import slugify


class SluggedModel(models.Model):
    """
    Abstract model for storing common data
    """

    class Meta:
        abstract = True

    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')

    slug_source_fields = []

    def generate_slug(self):
        return "-".join(str(getattr(self, field)) for field in self.slug_source_fields)

    def save(self, *args, **kwargs):
        if self.pk:
            old = self.__class__.objects.filter(pk=self.pk).first()
            if old:
                changed = any(getattr(self, field) != getattr(old, field) for field in self.slug_source_fields)
                if changed:
                    self.slug = None

        if not self.slug:
            base_slug = slugify(self.generate_slug())
            slug = base_slug
            num = 1
            while self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{num}'
            num += 1
            self.slug = slug

        super().save(*args, **kwargs)
