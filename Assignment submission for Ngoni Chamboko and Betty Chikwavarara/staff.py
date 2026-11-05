
# Staff hierarchy for Clinic Appointment System.


from abc import abstractmethod
from typing import Any, List
from person import Person

P_VALUE: int = 3


class Staff(Person):

    def __init__(self, name: str, person_id: int, **kwargs: Any) -> None:
        super().__init__(name=name, person_id=person_id, **kwargs)

    @abstractmethod
    def fee(self) -> float:
        pass


class Doctor(Staff):
    
    def role(self) -> str:
        return "Doctor"

    def fee(self) -> float:
        return float(40 + 5 * (P_VALUE % 5))


class Nurse(Staff):
   
    def role(self) -> str:
        return "Nurse"

    def fee(self) -> float:
        return float(10 + (P_VALUE % 3))


class Pharmacist(Staff):
   
    def role(self) -> str:
        return "Pharmacist"

    def fee(self) -> float:
        return 5.0


def print_staff_roster(staff_members: List[Staff]) -> None:
  
    for member in staff_members:
        print(f"{member.role()}: ${member.fee():.2f}")
