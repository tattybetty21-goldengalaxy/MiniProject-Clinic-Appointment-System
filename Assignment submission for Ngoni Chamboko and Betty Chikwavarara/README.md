Authors:

Name	                        Reg no	                  Prog
Ngonidzashe  T  Chamboko	  R2420419              	   HCS
Betty T Chikwavarara		     R2420387                    HCS


# Clinic Appointment System (Mini Project)

Language: Python 
This project is implemented and tested for Parameter $P = 3$, resulting in:
# Doctor Fee: $55.00  
# Nurse Fee: $10.00   
# Pharmacist Fee: $5.00  
# Assigned Twist: Twist 3 (Patient Discounts)  

-------------------------------------------------------------------------------------------

1. Class Diagram

```
                              ┌────────────────────────┐
                              │     <<abstract>>       │
                              │        Person          │
                              ├────────────────────────┤
                              │ - _name: str           │
                              │ - _id: int             │
                              ├────────────────────────┤
                              │ + name(): str          │
                              │ + id(): int            │
                              │ + role(): str {abstract}│
                              └───────────┬────────────┘
                                          │
            ┌─────────────────────────────┼─────────────────────────────┐
            │                             │                             │
            ▼                             ▼                             ▼
┌───────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────┐
│     <<abstract>>      │   │       <<abstract>>        │   │        Lecturer       │
│        Patient        │   │          Staff            │   ├───────────────────────┤
├───────────────────────┤   ├───────────────────────────┤   │ - _module_name: str   │
│                       │   │                           │   ├───────────────────────┤
├───────────────────────┤   ├───────────────────────────┤   │ + module_name(): str  │
│ + discount_rate()     │   │ + fee(): float {abstract} │   │ + role(): str         │
│ + calculate_price()   │   └─────────────┬─────────────┘   └───────────┬───────────┘
└───────────┬───────────┘                 │                             │
            │               ┌─────────────┼─────────────┐               │
     ┌──────┴──────┐        │             │             │               │
     ▼             ▼        ▼             ▼             ▼               │
┌─────────┐   ┌─────────┐┌──────┐      ┌─────┐    ┌──────────┐          │
│ Student │   │ Staff-  ││Doctor│      │Nurse│    │Pharmacist│          │
│ Patient │   │ Member  │├──────┤      ├─────┤    ├──────────┤          │
│ (50%)   │   │ (0%)    ││$55.00│      │$10  │    │$5.00     │          │
└─────────┘   └─────────┘└──┬───┘      └─────┘    └──────────┘          │
     │                      │                                           │
     ▼                      │                                           │
┌─────────┐                 └───────────────────┬───────────────────────┘
│ Visitor │                                     │
│ Patient │                                     ▼
│ (100%)  │                         ┌───────────────────────┐
└─────────┘                         │    MedicalLecturer    │
                                    │ (Doctor and Lecturer) │
                                    ├───────────────────────┤
                                    │ + role(): "Doctor and │
                                    │           Lecturer"   │
                                    │ + fee(): $55.00       │
                                    └───────────────────────┘

                 ┌───────────────────────────────────────────────┐
                 │                  Appointment                  │
                 ├───────────────────────────────────────────────┤
                 │ - __id: int                                   │
                 │ - __patient: Patient                          │
                 │ - __staff: Staff                              │
                 │ - __start_hour: int (0..168)                  │
                 │ - __status: PENDING | CONFIRMED | CANCELLED   │
                 ├───────────────────────────────────────────────┤
                 │ + confirm(): void                             │
                 │ + cancel(current_hour: int, reason: str): void│
                 │ + calculate_price(): float                    │
                 └───────────────────────┬───────────────────────┘
                                         │ 0..*
                                         ▼
                 ┌───────────────────────────────────────────────┐
                 │                    Clinic                     │
                 ├───────────────────────────────────────────────┤
                 │ - __clock: Clock                              │
                 │ - __staff: Dict[int, Staff]                   │
                 │ - __patients: Dict[int, Patient]              │
                 │ - __appointments: List[Appointment]           │
                 ├───────────────────────────────────────────────┤
                 │ + register_staff(staff: Staff): void          │
                 │ + register_patient(patient: Patient): void    │
                 │ + book_appointment(id, pt_id, st_id, hr)      │
                 │ + confirm_appointment(id): void               │
                 │ + cancel_appointment(id, reason): void        │
                 │ + open_log(): AppointmentLog                  │
                 └───────────────────────────────────────────────┘
```
-------------------------------------------------------------------------------------------

 2. Encapsulation, State Transitions, and Invariants (Question 2)

