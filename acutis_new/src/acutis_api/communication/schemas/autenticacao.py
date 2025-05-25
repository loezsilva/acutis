from pydantic import BaseModel, ConfigDict


class GoogleCallbackSchema(BaseModel):
    model_config = ConfigDict(extra='ignore')

    email: str
    name: str
