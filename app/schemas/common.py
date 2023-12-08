from pydantic import BaseModel

class NotFoundResponse(BaseModel):
    message: str = "Not found"
    value: str | None = None