# A. Information Hiding & Defensive Copies

- All collections (`__staff`, `__patients`, `__appointments`) are private with double-underscore(__)name mangling.
- Accessor methods `get_appointments()`, `get_staff()`, and `get_patients()` return shallow defensive copies (`list(...)`). Modifying the returned list (e.g calling `.clear()`) has zero effect on the Clinic's internal records.

# B. Legal Transitions & Enforced Cancellation Rules

1. Initial State: Appointments are created in `PENDING` status.

2. Legal Transitions:
   - `PENDING -> CONFIRMED` (via `confirm()`)
   - `PENDING -> CANCELLED` (via `cancel(now, reason)`)
   - `CONFIRMED -> CANCELLED` (via `cancel(now, reason)`)
3. Strict Invariants:

   - Cancelled is Terminal: A cancelled appointment can never return, be confirmed, or be cancelled again (`IllegalStateTransitionError`).

   - 2 Hour Rule: A confirmed appointment cannot be cancelled less than 2 hours before start (`now > start_hour - 2` raises `CancellationError`).

   - Post-Start Rule: No appointment (pending or confirmed) can be cancelled once it has started (`now >= start_hour` raises `CancellationError`).

4. Constructor Validation:
   - `Person` and `Appointment` reject empty or whitespace-only names and non positive IDs ($\le 0$) by raising `InvalidEntityError`.
   - `start_hour` is validated to fall strictly within $[0, 168]$ (one week).

-------------------------------------------------------------------------------------------

# 3.How to loop over a list of Staff, print each person’s role and fee in one loop. How do you do this with no instanceof / isinstance.(Question 3)

With $P = 3$:
- Doctor fee: $40 + 5 \times (3 \bmod 5) = 40 + 15 = \$55.00$
- Nurse fee: $10 + (3 \bmod 3) = 10 + 0 = \$10.00$
- Pharmacist fee: Flat rate of $5.00

# Polymorphism Iteration Without Type Tags
```python
def print_staff_roster(staff_members: List[Staff]) -> None:
    for member in staff_members:
        print(f"{member.role()}: ${member.fee():.2f}")
```
Why this satisfies OCP:

 New subclasses of `Staff` (such as `Dentist` or `Physiotherapist`) can be added without altering a single character of this loop or the `Clinic` class.

-------------------------------------------------------------------------------------------

# 4. Context-Managed Appointment Log (Question 4)

Every Clinic operation is guarded by the context manager protocol (`__enter__` and `__exit__`):

```python
with self.open_log() as log:
    
```

- When the block begins, `__enter__` emits `[log] opened`.
- When the block exits—whether normally or aborted by an exception—`__exit__` executes in a `finally` block and emits `[log] closed`.
- If an action violates a rule, `log_failure` emits:
  `FAILED cancel #3: too late: confirmed appointment #3 cannot be cancelled less than 2 hours before start (starts at 16, current is 15)`

-------------------------------------------------------------------------------------------

# 5. Multiple Inheritance, MedicalLecturer, and Constructor Counter (Question 5)

`MedicalLecturer` inherits from both `Doctor` and `Lecturer`:
- In Python, cooperative `super().__init__(**kwargs)` resolves the inheritance hierarchy via C3 Linearization (Method Resolution Order - MRO):
  `MedicalLecturer -> Doctor -> Staff -> Lecturer -> Person -> object`
- `Person._constructor_call_count` verifies that `Person.__init__` executes exactly once.
- `role()` returns `"Doctor and Lecturer"`.
- `fee()` returns `super().fee()` which evaluates to the Doctor's fee of $\$55.00$.

