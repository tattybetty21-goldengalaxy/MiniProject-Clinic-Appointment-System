
#Unit test suite for Clinic Appointment System.

import unittest
from clock import Clock
from person import Person
from patient import StudentPatient, StaffMemberPatient, VisitorPatient
from staff import Doctor, Nurse, Pharmacist
from medical_lecturer import Lecturer, MedicalLecturer
from appointment import Appointment, AppointmentStatus
from clinic import Clinic
from exceptions import (
    InvalidEntityError,
    DuplicateIdError,
    SchedulingConflictError,
    CancellationError,
    IllegalStateTransitionError,
)


class TestClinicAppointmentSystem(unittest.TestCase):

    def setUp(self) -> None:
        self.clock = Clock(initial_hour=10)
        self.clinic = Clinic(clock=self.clock)
        Person.reset_constructor_counter()


    def test_person_validation(self):
        
        with self.assertRaises(InvalidEntityError):
            Doctor(name="", person_id=1)
        with self.assertRaises(InvalidEntityError):
            Doctor(name="   ", person_id=1)
        with self.assertRaises(InvalidEntityError):
            Doctor(name="Dr. Valid", person_id=0)
        with self.assertRaises(InvalidEntityError):
            Doctor(name="Dr. Valid", person_id=-10)

    def test_clock_hours(self):
        
        c = Clock(0)
        self.assertEqual(c.now(), 0)
        c.advance(5)
        self.assertEqual(c.now(), 5)
        with self.assertRaises(ValueError):
            Clock(-1)
        with self.assertRaises(ValueError):
            Clock(169)
        with self.assertRaises(ValueError):
            c.advance(200)

    def test_staff_fees_p3(self):
        
        doc = Doctor("Dr. A", 1)
        nurse = Nurse("Nurse B", 2)
        pharm = Pharmacist("Pharm C", 3)
        self.assertEqual(doc.fee(), 55.0)
        self.assertEqual(nurse.fee(), 10.0)
        self.assertEqual(pharm.fee(), 5.0)

   
    def test_log_open_close_guarantee(self):
    
        doc = Doctor("Dr. A", 1)
        self.clinic.register_staff(doc)
        patient = StudentPatient("Alice", 10)
        self.clinic.register_patient(patient)

        
        with self.assertRaises(InvalidEntityError):
            self.clinic.book_appointment(1, 10, 1, 200)

    def test_medical_lecturer_diamond(self):
       
        Person.reset_constructor_counter()
        med_lec = MedicalLecturer("Dr. Smith", 5, "Cardiology 301")
        self.assertEqual(Person.get_constructor_counter(), 1)
        self.assertEqual(med_lec.role(), "Doctor and Lecturer")
        self.assertEqual(med_lec.fee(), 55.0)

    def test_twist3_discounts(self):
        
        doc = Doctor("Dr. A", 1)
        self.clinic.register_staff(doc)

        student = StudentPatient("Alice", 10)
        staff_pt = StaffMemberPatient("Bob", 11)
        visitor = VisitorPatient("Charlie", 12)

        self.clinic.register_patient(student)
        self.clinic.register_patient(staff_pt)
        self.clinic.register_patient(visitor)

        # Base fee $55.00
        a1 = self.clinic.book_appointment(1, 10, 1, 14)  # = 50% 
        a2 = self.clinic.book_appointment(2, 11, 1, 15)  # = 0% 
        a3 = self.clinic.book_appointment(3, 12, 1, 16)  # = 100% 

        self.assertEqual(a1.calculate_price(), 27.50)
        self.assertEqual(a2.calculate_price(), 0.00)
        self.assertEqual(a3.calculate_price(), 55.00)

    def test_conflict_prevention(self):
        
        doc1 = Doctor("Dr. A", 1)
        doc2 = Doctor("Dr. B", 2)
        self.clinic.register_staff(doc1)
        self.clinic.register_staff(doc2)

        p1 = StudentPatient("Alice", 10)
        p2 = StudentPatient("Bob", 11)
        self.clinic.register_patient(p1)
        self.clinic.register_patient(p2)

        # p1 with doc1 at hour 14
        self.clinic.book_appointment(1, 10, 1, 14)

        # doc1 with p2 at hour 14 (staff conflict)
        with self.assertRaises(SchedulingConflictError):
            self.clinic.book_appointment(2, 11, 1, 14)

        # p1 with doc2 at hour 14 (patient conflict)
        with self.assertRaises(SchedulingConflictError):
            self.clinic.book_appointment(3, 10, 2, 14)

    def test_cancellation_2hour_rule(self):
       
        doc = Doctor("Dr. A", 1)
        p = StudentPatient("Alice", 10)
        self.clinic.register_staff(doc)
        self.clinic.register_patient(p)

        self.clock.set_hour(10)
        appt = self.clinic.book_appointment(1, 10, 1, 14)  
        self.clinic.confirm_appointment(1)

        self.clock.set_hour(12)
        self.clinic.cancel_appointment(1, "Cancelled exactly at 2h")
        self.assertTrue(appt.is_cancelled())

        
        appt2 = self.clinic.book_appointment(2, 10, 1, 16)
        self.clinic.confirm_appointment(2)
        self.clock.set_hour(15)

        with self.assertRaises(CancellationError):
            self.clinic.cancel_appointment(2, "Too late")

    def test_cancellation_post_start(self):
        
        doc = Doctor("Dr. A", 1)
        p = StudentPatient("Alice", 10)
        self.clinic.register_staff(doc)
        self.clinic.register_patient(p)

        self.clock.set_hour(10)
        self.clinic.book_appointment(1, 10, 1, 12)
        self.clock.set_hour(12)  # Started

        with self.assertRaises(CancellationError):
            self.clinic.cancel_appointment(1)

    def test_cancelled_appointment_cannot_return(self):
        
        doc = Doctor("Dr. A", 1)
        p = StudentPatient("Alice", 10)
        self.clinic.register_staff(doc)
        self.clinic.register_patient(p)

        self.clock.set_hour(8)
        self.clinic.book_appointment(1, 10, 1, 12)
        self.clinic.cancel_appointment(1)

        with self.assertRaises(IllegalStateTransitionError):
            self.clinic.confirm_appointment(1)

        with self.assertRaises(IllegalStateTransitionError):
            self.clinic.cancel_appointment(1)


if __name__ == "__main__":
    unittest.main()
