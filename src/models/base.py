"""
Base Model Class

Provides common functionality for all models.
"""

from typing import Dict, Any
from datetime import datetime


class BaseModel:
    """
    Base model class with common validation and conversion methods.
    """

    def __init__(self, **kwargs):
        """Initialize model with given attributes."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary.

        Returns:
            Dictionary representation of model
        """
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        }

    def to_json(self) -> str:
        """
        Convert model to JSON string.

        Returns:
            JSON representation of model
        """
        import json

        return json.dumps(self.to_dict(), default=str)

    def validate(self) -> tuple:
        """
        Validate model data.

        Returns:
            Tuple of (is_valid, error_message)
        """
        return True, ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Create model instance from dictionary.

        Args:
            data: Dictionary with model data

        Returns:
            Model instance
        """
        return cls(**data)

    def __repr__(self) -> str:
        """String representation of model."""
        attrs = ", ".join(
            f"{k}={v!r}"
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        )
        return f"{self.__class__.__name__}({attrs})"