# Java Restructuring Explanation:

Java does not support multiple class inheritance. In Java, `Lecturer` must become an `interface Lecturer { String getModuleName(); }`, and `MedicalLecturer` extends `Doctor` while implementing `Lecturer`.

-------------------------------------------------------------------------------------------

# 6. Twist 3: Patient Discounts Without Type Checks (Question 6)

Discounts are structured using polymorphism dispatch:
- `StudentPatient`: $50\%$ discount (`discount_rate() = 0.50`, pays $0.5 \times \text{fee}$)
- `StaffMemberPatient`: $100\%$ discount (`discount_rate() = 1.00`, pays $0.0 \times \text{fee}$)
- `VisitorPatient`: $0\%$ discount (`discount_rate() = 0.00`, pays $1.0 \times \text{fee}$)

`appointment.calculate_price()` evaluates:

```python
self.__patient.calculate_price(self.__staff.fee())
```
There are zero `isinstance` checks in `Appointment` or `Clinic`.

---

# 7. Design Decision Log (D1 – D6)

# D1. Where does the 2-hour rule live?

Chosen Location: `Appointment.cancel(current_hour)`  

Alternatives Considered:

1. Inside Clinic: Violates information hiding by having Clinic micro-manage Appointment's internal state.

2. Inside Staff: Inappropriate, because cancellation rules are a property of the appointment agreement, not provider physiology.

3. Separate Policy Object (`CancellationPolicy`)*: Excellent for enterprise rule engines with dynamic rules, but introduces unnecessary indirection for a fixed 2-hour rule.

Trade-Off: Co-locating in `Appointment` keeps entity invariants self-contained and prevents any bypass if Appointment is manipulated directly. `Clinic` acts as the coordinator supplying simulation time from the Clock.

# D2. Why is your clock design testable, and what could not be tested with system time directly?
Why testable: 

The virtual `Clock` allows deterministic, instantaneous time travel. We can set $t=10$, book an appointment for $t=14$, advance to $t=12$ (boundary of 2-hour rule), and advance to $t=13$ (inside forbidden window) without waiting for real wall-clock hours or monkeypatching `time.time()`. 

What could not be tested: A 1-week simulation ($168$ hours) and millisecond-accurate boundary edge conditions cannot be feasibly tested on real wall-clock time in CI pipelines.

# D3. When you added Pharmacist, what did you change besides the new class?
 Nothing it remained the same.

Only `class Pharmacist(Staff): ...` was declared. The staff printing loop, the `Clinic`, the `Appointment` booking flow, and the billing engine required zero modifications. Nothing leaked because the design adheres strictly to the Open-Closed Principle (OCP) and Liskov Substitution Principle (LSP).

# D4. What should MedicalLecturer.fee() return, and which language feature stops Person being created twice?
Fee: $\$55.00$ (Doctor fee). In clinical practice, patient appointments represent medical services rendered by a licensed doctor. Academic lecturing duties are separately salaried by the university and not billed to clinic patients.

Language Feature: Python's C3 Linearization MRO(`method resolution order`) and cooperative `super()` ensure each ancestor in the diamond graph (`Person`) appears in the resolution list exactly once. Without cooperative `super()`, calling explicit parent initializers (`Doctor.__init__` and `Lecturer.__init__`) would run `Person.__init__` twice, duplicating initialization and state.

# D5. What should happen if writing to or closing the log itself fails?

The failure must be reported to a dedicated diagnostic fallback channel (such as `sys.stderr` or an alert monitor), but must not silently corrupt or abort clinical transactional records. In mission critical clinical systems, if the audit logger storage fills or crashes, transactions must either enter a failsecure mode or alert system administrators immediately.

# D6. Twist 3: Where does the discount live and why?
An The discount logic lives on `Patient` (`calculate_price` / `discount_rate`).  
Why?: Discount eligibility is an intrinsic property of the patient's institutional status (student ID, employee badge, visitor). Neither the `Staff` member nor the `Clinic` needs to know why a patient is discounted; they simply delegate price calculation to the patient entity.

-------------------------------------------------------------------------------------------

