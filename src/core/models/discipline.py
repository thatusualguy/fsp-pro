import uuid

from django.db import models

from src.core.models.enums import DisciplineEnum


class Discipline(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    discipline = models.CharField(
        max_length=100,
        choices=DisciplineEnum.choices,
        verbose_name='Тип дисциплины',
        unique=True,
    )

    def __str__(self):
        return self.discipline

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"
