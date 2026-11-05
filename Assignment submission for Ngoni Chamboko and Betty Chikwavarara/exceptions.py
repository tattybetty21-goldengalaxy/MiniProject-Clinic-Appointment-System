
#Custom exceptions for the Clinic Appointment System.
#Used for clean, explicit error handling and audit logging.



class ClinicError(Exception):
   
    pass


class InvalidEntityError(ClinicError):
   
    pass


class SchedulingConflictError(ClinicError):
   
    pass


class IllegalStateTransitionError(ClinicError):
    
    pass


class CancellationError(ClinicError):
   
    pass


class DuplicateIdError(ClinicError):
    
    pass
