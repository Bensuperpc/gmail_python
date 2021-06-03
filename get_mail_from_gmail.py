#!/usr/bin/env python
#
# get_mail.py - Get mail from gmail api
#
# Created by Bensuperpc at 28, February of 2020
#
# Released into the Private domain with MIT licence
# https://opensource.org/licenses/MIT
#
# Written with VisualStudio code 1.4.2 and python 3.7.8
# Script compatibility : Linux (Ubuntu ad debian based), Windows, mac
#
# ==============================================================================

from __future__ import print_function
import pickle
import os.path
import sys
import csv
from datetime import datetime
import sys

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client import file, client, tools

from utils.gmailapi_pers import GetListIDMail, ReadMail


class GetMail:
    __author__ = "Bensuperpc"
    __credits__ = ["None", "None"]
    __license__ = "MIT"
    __version__ = "1.0.0"
    __maintainer__ = "Bensuperpc"
    __email__ = ["bensuperpc@gmail.com"]
    __status__ = "Production"
    __compatibility__ = ["Linux", "Windows", "Darwin"]
    __name__ = "GetMail"

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    token_file_name = 'token.pickle'
    credentials_file_name = 'credentials.json'
    user_id = 'me'

    def GetService(self):
        creds = None

        if os.path.exists(self.token_file_name):
            with open(self.token_file_name, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file_name, self.SCOPES)
                creds = flow.run_local_server(port=0)

            with open(self.token_file_name, 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)
        return service

    def run(self, row_max=1000000):
        service = self.GetService()
        emails = GetListIDMail(service, self.user_id)
        row = 0
        file = 'emails_' + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + '.csv'
        fieldnames = ['msg_id', 'Date', 'From', 'To', 'Subject']

        with open(file, 'w+', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()
            for email in emails:
                msg_id = email['id']
                email_parse = ReadMail(service, self.user_id, msg_id)
                if email_parse is not None:
                    writer.writerow(email_parse)
                    row += 1
                if row > 0 and (row % 20) == 0:
                    print('Mails read: %d' % (row))
                if row >= row_max:
                    break

    def __init__(self):
        self.name = ""


if __name__ == '__main__':
    objName = GetMail()
    objName.run()
