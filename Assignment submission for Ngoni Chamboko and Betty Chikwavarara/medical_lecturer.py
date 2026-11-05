
# Lecturer and MedicalLecturer module for Clinic Appointment System.


from typing import Any
from person import Person
from staff import Doctor
from exceptions import InvalidEntityError


class Lecturer(Person):
    
    def __init__(self, name: str, person_id: int, module_name: str, **kwargs: Any) -> None:
        if not isinstance(module_name, str) or not module_name.strip():
            raise InvalidEntityError(f"Module name must be a non-empty string, got {module_name!r}")
        self._module_name: str = module_name.strip()
        
        super().__init__(name=name, person_id=person_id, **kwargs)

    @property
    def module_name(self) -> str:
        return self._module_name

    def role(self) -> str:
        return "Lecturer"


class MedicalLecturer(Doctor, Lecturer):
  
    def __init__(self, name: str, person_id: int, module_name: str, **kwargs: Any) -> None:
        
        super().__init__(name=name, person_id=person_id, module_name=module_name, **kwargs)

    def role(self) -> str:
    
        return "Doctor and Lecturer"

    def fee(self) -> float:
        
        return super().fee()
