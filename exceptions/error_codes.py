from typing import Optional

class ErrorCodeRegistry:
    _registry = {}

    @classmethod
    def register(cls, code: str, message_template: str) -> None:
        if code in cls._registry:
            raise ValueError(f"Duplicate error code detected: {code}")
        
        cls._registry[code] = message_template

    @classmethod
    def get(cls, code: str) -> Optional[str]:
        return cls._registry.get(code, None)