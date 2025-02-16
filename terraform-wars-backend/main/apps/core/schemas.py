from typing import Any, Dict, List
from ninja import Schema


class ForbiddenErrorSchema(Schema):
    detail: str


class NotFoundErrorSchema(Schema):
    detail: str


class ValidationErrorSchema(Schema):
    detail: List[Dict[str, Any]]
