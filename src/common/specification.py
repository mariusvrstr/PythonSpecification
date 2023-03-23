from typing import Callable
from sqlalchemy.orm import Query
from sqlalchemy.ext.declarative import DeclarativeMeta

class Specification:
    def __init__(self, condition: Callable = None):
        self.condition = condition

    def is_satisfied_by(self, entity) -> bool:
        if self.condition is None:
            return True
        return self.condition(entity)

    def to_sqlalchemy_filter(self, model_class: DeclarativeMeta) -> Callable:
        if self.condition is None:
            return lambda: True
        return lambda: self.condition(model_class)

    def and_specification(self, other: 'Specification') -> 'Specification':
        return Specification(lambda entity: self.is_satisfied_by(entity) and other.is_satisfied_by(entity))

    def or_specification(self, other: 'Specification') -> 'Specification':
        return Specification(lambda entity: self.is_satisfied_by(entity) or other.is_satisfied_by(entity))

    def not_specification(self) -> 'Specification':
        return Specification(lambda entity: not self.is_satisfied_by(entity))


def apply_specification(query: Query, spec: Specification) -> Query:
    model_class = query.column_descriptions[0]['type']
    filter_expr = spec.to_sqlalchemy_filter(model_class)
    return query.filter(filter_expr())
