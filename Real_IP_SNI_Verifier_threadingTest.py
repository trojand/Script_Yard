import time
import requests
import logging
import argparse
import concurrent.futures
import urllib3
from bs4 import BeautifulSoup


# Install dependencies: `pip install forcediphttpsadapter`
# Source: https://github.com/Roadmaster/forcediphttpsadapter
from forcediphttpsadapter.adapters import ForcedIPHTTPSAdapter


# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)


def main():
    log = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description="Description:\nA quick dirty script to try to find/confirm the real IP Address of a website behind a CDN by requesting for an actual resource from the website and confirming its contents.\n" +
                                     "Sure you could use curl and just put the \"Host: example.com\" header but most CDNs and cloud hosting providers usually use SNI." +
                                     "IMPORTANT: Make sure to edit the headers in the code. I usually use Burp Suite's \"Copy As Python-Requests\" plugin and save it using \"Copy as requests\" when right clicking on the Repeater or Proxy tab.\n\n" +
                                     "Example commands:\n" +
                                     "$ python3 Real_IP_SNI_Verifier.py --domain maps.google.com --path /landing/transit/js/transit_directions.min.js --ip 74.125.24.102 --keyword \"mapTypeId:google.maps.MapTypeId.ROADMAP\" --range-start 46 --range-end 49\n" +
                                     "$ python3 Real_IP_SNI_Verifier.py --domain maps.google.com --path /landing/transit/js/transit_directions.min.js --ip $(dig +short maps.google.com|head -n 1) --keyword \"mapTypeId:google.maps.MapTypeId.ROADMAP\"")
    parser.add_argument("-v", dest="verbose", action="store_true",
                        default=False, help="Verbose mode")
    parser.add_argument(
        "--ip", dest="ip", required=True, type=str, help="The subnet which you suspect the real IP Address might be in (A non CDN IP Address).\nIn some cases, this is an IP Address within the country where the company is based (Possibly hosted within their infrastructure).\nFor testing purposes, put the CDN IP Address.\nPaste the whole IP Address (i.e. 216.58.207.46)")
    parser.add_argument(
        "--domain", dest="domain", required=True, type=str, help="Target domain/subdomain. Example:\n- google.com\n- www.google.com\n- mail.google.com")
    parser.add_argument("--path", dest="path", required=True, type=str,
                        help="Path or pattern or directory+path or directory+document. Make sure this is unique to your website to avoid false positives. Example:\n- /index.html\n- /web_app/webpage.html\n- /images/imanimage.png\n- /web_app/documens/iamadoc.pdf\n- /session_handler_are_cool.aspx")
    parser.add_argument(
        "--keyword", dest="keyword_to_find", required=True, type=str, help="Keyword to find within the response's contents. This will confirm whether we are looking at the right page.")
    parser.add_argument(
        "--range-start", dest="range_start", required=False, type=int, default=1, help="Range start. Common range = 1-255. Default=1")
    parser.add_argument(
        "--range-end", dest="range_end", required=False, type=int, default=255, help="Range end. Common range = 1-255. Default=255")
    args = parser.parse_args()
    subnet_list = args.ip.split(".")
    subnet = str(subnet_list[0]+"."+subnet_list[1]+"."+subnet_list[2]+".")
    possible_matches = []

    # Configure Logging Verbosity
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    log.debug("Args: %s", args)
    log.info("Testing IP range: %s%s-%s for domain: \"%s\" with path \"%s\"",
             subnet, args.range_start, args.range_end, args.domain, args.path)

    # Here be Burp headers from the plugin "Copy as Python-Requests". Paste your own and replace the args.domain, args.path as seen below. (Estimate of 2-3 paramters only)
    ###########################################################################################################################
    ############################################# START - Edit HEADERS  #######################################################
    burp0_url = "https://" + args.domain + args.path
    burp0_headers = {"Host": args.domain, "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4280.88 Safari/532.36 OPR/ 73.0.3856.284", "Accept": "application/json",
                     "Accept-Language": "en-US,en", "Accept-Encoding": "gzip, deflate", "X-Requested-With": "XMLHttpRequest", "DNT": "1", "Connection": "close"}
    ############################################# END - Edit HEADERS here #####################################################
    ###########################################################################################################################

    with concurrent.futures.ThreadPoolExecutor() as executor:
        possible_matches = [executor.submit(web_request, [burp0_url, burp0_headers, args.domain, args.path,
                                                          subnet, number, args.keyword_to_find, log]) for number in range(int(args.range_start), int(args.range_end)+1)]

    # Print possible matches
    print("\n\n================================================\nPossibe Matches:")
    for ip in concurrent.futures.as_completed(possible_matches):
        print(ip.result())


# def web_request(burp0_url, burp0_headers, domain, path, subnet, number, keyword_to_find, log):
def web_request(request_args):
    burp0_url = request_args[0]
    burp0_headers = request_args[1]
    domain = request_args[2]
    path = request_args[3]
    subnet = request_args[4]
    number = request_args[5]
    keyword_to_find = request_args[6]
    log = request_args[7]
    ip = subnet+str(number)
    print(ip, end=" --- ")
    session = requests.Session()
    session.mount("https://"+domain, ForcedIPHTTPSAdapter(dest_ip=ip))
    try:
        response = session.get(burp0_url, headers=burp0_headers, verify=False, timeout=5)
        try:
            print("Response Code: " + str(response.status_code), end=' --- ')
            try:
                parsed_html = BeautifulSoup(response.content, 'html.parser')
                print("Webpage Title: " + str(parsed_html.title))
            except Exception as e:
                print("Response not HTML")
                log.debug("Exception: %s" % e)
        except Exception as e:
            print("Could not print response \n%s" % e)

        if keyword_to_find in response.content.decode('utf-8'):
            print("\n========================================\nPossible Match on [\"" + keyword_to_find +
                  "\"]!\nVerify with this IP manually: %s\nhttp(s)://%s%s\n========================================\n\n" % (ip, domain, path))
            return ip
    except Exception as e:
        print("Timeout")
        log.debug("Exception: %s" % str(e))
    finally:
        session.close()


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    ellapsed_time = round(time.perf_counter() - start_time, 2)
    print(f'Finished in {ellapsed_time} seconds(s)')
