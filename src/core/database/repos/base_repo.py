from __future__ import annotations

from abc import ABC
from typing import List, TypeVar, Generic, Type

from django.db import models

T = TypeVar('T', bound=models.Model)


class CRUDMixin(Generic[T]):
    model: Type[T]

    @classmethod
    def scalar(cls, **kwargs) -> T:
        return cls.model.objects.get(**kwargs)

    @classmethod
    def select(cls, **kwargs) -> List[T]:
        return cls.model.objects.filter(**kwargs)

    @staticmethod
    def update(model: T, **fields):
        for fname, fvalue in fields.items():
            setattr(model, fname, fvalue)
        model.save()

    @staticmethod
    def delete(model: T):
        model.delete()

    @classmethod
    def create(cls, **fields) -> T:
        return cls.model.objects.create(**fields)


class BaseRepo(ABC, CRUDMixin[T], Generic[T]):
    model = type(None)
