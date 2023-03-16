
from abc import abstractmethod
from typing import List
from pydantic import BaseModel

class Specification(BaseModel):

    def __and__(self, other):
        return AndSpecification(self, other)

    def __or__(self, other):
        return OrSpecification(self, other)

    def __invert__(self):
        return NotSpecification(self)
    
    @abstractmethod
    def is_satisfied_by(self, item):
        pass

class AndSpecification(Specification):
    specs = []
    
    def __init__(self, *specs:Specification):        
        for spec in specs:
            self.specs.append(spec)

    def is_satisfied_by(self, item):
        return all(self.specs.is_satisfied_by(item) for spec in self.specs)

class OrSpecification(Specification):
    specs = []
    
    def __init__(self, *specs:Specification):
        for spec in specs:
            self.specs.append(spec)

    def is_satisfied_by(self, item):
        return any(self.specs.is_satisfied_by(item) for spec in self.specs)

class NotSpecification(Specification):
    spec:List[Specification] = None
    
    def __init__(self, spec:Specification):
        self.spec = spec

    def is_satisfied_by(self, item):
        return self.spec.is_satisfied_by(item)