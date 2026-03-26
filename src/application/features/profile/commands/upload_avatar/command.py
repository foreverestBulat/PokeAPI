from dataclasses import dataclass
from uuid import UUID


@dataclass
class UploadAvatarCommand:
    user_id: UUID
    content: bytes
    filename: str
