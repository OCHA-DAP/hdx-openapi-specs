from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class FieldDictionaryInfo(BaseModel):
    # CKAN's data dictionary is free-form; label and notes are the keys HDX uses.
    model_config = ConfigDict(extra="allow")

    label: str | None = Field(None, description="Human-readable display name for the column.")
    notes: str | None = Field(None, description="Description of the column's contents.")


class FieldInfo(BaseModel):
    id: str = Field(..., description="The field name (column identifier).")
    type: str = Field(..., description="The CKAN DataStore type of the field (e.g. 'text', 'numeric', 'timestamp').")
    info: FieldDictionaryInfo | None = Field(
        None,
        description="The column's data dictionary entry. Other keys besides `label` and `notes` may be present.",
    )


class ErrorResponse(BaseModel):
    success: bool = Field(False, description="Always false for error responses.")
    error: dict[str, Any] = Field(..., description="Error detail object. Always contains a '__type' string. 403/404 errors include a 'message'; validation (409) errors instead carry structured 'query'/'info' fields.")
