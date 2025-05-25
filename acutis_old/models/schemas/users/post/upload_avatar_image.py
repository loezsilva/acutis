from pydantic import BaseModel
from spectree import BaseFile


class UploadAvatarImageRequest(BaseModel):
    image: BaseFile
