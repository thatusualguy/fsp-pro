from django.db import models


class Region(models.Model):
    REGION_TYPE_CHOICES = [
        ('resp', 'Республика'),
        ('kray', 'Край'),
        ('oblast', 'Область'),
        ('aokrug', 'Автономный округ'),
        ('gorod', 'Город федерального значения'),
    ]

    FEDERAL_DISTRICT_CHOICES = [
        ('central', 'Центральный'),
        ('northwestern', 'Северо-Западный'),
        ('southern', 'Южный'),
        ('north_caucasus', 'Северо-Кавказский'),
        ('volga', 'Приволжский'),
        ('ural', 'Уральский'),
        ('siberian', 'Сибирский'),
        ('far_eastern', 'Дальневосточный'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Название региона")
    federal_district = models.CharField(
        max_length=100,
        choices=FEDERAL_DISTRICT_CHOICES,
        verbose_name="Федеральный округ"
    )
    region_type =models.CharField(
        max_length=100,
        choices=REGION_TYPE_CHOICES,
        verbose_name="Тип региона",
        default='resp'
    )
    timezone = models.CharField(
        max_length=10,
        verbose_name="Часовой пояс",
        help_text="Формат: UTC±X"
    )

    population = models.PositiveIntegerField(verbose_name="Население")
    code = models.CharField(
        max_length=10,
        verbose_name="Код региона",
        help_text="Двухзначный код региона"
    )
