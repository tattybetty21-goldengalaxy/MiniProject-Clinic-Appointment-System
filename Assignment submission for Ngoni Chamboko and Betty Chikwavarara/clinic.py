
# Clinic module for Clinic Appointment System.


from typing import Dict, List, Optional, TextIO, Callable
from clock import Clock
from exceptions import (
    ClinicError,
    InvalidEntityError,
    DuplicateIdError,
    SchedulingConflictError,
    CancellationError,
    IllegalStateTransitionError,
)
from person import Person
from patient import Patient
from staff import Staff
from appointment import Appointment, AppointmentStatus
from logger import AppointmentLog


class Clinic:
   

    def __init__(
        self,
        clock: Clock,
        log_stream: Optional[TextIO] = None,
        log_callback: Optional[Callable[[str], None]] = None,
    ) -> None:
        if not isinstance(clock, Clock):
            raise InvalidEntityError("Clinic requires an instance of Clock")

        self.__clock: Clock = clock
        self.__log_stream: Optional[TextIO] = log_stream
        self.__log_callback: Optional[Callable[[str], None]] = log_callback

        
        self.__staff: Dict[int, Staff] = {}
        self.__patients: Dict[int, Patient] = {}
        self.__appointments: List[Appointment] = []
        self.__person_ids: set[int] = set()
        self.__appointment_ids: set[int] = set()

    @property
    def clock(self) -> Clock:
        return self.__clock

    def open_log(self) -> AppointmentLog:
        """Create a fresh context-managed log session."""
        return AppointmentLog(stream=self.__log_stream, callback=self.__log_callback)

    
    def register_staff(self, staff_member: Staff) -> None:
        """Register a healthcare provider. Enforces unique Person ID across clinic."""
        if not isinstance(staff_member, Staff):
            raise InvalidEntityError("Must register an instance of Staff")
        if staff_member.id in self.__person_ids:
            raise DuplicateIdError(f"Person ID {staff_member.id} is already registered in this clinic")

        self.__staff[staff_member.id] = staff_member
        self.__person_ids.add(staff_member.id)

    def register_patient(self, patient: Patient) -> None:
        """Register a patient. Enforces unique Person ID across clinic."""
        if not isinstance(patient, Patient):
            raise InvalidEntityError("Must register an instance of Patient")
        if patient.id in self.__person_ids:
            raise DuplicateIdError(f"Person ID {patient.id} is already registered in this clinic")

        self.__patients[patient.id] = patient
        self.__person_ids.add(patient.id)

    def get_staff(self) -> List[Staff]:
      
        return list(self.__staff.values())

    def get_patients(self) -> List[Patient]:
        return list(self.__patients.values())

    def get_appointments(self) -> List[Appointment]:
        return list(self.__appointments)

    def find_appointment(self, appointment_id: int) -> Optional[Appointment]:
        for appt in self.__appointments:
            if appt.id == appointment_id:
                return appt
        return None

    
    def book_appointment(
        self,
        appointment_id: int,
        patient_id: int,
        staff_id: int,
        start_hour: int,
    ) -> Appointment:
    
        with self.open_log() as log:
            action_desc = f"book #{appointment_id}"

    
            if appointment_id in self.__appointment_ids:
                log.log_failure(action_desc, f"duplicate ID #{appointment_id} already exists")
                raise DuplicateIdError(f"Appointment ID #{appointment_id} already exists in the clinic")

        
            patient = self.__patients.get(patient_id)
            if not patient:
                log.log_failure(action_desc, f"patient ID #{patient_id} not found")
                raise InvalidEntityError(f"Patient with ID {patient_id} is not registered")

        
            staff_member = self.__staff.get(staff_id)
            if not staff_member:
                log.log_failure(action_desc, f"staff ID #{staff_id} not found")
                raise InvalidEntityError(f"Staff member with ID {staff_id} is not registered")

            
            for existing in self.__appointments:
                if not existing.is_cancelled() and existing.start_hour == start_hour:
                    if existing.staff.id == staff_id:
                        log.log_failure(
                            action_desc,
                            f"staff {staff_member.name} already booked at hour {start_hour} (conflict with #{existing.id})"
                        )
                        raise SchedulingConflictError(
                            f"Staff {staff_member.name} has a conflict at hour {start_hour}"
                        )
                    if existing.patient.id == patient_id:
                        log.log_failure(
                            action_desc,
                            f"patient {patient.name} already booked at hour {start_hour} (conflict with #{existing.id})"
                        )
                        raise SchedulingConflictError(
                            f"Patient {patient.name} has a conflict at hour {start_hour}"
                        )

            
            try:
                appt = Appointment(
                    appointment_id=appointment_id,
                    patient=patient,
                    staff=staff_member,
                    start_hour=start_hour,
                )
            except Exception as e:
                log.log_failure(action_desc, str(e))
                raise

        
            self.__appointments.append(appt)
            self.__appointment_ids.add(appointment_id)

            
            price = appt.calculate_price()
            log.log(
                f"BOOKED #{appt.id}: {patient.name} ({patient.role()}) with {staff_member.name} "
                f"({staff_member.role()}) at hour {start_hour}:00 | Base: ${staff_member.fee():.2f}, Final: ${price:.2f}"
            )
            return appt

    def confirm_appointment(self, appointment_id: int) -> None:
        
        with self.open_log() as log:
            action_desc = f"confirm #{appointment_id}"
            appt = self.find_appointment(appointment_id)
            if not appt:
                log.log_failure(action_desc, f"appointment #{appointment_id} not found")
                raise InvalidEntityError(f"Appointment #{appointment_id} not found")

            try:
                appt.confirm()
                log.log(f"CONFIRMED #{appointment_id}: for {appt.patient.name} at hour {appt.start_hour}")
            except IllegalStateTransitionError as e:
                log.log_failure(action_desc, str(e))
                raise

    def cancel_appointment(self, appointment_id: int, reason: str = "") -> None:
        
        
        with self.open_log() as log:
            action_desc = f"cancel #{appointment_id}"
            appt = self.find_appointment(appointment_id)
            if not appt:
                log.log_failure(action_desc, f"appointment #{appointment_id} not found")
                raise InvalidEntityError(f"Appointment #{appointment_id} not found")

            current_hour = self.__clock.now()
            try:
                appt.cancel(current_hour=current_hour, reason=reason)
                log.log(f"CANCELLED #{appointment_id}: at hour {current_hour} ({appt.cancellation_reason})")
            except (CancellationError, IllegalStateTransitionError) as e:
                log.log_failure(action_desc, str(e))
                raise
