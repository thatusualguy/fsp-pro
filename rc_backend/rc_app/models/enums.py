from django.db import models


class TeamInvitationEnum(models.TextChoices):
    PENDING = "PENDING", "На модерации"
    APPROVED = "APPROVED", 'Принято'
    REJECTED = "REJECTED", 'Отказать'


class CompetitionEnum(models.TextChoices):
    NEW = 'NEW', "Новая"
    ON_MODERATION = 'ON_MODERATION', "На модерации"
    ACCEPTED = 'ACCEPTED', "Принято"
    REJECTED = 'REJECTED', "Отказать"


class JoinRequestEnum(models.TextChoices):
    PENDING = "PENDING", "На модерации"
    APPROVED = "APPROVED", 'Принято'
    REJECTED = "REJECTED", 'Отказать'


class BaseStatusEnum(models.TextChoices):
    PENDING = "PENDING", "На модерации"
    APPROVED = "APPROVED", 'Принято'
    REJECTED = "REJECTED", 'Отказать'



class OnModerationStatus(models.TextChoices):
    PENDING = "PENDING", "На модерации"
    APPROVED = "APPROVED", 'Принято'
    REJECTED = "REJECTED", 'Отказать'


class InviteStatusEnum(models.TextChoices):
    PENDING = "PENDING", "На модерации"
    APPROVED = "APPROVED", 'Принято'
    REJECTED = "REJECTED", 'Отказать'


class ModerationEnum(models.TextChoices):
    PENDING = "PENDING", "На модерации"
    APPROVED = "APPROVED", 'Принято'
    REJECTED = "REJECTED", 'Отказать'
