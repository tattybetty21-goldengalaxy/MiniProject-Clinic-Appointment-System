
# Patient module for Clinic Appointment System.

from abc import abstractmethod
from typing import Any
from person import Person


class Patient(Person):
    
    def __init__(self, name: str, person_id: int, **kwargs: Any) -> None:
        super().__init__(name=name, person_id=person_id, **kwargs)

    @abstractmethod
    def discount_rate(self) -> float:
    
        pass

    def calculate_price(self, base_fee: float) -> float:
     
        multiplier = 1.0 - self.discount_rate()
        return round(base_fee * multiplier, 2)

class StudentPatient(Patient):

    def role(self) -> str:
        return "Patient (Student)"

    def discount_rate(self) -> float:
        return 0.50


class StaffMemberPatient(Patient):
    
    def role(self) -> str:
        return "Patient (Staff-Member)"

    def discount_rate(self) -> float:
        return 1.00  


class VisitorPatient(Patient):
    

    def role(self) -> str:
        return "Patient (Visitor)"

    def discount_rate(self) -> float:
        return 0.00  
