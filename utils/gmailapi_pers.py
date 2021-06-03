#!/usr/bin/env python
#
# send_to_neo4j.py - Get mail from gmail api
#
# Created by Bensuperpc at 05, March of 2020
#
# Released into the Private domain with MIT licence
# https://opensource.org/licenses/MIT
#
# Written with VisualStudio code 1.4.2 and python 3.7.8
# Script compatibility : Linux (Ubuntu ad debian based), Windows, mac
#
# ==============================================================================

import re

def GetListIDMail(service=None, user_id=None, max_res=500):
    if service == None or user_id == None:
        return
    response = service.users().messages().list(userId=user_id,
                                                labelIds=[],
                                                maxResults=max_res).execute()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])

    while 'nextPageToken' in response:
        page_token = response['nextPageToken']

        response = service.users().messages().list(userId=user_id,
                                                    labelIds=[],
                                                    pageToken=page_token,
                                                    maxResults=max_res).execute()
        messages.extend(response['messages'])

        print('%d emails on page: token: %s, %d mails getted now...' % (
            len(response['messages']), page_token, len(messages)))
    return messages

def ReadMail(service=None, user_id=None, msg_id=None):
    if service == None or user_id == None or msg_id == None:
        return
    
    temp = {}
    pat = r'(?<=\<).+?(?=\>)'
    try:

        message = service.users().messages().get(
            userId=user_id, id=msg_id).execute()
        header = message['payload']['headers']

        temp['msg_id'] = msg_id
        list_ = ['']

        for one in header:
            if one['name'] == 'Date':
                msg_date = one['value']
                temp['Date'] = msg_date
            else:
                pass
        for two in header:
            if two['name'] == 'From':
                tmp = two['value']
                if "<" in tmp:
                    str_list = re.findall(pat, tmp)
                    tmp = ''
                    for str_ in str_list:
                        tmp = tmp + str_ + ', '
                    tmp = tmp.rstrip(', ')
                    temp['From'] = tmp
                else:
                    temp['From'] = tmp
            else:
                pass
        for three in header:
            if three['name'] == 'To':
                tmp = three['value']
                if "<" in tmp:
                    str_list = re.findall(pat, tmp)
                    tmp = ''
                    for str_ in str_list:
                        tmp = tmp + str_ + ', '
                    tmp = tmp.rstrip(', ')
                    temp['To'] = tmp
                else:
                    temp['To'] = tmp
                if not tmp:
                    temp['To'] = 'Test'
            else:
                pass
        for four in header:
            if four['name'] == 'Subject':
                temp['Subject'] = four['value']
            else:
                pass
    except Exception as e:
        print(e)
        temp = None
        pass

    finally:
        if not temp == None:
            if len(temp) == 3:
                temp['To'] = 'bensuperpc@gmail.com'
        return temp

