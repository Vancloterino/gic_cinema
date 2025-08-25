"""Domain-level exceptions for the booking system."""

from __future__ import annotations


class DomainError(Exception):
    """Base class for domain errors."""


class NotFound(DomainError):
    """Requested entity was not found."""


class CapacityExceeded(DomainError):
    """Requested capacity exceeds availability."""


class InvalidSelection(DomainError):
    """User selection failed validation (format, bounds, etc.)."""


class RuleViolation(DomainError):
    """A business rule was violated (e.g., seat spacing rules)."""
