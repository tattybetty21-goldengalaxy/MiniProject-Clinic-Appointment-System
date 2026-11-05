"""
Appointment module for Clinic Appointment System.
                   
"""

from enum import Enum, auto
from typing import Optional
from exceptions import InvalidEntityError, IllegalStateTransitionError, CancellationError
from patient import Patient
from staff import Staff


class AppointmentStatus(Enum):
    PENDING = auto()
    CONFIRMED = auto()
    CANCELLED = auto()

    def __str__(self) -> str:
        return self.name


class Appointment:
    
    def __init__(
        self,
        appointment_id: int,
        patient: Patient,
        staff: Staff,
        start_hour: int,
    ) -> None:
        
        if not isinstance(appointment_id, int) or appointment_id <= 0:
            raise InvalidEntityError(f"Appointment ID must be a positive integer, got {appointment_id!r}")

    
        if not isinstance(start_hour, int) or not (0 <= start_hour <= 168):
            raise InvalidEntityError(f"Start hour must be in range [0, 168], got {start_hour!r}")

    
        if not isinstance(patient, Patient):
            raise InvalidEntityError("Appointment patient must be an instance of Patient")
        if not isinstance(staff, Staff):
            raise InvalidEntityError("Appointment staff must be an instance of Staff")

    
        self.__id: int = appointment_id
        self.__patient: Patient = patient
        self.__staff: Staff = staff
        self.__start_hour: int = start_hour
        self.__status: AppointmentStatus = AppointmentStatus.PENDING
        self.__cancellation_reason: Optional[str] = None

    @property
    def id(self) -> int:
        return self.__id

    @property
    def patient(self) -> Patient:
        return self.__patient

    @property
    def staff(self) -> Staff:
        return self.__staff

    @property
    def start_hour(self) -> int:
        return self.__start_hour

    @property
    def status(self) -> AppointmentStatus:
        return self.__status

    @property
    def cancellation_reason(self) -> Optional[str]:
        return self.__cancellation_reason

    def is_cancelled(self) -> bool:
        return self.__status == AppointmentStatus.CANCELLED

    def is_confirmed(self) -> bool:
        return self.__status == AppointmentStatus.CONFIRMED

    def is_pending(self) -> bool:
        return self.__status == AppointmentStatus.PENDING

    def confirm(self) -> None:
        
        if self.__status == AppointmentStatus.CANCELLED:
            raise IllegalStateTransitionError(
                f"Appointment #{self.__id} is CANCELLED and can never return or be confirmed."
            )
        self.__status = AppointmentStatus.CONFIRMED

    def cancel(self, current_hour: int, reason: str = "") -> None:
        
        
        if self.__status == AppointmentStatus.CANCELLED:
            raise IllegalStateTransitionError(
                f"Appointment #{self.__id} is already CANCELLED and cannot be cancelled again."
            )

        if current_hour >= self.__start_hour:
            raise CancellationError(f"too late: appointment #{self.__id} has already started at hour {self.__start_hour}")

    
        if self.__status == AppointmentStatus.CONFIRMED:
            time_until_start = self.__start_hour - current_hour
            if time_until_start < 2:
                raise CancellationError(
                    f"too late: confirmed appointment #{self.__id} cannot be cancelled less than 2 hours before start (starts at {self.__start_hour}, current is {current_hour})"
                )

        self.__status = AppointmentStatus.CANCELLED
        self.__cancellation_reason = reason or "User requested cancellation"

    def calculate_price(self) -> float:
        
        base_fee = self.__staff.fee()
        return self.__patient.calculate_price(base_fee)

    def __repr__(self) -> str:
        return (
            f"Appointment(id={self.__id}, patient='{self.__patient.name}', "
            f"staff='{self.__staff.name}', hour={self.__start_hour}, status={self.__status.name})"
        )
