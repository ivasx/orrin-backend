from django.db import models


class LegalDocument(models.Model):
    """
    Stores a versioned legal document (Terms of Service, Privacy Policy, etc.)
    with per-language support.

    Each language variant is a separate row identified by (doc_type, language).
    Sections are stored as a JSON array:

        [
            { "id": "general", "title": "General Provisions", "content": "..." },
            ...
        ]

    This allows the frontend to render sections without any extra queries.
    """

    DOC_TYPE_CHOICES = (
        ('terms', 'Terms of Service'),
        ('privacy', 'Privacy Policy'),
    )

    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('uk', 'Ukrainian'),
    )

    doc_type = models.CharField(
        max_length=10,
        choices=DOC_TYPE_CHOICES,
        verbose_name='Document type',
    )
    language = models.CharField(
        max_length=5,
        choices=LANGUAGE_CHOICES,
        default='en',
        verbose_name='Language',
    )
    title = models.CharField(max_length=255, verbose_name='Title')
    last_updated = models.DateField(verbose_name='Last updated')
    # Array of { id, title, content }
    sections = models.JSONField(
        default=list,
        verbose_name='Sections',
        help_text='JSON array of { "id", "title", "content" } objects.',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active',
        help_text='Only the active version is served via the API.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('doc_type', 'language')
        ordering = ('doc_type', 'language')
        verbose_name = 'Legal document'
        verbose_name_plural = 'Legal documents'

    def __str__(self):
        return f'{self.get_doc_type_display()} [{self.language.upper()}]'
