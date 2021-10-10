#!/usr/bin/python3

'''
Description:
* To check difference of list in 1st and 2nd then ouput the values in 2nd list that were not in 1st list.
* Used when initial phishing campaign yielded results.
    * Once you get to download the full address list (list of emails) of that target company, you may then need to send a 2nd phishing campaign to those you have not sent yet in the 1st campaign.
    * This script compares both email list.
* Inputs:
  * 1st argument:
    * 1st list (i.e. line separated list of emails)
      * Use case: list of users in the 1st phishing campaign
  * 2nd argument:
    * 2nd list (i.e. Global/Full address/email list)
      * Extracted by Mailsniper or manually through the OWA or Office365 People
'''

import os,sys

with open(sys.argv[1],'r') as file1, open(sys.argv[2],'r') as file2:
    names_first = [name_first.lower().strip("\n") for name_first in file1.readlines()]
    names_second = [name_second.lower().strip("\n") for name_second in file2.readlines()]
    for name in names_second:
        if name not in names_first:
            print(name)
