from typing import Iterable

from api_builder.schema.abc import FieldABC
from api_builder.schema.extras import empty, Levels
from api_builder.schema.exceptions import ValidationError
from api_builder.schema.typing_mapping import types_to_fields


class SchemaMeta(type):
    def __new__(mcs, name, bases, attrs):
        instance = super(SchemaMeta, mcs).__new__(mcs, name, bases, attrs)
        instance._parent = None
        instance._fields = {
            **{k: v for k, v in attrs.items() if isinstance(v, FieldABC)},
            **types_to_fields(attrs.get('__annotations__', {})),
        }
        instance._before = [
            item.__name__
            for item in sorted(
                (v for v in attrs.values() if hasattr(v, '__vang_before__')),
                key=lambda x: x.__vang_before__,
            )
        ]
        instance._after = [
            item.__name__
            for item in sorted(
                (v for v in attrs.values() if hasattr(v, '__vang_after__')),
                key=lambda x: x.__vang_after__,
            )
        ]
        return instance


class Schema(metaclass=SchemaMeta):
    def __init__(
        self,
        *,
        exclude: Iterable[str] = (),
        only: Iterable[str] = (),
        level: Levels = Levels.MEDIUM,
        **_
    ):
        only = set(only or self._fields.keys())
        self._fields = {
            k: prepare_field(v, self)
            for k, v in self._fields.items()
            if k not in exclude and k in only
        }
        self.level = level

    def validate(self, data: dict):

        if self._parent is None:
            for before_func in self._before:
                data = getattr(self, before_func)(data)

        error = None
        result = {}

        for k, v in self._fields.items():
            try:
                value = v.validate(k, data)
            except ValidationError as ve:
                if self.level == Levels.LOW:
                    raise ValidationError(msg={ve.key: ve.msg})
                if error is None:
                    error = ValidationError()
                error.msg[ve.key] = ve.msg
            else:
                if error is None and value is not empty:
                    result[k] = v.validate(k, data)
        if error:
            raise ValidationError(error.msg, error.key)

        if self._parent is None:
            for after_func in self._after:
                result = getattr(self, after_func)(result)

        return result


def prepare_field(child: FieldABC, parent: Schema):
    child._parent = parent
    child.init()
    return child
