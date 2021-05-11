import re
import sys
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="DESCRIPTION:\nThis small script just filters out and prints the email address from a blob of text.\n" +
                                     "I commonly use this for filtering out email addresses from for example Office 365 / Exchange \"People\".\n" +
                                     "In Burp suite the blob.txt would be the responses from this URL: https://outlook.office.com/owa/service.svc?action=FindPeople&app=People&n=40\n" +
                                     "There a easier and better alternatives to this script such as Cyberchef's \"Extract Email Addresses\" Recipe (General use) or dafthack's \"Get-GlobalAddressList\" function in MailSniper (Exchange/o365 use) although processing a REALLY BIG blob of text is better using this.\n\n"+
                                     "Example commands:\n" +
                                     "$ python3 " + sys.argv[0] + " --blob blob.txt --output output.txt\n")

parser.add_argument("--blob", dest="blob", required=True, type=str, help="Input file. Blob of text.")
parser.add_argument("--output", dest="output", required=False, type=str, default="blob_email_addresses_output.txt",help="The NTDS file from which you extracted the users hashes from.\nThis could be the output of ntdsutil+secretsdump or secretsdump directly or 'crackmapexec --ntds' option, etc. Then grepped to filter out machine hashes and other non-user hash related lines.")
args = parser.parse_args()

list_of_emails = set()

with open(args.blob,'r') as blob_file, open(args.output,'w+') as output :
 
	for line in blob_file.readlines():
	    line = line.strip('\n')
	    emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", line)
	    for mail in emails:
	        list_of_emails.add(mail.lower())


	for mail in sorted(list_of_emails):
	    output.write(mail+"\n")
	    print(mail)
