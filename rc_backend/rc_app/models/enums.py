from enum import StrEnum


class TeamInvitationEnum(StrEnum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"


class CompetitionEnum(StrEnum):
    NEW = 'NEW'
    ON_MODERATION = 'ON_MODERATION'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'


class RoleEnum(StrEnum):
    MEMBER = "MEMBER"
    LEADER = "LEADER"
    ADMIN = "ADMIN"


class JoinRequestEnum(StrEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class BaseStatusEnum(StrEnum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'


class OnModerationStatus(BaseStatusEnum):
    pass


class InviteStatusEnum(BaseStatusEnum):
    pass


class ModerationEnum(BaseStatusEnum):
   pass



