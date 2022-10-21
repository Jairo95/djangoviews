from collections import OrderedDict

from django.db import models


class Locker(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Casillero'
        verbose_name_plural = 'Casilleros'

    def __str__(self):
        return self.name


class Folder(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    locker = models.ForeignKey(
        'Locker', on_delete=models.CASCADE,
        related_name='folders',
        blank=False, null=False
    )

    class Meta:
        verbose_name = 'Carpeta'
        verbose_name_plural = 'Carpetas'

    def __str__(self):
        return self.name


class Document(models.Model):

    GENERIC = 'GENERIC'
    LEGAL = 'LEGAL'
    PERSONAL = 'PERSONAL'

    DOCUMENT_TYPES = OrderedDict((
        (GENERIC, 'Genericos'),
        (LEGAL, 'Legales'),
        (PERSONAL, 'Personales'),
    ))

    name = models.CharField(max_length=250, blank=False, null=False)
    document_type = models.CharField(
        max_length=25, blank=False, null=False,
        choices=DOCUMENT_TYPES.items(),
        default=GENERIC
    )
    folder = models.ForeignKey(
        'Folder', on_delete=models.CASCADE,
        related_name='documents',
        blank=False, null=False
    )
    source = models.CharField(max_length=1500, blank=True, null=True)

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

    def __str__(self):
        return self.name
