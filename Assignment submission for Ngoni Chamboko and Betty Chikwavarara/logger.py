
# Logging module for Clinic Appointment System.

import sys
from typing import Optional, List, Callable, TextIO


class AppointmentLog:
   
    def __init__(
        self,
        stream: Optional[TextIO] = None,
        callback: Optional[Callable[[str], None]] = None,
    ) -> None:
        self._stream: TextIO = stream if stream is not None else sys.stdout
        self._callback: Optional[Callable[[str], None]] = callback
        self._entries: List[str] = []
        self._is_open: bool = False

    def __enter__(self) -> "AppointmentLog":
        self._is_open = True
        self._emit("[log] opened")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
       
        try:
            self._emit("[log] closed")
        finally:
            self._is_open = False
        
        return False

    def log(self, message: str) -> None:
        self._emit(message)

    def log_failure(self, action: str, reason: str) -> None:
        self._emit(f"FAILED {action}: {reason}")

    def _emit(self, line: str) -> None:
        self._entries.append(line)
        if self._stream:
            self._stream.write(line + "\n")
            self._stream.flush()
        if self._callback:
            self._callback(line)

    @property
    def entries(self) -> List[str]:
        return list(self._entries)

    def clear(self) -> None:
        self._entries.clear()
