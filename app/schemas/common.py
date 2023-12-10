from dataclasses import dataclass
from bson import ObjectId
from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import core_schema
from typing import Any, Type

class NotFoundResponse(BaseModel):
    message: str = "Not found"
    value: str | None = None

@dataclass
class PyMongoObjectId:
    value: ObjectId

    def build(self) -> ObjectId:
        return self.value

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        assert source is PyMongoObjectId
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize,
                info_arg=False,
                return_schema=core_schema.str_schema(),
            ),
        )
    
    @staticmethod
    def _validate(value: ObjectId) -> 'PyMongoObjectId':
        return PyMongoObjectId(value)
    
    @staticmethod
    def _serialize(value: 'PyMongoObjectId') -> ObjectId:
        return value.build()