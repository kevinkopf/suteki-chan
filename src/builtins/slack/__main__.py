import os
from email.utils import parseaddr
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Union


class Slack:
    def __init__(self, config: dict, action: dict) -> None:
        token = os.getenv('SUTEKI_SLACK_TOKEN') if os.getenv('SUTEKI_SLACK_TOKEN') else config['security']['slack']['token']
        self.client = WebClient(token=token)
        self.action = action
        self.action_args = action['args']

    def get_user_by_email(self) -> Union[str, None]:
        try:
            result = self.client.users_lookupByEmail(
                email=self.action_args['channel']
            )
            if result.get("ok"):
                return result.get("user")['id']
            return None

        except SlackApiError as e:
            print("Error posting message: {}".format(e))
            return None

    def is_channel_email_address(self) -> bool:
        addr = parseaddr(self.action_args['channel'])
        if addr[1]:
            return True
        return False

    def post_message(self) -> Union[str, None]:
        try:
            result = self.client.chat_postMessage(
                channel=self.get_user_by_email() if self.is_channel_email_address() else self.action_args['channel'],
                thread_ts=self.action_args['thread'] if 'thread' in self.action_args else None,
                text=self.action_args['message']
            )
            if result.get("ok"):
                return result.get("ts")
            return None

        except SlackApiError as e:
            print("Error posting message: {}".format(e))
            return None

    def post_file(self):
        try:
            result = self.client.files_upload(
                channel=self.get_user_by_email() if self.is_channel_email_address() else self.action_args['channel'],
                thread_ts=self.action_args['thread'] if 'thread' in self.action_args else None,
                file=self.action_args['file'],
            )
            return result

        except SlackApiError as e:
            print("Error uploading file: {}".format(e))
