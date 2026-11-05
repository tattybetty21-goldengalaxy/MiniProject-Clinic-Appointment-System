
#  Virtual Clock module for Clinic Appointment System.


from typing import Protocol


class Clock:
   

    def __init__(self, initial_hour: int = 0) -> None:
        if not isinstance(initial_hour, int) or not (0 <= initial_hour <= 168):
            raise ValueError(f"Initial hour must be an integer between 0 and 168, got {initial_hour}")
        self._current_hour: int = initial_hour

    def now(self) -> int:
        return self._current_hour

    def advance(self, hours: int = 1) -> int:
        if not isinstance(hours, int) or hours < 0:
            raise ValueError(f"Advance hours must be a non-negative integer, got {hours}")
        new_hour = self._current_hour + hours
        if new_hour > 168:
            raise ValueError(f"Advancing by {hours} hours exceeds the 1-week limit (168h): {new_hour}")
        self._current_hour = new_hour
        return self._current_hour

    def set_hour(self, hour: int) -> None:
        if not isinstance(hour, int) or not (0 <= hour <= 168):
            raise ValueError(f"Hour must be an integer between 0 and 168, got {hour}")
        self._current_hour = hour

    def __repr__(self) -> str:
        return f"Clock(now={self._current_hour}h)"
