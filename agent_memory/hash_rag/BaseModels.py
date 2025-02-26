from pydantic import BaseModel, Field
from typing import List, Literal, Any, Optional, Union
import uuid

class DataInformation(BaseModel):
    parent_location: str = Field(description='The location of the source data')
    datatype: str = Field(description='The datatype of the data')
    is_stored_locally: bool = Field(description='A boolean to describe if the data is stored locally or internally')
    data: Optional[Union[str, bytes, dict, list]] = Field(description='The data')
    data_location: Optional[str] = Field(default=None, description='The location of the data')

class HashRagBaseModel(BaseModel):
    index: uuid.UUID = Field(default_factory=uuid.uuid4, description='The unique identifier for the underlying data')
    data_object: DataInformation
    vector_embeddings: List = Field(description='The returned embeddings from the given datapoint')

class DataResponseInformation(BaseModel):
    source: str
    data: str

class ResponseModel(BaseModel):
    ai_response: str = Field(description='This is the approximate response from the data sources')
    data: List[DataResponseInformation]