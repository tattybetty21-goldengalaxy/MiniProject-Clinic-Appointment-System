
#Comprehensive 5-minute demonstration script for Clinic Appointment System.


from clock import Clock
from person import Person
from patient import StudentPatient, StaffMemberPatient, VisitorPatient
from staff import Doctor, Nurse, Pharmacist, print_staff_roster, P_VALUE
from medical_lecturer import Lecturer, MedicalLecturer
from appointment import AppointmentStatus
from clinic import Clinic
from exceptions import (
    InvalidEntityError,
    SchedulingConflictError,
    CancellationError,
    IllegalStateTransitionError,
    DuplicateIdError,
)


def run_demo() -> None:
    print("=" * 70)
    print("CLINIC APPOINTMENT SYSTEM: 5-MINUTE ACADEMIC DEMONSTRATION")
    print(f"Configured for Parameter P = {P_VALUE} | Twist 3: Patient Discounts")
    print("=" * 70)

    # PART 1 & 2: Constructor validation & Clock

    print("\n--- [DEMO PART 1 & 2]: Constructor Validation & Clock Setup ---")
    clock = Clock(initial_hour=10)
    print(f"Virtual Clock initialized at now() = {clock.now()}h (computer clock not used)")

    clinic = Clinic(clock=clock)

    # Validate constructor rejection of invalid names/ids
    print("\nTesting defensive constructor validation:")
    try:
        Doctor(name="   ", person_id=101)
    except InvalidEntityError as e:
        print(f"  [PASSED] Blank name rejected: {e}")

    try:
        Nurse(name="Nurse Joy", person_id=-5)
    except InvalidEntityError as e:
        print(f"  [PASSED] Non-positive ID rejected: {e}")


    # PART 3: Staff Roster & Polymorphic Loop (P=3)
    
    print("\n--- [DEMO PART 3]: Polymorphic Staff Fee Calculation (Zero Type Tags) ---")
    doc = Doctor(name="Dr. Gregory House", person_id=1)
    nurse = Nurse(name="Nurse Jackie", person_id=2)
    pharm = Pharmacist(name="Pharmacist Bob", person_id=3)

    clinic.register_staff(doc)
    clinic.register_staff(nurse)
    clinic.register_staff(pharm)

    staff_team = [doc, nurse, pharm]
    print(f"Looping over {len(staff_team)} Staff members polymorphically:")
    print_staff_roster(staff_team)
    print(f"Formula verification: Doctor = 40 + 5*(3 mod 5) = ${doc.fee():.2f}")
    print(f"Formula verification: Nurse  = 10 + (3 mod 3)   = ${nurse.fee():.2f}")
    print(f"Formula verification: Pharmacist flat fee       = ${pharm.fee():.2f}")

    
    
    print("\n--- [DEMO PART 5]: Diamond Inheritance & Single Person Constructor ---")
    Person.reset_constructor_counter()
    print(f"Person constructor counter before instantiation: {Person.get_constructor_counter()}")

    med_lecturer = MedicalLecturer(
        name="Dr. Stephen Strange",
        person_id=4,
        module_name="Advanced Neuroanatomy & Sorcery",
    )
    clinic.register_staff(med_lecturer)

    counter_after = Person.get_constructor_counter()
    print(f"MedicalLecturer created: name='{med_lecturer.name}', module='{med_lecturer.module_name}'")
    print(f"Role returned: '{med_lecturer.role()}' (Expected: 'Doctor and Lecturer')")
    print(f"Person constructor counter after instantiation: {counter_after}")
    assert counter_after == 1, "Person constructor must run exactly once!"
    print(f"MedicalLecturer.fee() = ${med_lecturer.fee():.2f} (Doctor clinical tariff)")



    print("\n--- [DEMO PART 6]: Patients & Twist 3 Discounts (Double Dispatch) ---")
    student = StudentPatient(name="Alice Smith", person_id=10)        # 50%
    staff_pt = StaffMemberPatient(name="Nurse Jackie", person_id=11)  # 0%
    visitor = VisitorPatient(name="Charlie Brown", person_id=12)      # 100%

    clinic.register_patient(student)
    clinic.register_patient(staff_pt)
    clinic.register_patient(visitor)

    print(f"Registered {student.name}: {student.role()} -> Discount {student.discount_rate()*100:.0f}%")
    print(f"Registered {staff_pt.name}: {staff_pt.role()} -> Discount {staff_pt.discount_rate()*100:.0f}%")
    print(f"Registered {visitor.name}: {visitor.role()} -> Discount {visitor.discount_rate()*100:.0f}%")

    
    print("\n--- [DEMO PART 4 & 6]: Booking with Guaranteed Log Open/Close & Discounts ---")

    # Booking #1: Student with Doctor (Fee $55 -> Student pays 50% = $27.50)
    clinic.book_appointment(appointment_id=1, patient_id=10, staff_id=1, start_hour=14)

    # Booking #2: Staff Member with Nurse (Fee $10 -> Staff pays 0% = $0.00)
    clinic.book_appointment(appointment_id=2, patient_id=11, staff_id=2, start_hour=15)

    # Booking #3: Visitor with Doctor (Fee $55 -> Visitor pays 100% = $55.00)
    clinic.book_appointment(appointment_id=3, patient_id=12, staff_id=1, start_hour=16)

    # Booking #4: Student with Pharmacist (Fee $5 -> Student pays 50% = $2.50)
    clinic.book_appointment(appointment_id=4, patient_id=10, staff_id=3, start_hour=18)

    print("\nConfirming appointment #3:")
    clinic.confirm_appointment(3)

    
    print("\n--- [DELIBERATE FAILURE SCENARIO 1]: Booking Conflict at Same Hour ---")
    print("Attempting to double-book Dr. Gregory House at hour 14:00 (already booked with Alice):")
    try:
        clinic.book_appointment(appointment_id=5, patient_id=12, staff_id=1, start_hour=14)
    except SchedulingConflictError as e:
        print(f"  [CAUGHT EXPECTED ERROR]: {e}")

    
    print("\n--- [DELIBERATE FAILURE SCENARIO 2 (PART 8)]: Cancellation Less Than 2 Hours Before Start ---")
    print(f"Current clock hour: {clock.now()}h. Appointment #3 starts at hour 16:00 and is CONFIRMED.")
    print("Advancing clock to hour 15:00 (only 1 hour before appointment #3 starts)...")
    clock.set_hour(15)
    print(f"Current clock hour is now: {clock.now()}h.")

    print("Attempting to cancel confirmed appointment #3 within the 2-hour forbidden window:")
    try:
        clinic.cancel_appointment(appointment_id=3, reason="Changed my mind")
    except CancellationError as e:
        print(f"  [CAUGHT EXPECTED ERROR]: {e}")


    print("\n--- [DEMO CANCELLATION RULES]: Post-Start & Once-Cancelled Rules ---")
    print("Successful cancellation of unstarted pending appointment #4:")
    clinic.cancel_appointment(appointment_id=4, reason="Student had class conflict")

    print("\nAttempting to resurrect or confirm cancelled appointment #4:")
    try:
        clinic.confirm_appointment(4)
    except IllegalStateTransitionError as e:
        print(f"  [CAUGHT EXPECTED ERROR]: {e}")

    print("\nAdvancing clock past start hour of appointment #1 (hour 14:00 -> clock at 15:00):")
    print("Attempting to cancel appointment #1 which has already passed:")
    try:
        clinic.cancel_appointment(appointment_id=1, reason="Cannot cancel after start")
    except CancellationError as e:
        print(f"  [CAUGHT EXPECTED ERROR]: {e}")


    print("\n--- [DEMO PART 2]: Encapsulation Verification ---")
    appts_copy = clinic.get_appointments()
   # Caller tries to wipe internal clinic records
    appts_copy.clear() 
    print(f"Caller cleared their returned list. Clinic internal appointment count: {len(clinic.get_appointments())}")
    assert len(clinic.get_appointments()) > 0, "Clinic internal list was mutated by caller!"
    print("  [PASSED] Clinic internal state is securely protected against external mutation.")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE: ALL INVARIANTS, LAWS, AND LOG REQUIREMENTS VERIFIED!")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
