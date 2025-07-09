from pydantic import BaseModel, Field
from typing import List, Optional


class Profile(BaseModel):
    name: str = Field(..., alias="name")


class Contact(BaseModel):
    wa_id: str = Field(..., alias="wa_id")
    profile: Profile = Field(..., alias="profile")


class MessageText(BaseModel):
    body: str = Field(..., alias="body")


class MessageAudio(BaseModel):
    id: str = Field(..., alias="id")
    mime_type: str = Field(..., alias="mime_type")
    sha256: Optional[str] = None
    voice: Optional[bool] = None


class Message(BaseModel):
    from_user: str = Field(..., alias="from")
    id: str = Field(..., alias="id")
    timestamp: str = Field(..., alias="timestamp")
    type: str = Field(..., alias="type")

    text: Optional[MessageText] = None
    audio: Optional[MessageAudio] = None
    image: Optional[MessageAudio] = None


class WhatsAppPayload(BaseModel):
    contacts: List[Contact]
    messages: List[Message]
