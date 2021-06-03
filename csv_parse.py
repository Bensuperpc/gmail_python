#!/usr/bin/env python
#
# send_to_neo4j.py - Get mail from gmail api
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

import csv

from utils.send_to_neo4j import send

with open('emails_06-03-2020_16-04-50.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    data = []

    # Skip Header
    next(spamreader)

    for row in spamreader:
        f = row[2]
        t = row[3].split(",")
        s = row[4]

        if not "@" in f:
            continue

        for t_data in t:
            if not "@" in t_data:
                continue
            if not t_data.split("@")[1] == "homtmail.fr" and not f.split("@")[1] == "homtmail.fr":
                continue
            #if t_data.split("@")[1] == "homtmail.fr" and f.split("@")[1] == "homtmail.fr":
            #   continue

            if not f == t_data.strip():
                #data.append([f.split("@")[0], t_data.strip().split("@")[0]])
                data.append([f, t_data.strip(), s])

    # Sand data to NEO4J
    #send(data)

    people = []
    mail_people = []
    moy_send = 0.0
    moy_rece = 0.0
    
    # add people
    for _data in data:
        if not _data[0] in people:
            people.extend([_data[0]])
        if not _data[1] in people:
            people.extend([_data[1]])
    
    for _people in people:
        mail_people.append([_people, int(0), int(0)])
    
    for _data in data:
        # Sender
        # index = sorted(mail_people, key=lambda tup: tup[1])
        index = [y[0] for y in mail_people].index(_data[0])
        mail_people[index][1] = mail_people[index][1] + 1
        # Receiver
        index = [y[0] for y in mail_people].index(_data[1])
        mail_people[index][2] = mail_people[index][2] + 1
    mail_people.sort(key=lambda tup: tup[2])
    
    for _mail_people in mail_people:
        moy_send = moy_send + _mail_people[1]
        moy_rece = moy_rece + _mail_people[2]
        
    moy_send = moy_send / len(mail_people)
    moy_rece = moy_rece / len(mail_people)
    
    print(*mail_people,sep='\n')
    print(len(people), 'People')
    
    print('moy Send :', moy_send)
    print('moy Receive :', moy_rece)
    
    
