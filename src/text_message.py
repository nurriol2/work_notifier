#!/usr/bin/env python3 

#buying twilio phone numbers costs $1.00 each
#sending SMS costs $0.01 each

from twilio.rest import Client
from credentials import credentials

class TextMessage:

    client = Client(credentials["account_sid"], credentials["auth_token"])

    def __init__(self, msg_content=""):
        """Wrapper for the contents of a group text message (SMS)

        Args:
            msg_content (string, optional): The content of a text message.
                                         Typically, all scheduled instructor's working hours. 
                                         Defaults to "".
        """
        self.msg_content = msg_content
        return 

    def append_to_msg_content(self, to_add):
        """Modify the contents of `msg_content` by adding a new line to the end

        Args:
            to_add (string): The content to append. Typically generated from `Instructor().get_human_time()`.
        """
        self.msg_content += to_add
        return 

    def send_text(self):
        """Send a text message (SMS)
        """
        self.client.messages.create(
            to=credentials["my_cell"],
            from_=credentials["my_twilio"],
            body=self.msg_content
        )
        return 

