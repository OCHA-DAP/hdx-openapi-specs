from typing import Any
from pydantic import BaseModel, Field


class FieldInfo(BaseModel):
    id: str = Field(..., description="The field name (column identifier).")
    type: str = Field(..., description="The PostgreSQL data type of the field (e.g. 'text', 'int4', 'timestamp').")
    info: dict[str, Any] | None = Field(None, description="Optional metadata dictionary attached to the field.")


class ErrorResponse(BaseModel):
    success: bool = Field(False, description="Always false for error responses.")
    error: dict[str, Any] = Field(..., description="Error detail object. Always contains a '__type' string. 403/404 errors include a 'message'; validation (409) errors instead carry structured 'query'/'info' fields.")
