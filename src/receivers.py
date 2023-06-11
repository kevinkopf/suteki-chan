from abc import ABC
from typing import Literal, Optional
from pydantic import BaseModel, Field


class BaseReceiver(ABC, BaseModel):
    user_agent: str
    event: str
    security_token: str

    def security_check(self, security_token: str) -> bool:
        return security_token == self.security_token


class GitlabReceiver(BaseReceiver):
    user_agent: Literal['GitLab']
    instance: str
    event: str
    event_uuid: str
    security_token: str
    content_type: Optional[str]

    class Config:
        fields = {
            'instance': 'x-gitlab-instance',
            'event': 'x-gitlab-event',
            'event_uuid': 'x-gitlab-event-uuid',
            'security_token': 'x-gitlab-token',
            'content_type': 'content-type',
        }


class CustomReceiver(BaseReceiver):
    user_agent: Literal['Custom']
    security_token: str
    event: Optional[str]
    content_type: Optional[str]

    class Config:
        extra = 'allow'
        fields = {
            'event': 'x-event',
            'security_token': 'x-token',
            'content_type': 'content-type',
        }


class Receiver(BaseModel):
    receiver: \
        GitlabReceiver | \
        CustomReceiver \
        = Field(..., discriminator='user_agent')
