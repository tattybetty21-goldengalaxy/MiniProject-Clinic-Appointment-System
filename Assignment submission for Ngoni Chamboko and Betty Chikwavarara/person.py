
# Person base module for Clinic Appointment System.


from abc import ABC, abstractmethod
from typing import Any
from exceptions import InvalidEntityError


class Person(ABC):
    
    _constructor_call_count: int = 0

    @classmethod
    def reset_constructor_counter(cls) -> None:
        
        cls._constructor_call_count = 0

    @classmethod
    def get_constructor_counter(cls) -> int:
        
        return cls._constructor_call_count

    def __init__(self, name: str, person_id: int, **kwargs: Any) -> None:
        
        if not isinstance(name, str) or not name.strip():
            raise InvalidEntityError(f"Person name must be a non-empty string, got {name!r}")

        if not isinstance(person_id, int) or person_id <= 0:
            raise InvalidEntityError(f"Person ID must be a strictly positive integer, got {person_id!r}")

        self._name: str = name.strip()
        self._id: int = person_id

        Person._constructor_call_count += 1

        super().__init__(**kwargs)

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> int:
        return self._id

    @abstractmethod
    def role(self) -> str:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id}, name='{self._name}', role='{self.role()}')"
