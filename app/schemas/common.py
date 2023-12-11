from typing import Generic, List, TypeVar
from typing_extensions import Annotated
from pydantic import BaseModel, BeforeValidator

class NotFoundResponse(BaseModel):
    message: str = "Not found"
    value: str | None = None

T = TypeVar('T', bound=BaseModel)
class GetManyResponseDto(BaseModel, Generic[T]):
    page: int
    perPage: int
    nextPage: int | None = None
    prevPage: int | None = None
    totalPage: int
    data: List[T]

PyObjectId = Annotated[str, BeforeValidator(str)]