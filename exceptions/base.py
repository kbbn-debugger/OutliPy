from abc import ABC
from error_codes import ErrorCodeRegistry
from typing import Optional, Dict, Any

class OutliPyException(Exception, ABC):
    """
    Base exception. It creates the message but doesn't care about specific parameters.
    """
    default_error_code = "OE000"

    def __init__(self, *, 
                 error_code: str,
                 detector: str,
                 context: Optional[Dict[str, Any]] = None,
                 suggestion: Optional[str] = None
                 ):
        
        self.error_code = error_code
        self.detector = detector
        self.context = context or {} 
        self.suggestion = suggestion or "Please check your configuration."
        
        message = self._build_message()
        super().__init__(message)

    def _build_message(self) -> str:
        """
        Builds the exception message from template using the error code, detector, suggestion, and context.

        Returns:
            str: The message.
        """
        template = ErrorCodeRegistry.get(self.error_code)

        if template is None:
            return (
                f"[{self.detector}] - {self.default_error_code}\n"
                f"Context: Unknown OutliPy Error.\n"
                f"Suggestion: Please report us the error"
            )

        return template.format(
            error_code=self.error_code,
            detector=self.detector,
            suggestion=self.suggestion,
            **self.context 
        )