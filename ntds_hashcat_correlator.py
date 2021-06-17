#!/usr/bin/python3

import sys
import argparse
import time

def statistics(credentials):
    """
    Statistics for count:password

    Prints the statistics of the most common/reused password and its total number
    The output here does not contain the users that use the password, just password and count itself

    Output sample:
    +++++++++++++++++++++++++++++++++++++++++++
    Below are the top commonly used passwords amongst this set:
    671 : P@ssw0rd
    423 : monkey
    322 : rick@roll
    2 : whowouldhavethought
    ... : ...
    ...
    """
    print("\n\n+++++++++++++++++++++++++++++++++++++++++++\n                 STATISTICS\n+++++++++++++++++++++++++++++++++++++++++++\nBelow are the top commonly used passwords amongst this set:\n")
    for password, result_set in sorted(credentials.items(), key=lambda item: len(item[1]), reverse=True):
        if len(result_set):
            print(f"{len(result_set)} : {password}")


def password_reuse_view(ntds_dump, hashcat_cracked_NTLM_hashes):
    """
    Sorts and prints first according to the biggest number/count of common/reused passwords and
    prints the users that use that password directly below it.

    Output sample:
    -------------------------------------------
    [671] usernames use the password:  P@ssw0rd
     - ACME\\john
     - ACME\\haxy
     - ACME\\bob
     - ...
     ...

    """
    credentials = {}
    for cracked_hash in hashcat_cracked_NTLM_hashes:
        result_set = set()
        cracked_ntlm_hash = cracked_hash.strip('\n').split(':')[0]
        cracked_plaintext_password = cracked_hash.strip('\n').split(':')[1]
        for ntds_hash in ntds_dump:
            if cracked_ntlm_hash == ntds_hash.strip('\n').split(':')[3]:
                result_set.add(ntds_hash.strip('\n').split(':')[0].lower())
        if len(result_set):
            credentials[cracked_plaintext_password] = result_set

    flag_start_of_unique_passwords = 0
    for password, result_set in sorted(credentials.items(), key=lambda item: len(item[1]), reverse=True):
        if len(result_set) == 1:
            if(not flag_start_of_unique_passwords):
                print(
                    "\n\n-------------------------------------------\n[1] Below are usernames that makes use of unique passwords amongst this set of cracked hashes:\n")
                flag_start_of_unique_passwords = 1
            print(result_set.pop() + ":"+password)
        else:
            print(
                f"\n-------------------------------------------\n[{len(result_set)}] username(s) use Password:  {password}")
            for result in sorted(result_set):
                print(" - " + result)

    statistics(credentials)


def normal_view(ntds_dump, hashcat_cracked_NTLM_hashes):
    """
    Correlates the original ntds dump from tools like impacket-secretsdump.py or mimikatz
    Finds the hash from each text file and prints the line if there is a match, the output of this line is the domain\\username:CLEARTEXTPASSWORD

    Output sample:
    ACME\\john:P@ssw0rd
    ACME\\haxy:P@ssw0rd
    ACME\\mrhankee:P00sw0rd
    """
    result_set = set()
    for cracked_hash in hashcat_cracked_NTLM_hashes:
        cracked_ntlm_hash = cracked_hash.strip('\n').split(':')[0]
        cracked_plaintext_password = cracked_hash.strip('\n').split(':')[1]
        for ntds_hash in ntds_dump:
            if cracked_ntlm_hash == ntds_hash.strip('\n').split(':')[3]:
                result_set.add(str(ntds_hash.strip('\n').split(
                    ':')[0].lower() + ':' + cracked_plaintext_password).strip('\t'))

    for result in sorted(result_set):
        print(result)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="DESCRIPTION:\nThis script correlates the NTDS dump(i.e. secretsdump/ntdsutil/crackmapexec --ntds) and hashcat's potfile or cracked output.\n\n" +
                                     "This script has two modes:\n" +
                                     "Mode 1: Normal Output: Normal output of \"username:<password>\" or \"domain\\username:<password>\".\n" +
                                     "Mode 2: Password Reuse + Statistics Output: First output prints from top most used password first then all usernames using that password and so on.\nLast output would be the Statistics output which prints the top most used passwords in descending order and how many accounts are using those passwords.\n\n" +
                                     'IMPORTANT: Make sure the NTDS input file only contains user hashes and does not include machine hashes and other lines (Kerberos algo). Below some example commands on how to achieve this:\n' +
                                     ' * From "crackmapexec --ntds" output:\n' +
                                     '     cat crackmapexec-ntds.txt|awk {\'print $5" "$6" "$7" "$8" "$9" "$10\'}|grep -v -e "\$:"|grep -e ":::" > ntds_users_only.txt\n' +
                                     ' * From NTDSUtil + Secretsdump output:\n' +
                                     '     secretsdump.py -ntds ntds.dit -system system.save LOCAL -outputfile output # You may add the "-history" option too\n' +
                                     '     cat output.ntds|grep -v -e "\$:" > ntds_users_only.txt\n' +
                                     ' * From Secretsdump directly (i.e. secretsdump.py domain/admin02:Password123@DC01.domain.local") output:\n' +
                                     '     cat secretsdump.txt|grep -v -e "\$:" -e "\[" -e "\]"|grep -e ":::" > ntds_users_only.txt\n' +
                                     "The \"ntds_users_only.txt\" file is the file you crack in hashcat. After all your cracking efforts, retrieve the hashcat.potfile and use it as the 2nd input to this script.\n\n" +                                     'IMPORTANT: Make sure your hashcat.potfile is fresh and for that "ntds_users_only.txt" file only. Meaning it is not mixed with previously cracked hashes.\n\n' + 
                                     "Example commands:\n" +
                                     "$ python3 " + sys.argv[0] + " --mode 2 --ntds ntds_users_only.txt --hashcat_potfile hashcat.potfile\n")

    parser.add_argument("--mode", dest="mode", required=True, type=int, help="Mode '1': Normal Output. Mode '2': Password Reuse + Statistics Output")
    parser.add_argument("--ntds", dest="ntds", required=True, type=str, help="The NTDS file from which you extracted the users hashes from.\nThis could be the output of ntdsutil+secretsdump or secretsdump directly or 'crackmapexec --ntds' option, etc. Then grepped to filter out machine hashes and other non-user hash related lines.")
    parser.add_argument("--hashcat_potfile", dest="hashcat_potfile", required=True, type=str, help="hashcat.potfile is a file where hashcat stores all its outputs")
    args = parser.parse_args()

    with open(args.ntds, 'r') as ntds_dump, open(args.hashcat_potfile, 'r') as hashcat_cracked_NTLM_hashes:
        if args.mode == 1:
            normal_view(ntds_dump.readlines(), hashcat_cracked_NTLM_hashes.readlines())
        elif args.mode == 2:
            password_reuse_view(ntds_dump.readlines(), hashcat_cracked_NTLM_hashes.readlines())
        else:
            print("[-] Invalid mode: %s" % args.mode)
            sys.exit(1)

if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    ellapsed_time = round(time.perf_counter() - start_time, 2)
    print(f'\n\nFinished in {ellapsed_time} seconds(s)')
