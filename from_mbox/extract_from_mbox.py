import sys
import mailbox
import csv

import json

infile = sys.argv[1]
outfile = sys.argv[2]
writer = csv.writer(open(outfile, "w+"))

writer.writerow(['from', 'to', 'cc'])
for index, message in enumerate(mailbox.mbox(infile)):
    row = [
        # message['date'],
        message['from'],
        message['to'],
        message['cc']
    ]
    writer.writerow(row)
