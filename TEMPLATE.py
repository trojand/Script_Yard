import random
import requests
import logging
import argparse
import time
import json
import sys
import re
import asyncio
from aiohttp import ClientSession
# from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from tqdm import tqdm, trange

# Create and configure logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

# Suppress only the single warning from urllib3 needed.
# requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def main():
    log = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Description:\nThis is a template/skeleton script to avoid typing a lot of basic stuff.\n" +
                                     "IMPORTANT: Make sure to update this as this script does not do anything.\n" +
                                     "Also, delete the functions below once done as they are just tips and reminders.\n" +
                                     "Message me if you have any suggestions to improve this template/skeleton script.\n" +
                                     "Example commands:\n" +
                                     "$ python3 " + sys.argv[0] + " --ip 1.2.3.4 --range-start-variable 30\n")
    parser.add_argument("-v", dest="verbose", action="store_true",
                        default=False, help="Verbose/Debug mode")
    parser.add_argument(
        "--ip", dest="ip", required=True, type=str, help="The subnet:\n Example: XXX.XXX.XXX.46")
    parser.add_argument(
        "--range-start-variable", dest="range-start-variable", required=False, type=int, default=1, help="Range start. Default = 1")
    args = parser.parse_args()

    # Configure Logging Verbosity
    if args.verbose:
        logging.basicConfig(filename="./python-debug.log", format=LOG_FORMAT, level=logging.DEBUG)
    else:
        logging.basicConfig(filename="./python-info.log", format=LOG_FORMAT, level=logging.INFO)

    log.debug("DEBUG: Args: %s", args)
    log.info("INFO: Args: % s" % args.ip)
    
    # Requests
    proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}
    headers = {'User-Agent': 'Mozilla'}
    data = "id=1"
    r = requests.get('https://google.com/', headers=headers, verify=False, proxies=proxies)
    # r = requests.post('https://google.com/', headers=headers, verify=False, proxies=proxies, data=data)
    print('Status_code is: ', r.status_code)
    print('Headers are: ', r.headers)
    print('Cookies are: ', r.cookies)
    print('Text is: ', r.text)
    

if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    ellapsed_time = round(time.perf_counter() - start_time, 2)
    print(f'Finished in {ellapsed_time} seconds(s)')


def general_Tips_And_Tricks():
    """ Tips and Tricks, mostly from https://www.youtube.com/watch?v=C-gEQdGVXbk"""
    # - Context manager
    try:
        with open('test.txt', 'r') as f:
            text_file = f.read()
        print(text_file)
    except Exception:
        pass

    # - Enumerate
    names = ['test', 'teser']
    for index, name in enumerate(names, start=1):
        print(index, name)

    # - Zip
    names = ['test', 'teser']
    namez = ['ztest', 'zteser']
    for name, namz in zip(names, namez):
        print(name, namz)

    # - Unpack
    for name, _ in zip(names, namez):
        print(name)
    a, b, *c = (1, 2, 3, 4, 5)
    print(a, b, c)
    a, b, *c, d = (1, 2, 3, 4, 5)
    print(a, b, c, d)
    a, b, *_, d = (1, 2, 3, 4, 5)
    print(a, b, d)

    # Setattr/Getattr
    class Person():
        pass
    person = Person()
    person_info = {'first': 'Corey', 'last': 'Schafer'}
    for key, value in person_info.items():
        setattr(person, key, value)

    for key in person_info.keys():
        print(getattr(person, key))

    # Get sensitive information from CLI(getpass)
    from getpass import getpass
    password = getpass('Type in password: ')

    # python3 -m (module)
    # python3 -m venv my_env

    # help/dir
    # import smtpd
    # help(smtpd)
    # from datetime import datetime
    # dir(datetime)
    # datetime.today
    # datetime.today()
    
    # Progress bar (tqdm)
    with tqdm(desc="Sample description", leave=False, unit=" Requests", total=50) as pbar: # Manual updating
        for i in range(50):
            r = requests.get(url)
            pbar.update()
            # or someFunction(pbar) then pbar.update() there
            if int(r.headers['Content-Length']) == 200:
                pbar.close()
                return r.text
    for i in trange(50): # Might not have leave feature
        print("Do something)
    for i in tqdm(range(50),desc="Sample description", leave=False, unit=" Requests"): # Might not have leave feature
        print("Do something)

def concurrent_threading_tips():
    """
    Tips from @CoreyShafer https://www.youtube.com/watch?v=IEEhzQoKtQU

    Rule:
        threads for IO bound
        multiprocess for CPU bound
    """

    # Synchronous sample
    import time
    start = time.perf_counter()
    general_Tips_And_Tricks()
    finish = time.perf_counter()
    print('Finished in %s seconds(s)' % round(finish-start, 2))

    # Sample thread - Synchronous sample - Manual
    import time
    import threading
    start = time.perf_counter()
    t1 = threading.Thread(target=general_Tips_And_Tricks)
    t2 = threading.Thread(target=general_Tips_And_Tricks)

    t1.start()
    t2.start()

    t1.join()  # To wait for t1 to end before continuing
    t2.join()  # To wait for t2 to end before continuing

    finish = time.perf_counter()
    print('Finished in %s seconds(s)' % round(finish-start, 2))

    # Loop - Manual
    threads = []
    for _ in range(10):
        t = threading.Thread(target=general_Tips_And_Tricks)
        # t = threading.Thread(target=general_Tips_And_Tricks, args=[<value>])
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    # Threadpool executor
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # f1 = executor.submit(general_Tips_And_Tricks,<arg_value>)
        f1 = executor.submit(general_Tips_And_Tricks, 1)
        f2 = executor.submit(general_Tips_And_Tricks, 1)
        print(f1.result())
        print(f2.result())

    # Threadpool executor - Loop
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(general_Tips_And_Tricks, 1) for _ in range(10)]

        for f in concurrent.futures.as_completed(results):
            print(f.result())

    # Threadpool executor - Loop - List - Map
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        secs = [5, 4, 3, 2, 1]
        results = executor.map(general_Tips_And_Tricks, secs)

        for result in results:
            print(result)

    # Real world example. Download images: https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Threading/download-images.py


def concurrent_multiprocessing_tips():
    """
    Multiprocessing tips from https://www.youtube.com/watch?v=fKl2JW_qrso.
    Nearly the same syntax as threading
        Here it makes use of mutliprocessing.Process() instead of threading.Thread()
    Even makes use of concurrent.futures
        Makes use of concurrent.futures.ProcessPoolExecutor() instead of concurrent.futures.ThreadPoolExecutor()

    Rule:
        threads for IO bound
        multiprocess for CPU bound
    """
    # Sample multiprocessing - Synchronous sample - Manual
    import multiprocessing
    start = time.perf_counter()
    p1 = multiprocessing.Process(target=general_Tips_And_Tricks)
    p2 = multiprocessing.Process(target=general_Tips_And_Tricks)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    finish = time.perf_counter()
    print('Finished in %s seconds(s)' % round(finish-start, 2))

    # Processpool executor - Loop
    import concurrent.futures.ProcessPoolExecutor
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(general_Tips_And_Tricks, 1) for _ in range(10)]

        for f in concurrent.futures.as_completed(results):
            print(f.result())

    # Processpool executor - Loop - List - Map
    import concurrent.futures
    with concurrent.futures.ProcessPoolExecutor() as executor:
        secs = [5, 4, 3, 2, 1]
        results = executor.map(general_Tips_And_Tricks, secs)

        for result in results:
            print(result)

    # Demo https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/MultiProcessing/process-images.py


async def myCoroutine(id: int):
    """
    Asyncio function 1
    """
    process_time = random.randint(1, 5)
    await asyncio.sleep(process_time)
    print("Coroutine: {}, has successfully completed after {} seconds".format(id, process_time))


async def async_main():
    """
    Main function in Asyncio Demo
    taken from:
    https://www.youtube.com/watch?v=L3RyxVOLjz8
    https://www.youtube.com/watch?v=6ow7xloFy5s
    """
    tasks = []
    for i in range(10):
        tasks.append(asyncio.ensure_future(myCoroutine(i)))
    await asyncio.gather(*tasks)
    # OR
    tasks = []
    for i in range(10):
        tasks.append(
            asyncio.create_task(
                myCoroutine(i)
            )
        )
    await asyncio.gather(*tasks)
    # OR
    await asyncio.wait([
        myCoroutine(100),
        myCoroutine(10),
        myCoroutine(1)
    ])

    # Three lines below should be indented left
    # To run the async_main() function using event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())
    loop.close()
    # OR a simpler way
    asyncio.run(async_main())


async def async_main_http():
    """
    Asyncio web scraping
    taken from:
    https://www.youtube.com/watch?v=6ow7xloFy5s
    Sample code:
    https://github.com/codingforentrepreneurs/30-Days-of-Python/blob/master/tutorial-reference/Day%2027/ascrape_sema.py
    """

# START of Asyncio POC code

async def sqli_request(session, url, headers, data, proxies):
    """
    HTTP Request function to send SQLi
    """
    async with session.post(url, headers=headers, data=data, proxy=proxies) as response:
        html_body = await response.text()
        return {"statusCode": response.status, "headers": response.headers, "body": html_body, "cookies": response.cookies}


async def sqli_request_sem(sem, session, url, headers, data, proxies):
    """
    Semaphore function
    """
    async with sem:
        sqli_request(session, url, headers, data, proxies)


async def sqli_main():
    # Insert argparse and logging section HERE

    # Variables
    proxies = "http://127.0.0.1:8080"
    headers = {'User-Agent': 'Mozilla', 'Content-Type': 'application/json'}
    protocol = 'http://'
    path = '/someApp/someFile.php'
    data = "id="+args.injection + "&sort=True"
    url = protocol+args.host+path

    sem = asyncio.Semaphore(10)
    async with ClientSession() as session:
        tasks = []
        for i in range(10):
            tasks.append(
                asyncio.create_task(
                    sqli_request_sem(sem, session, url, headers, data, proxies)
                )
            )
        responses = await asyncio.gather(*tasks)

    for r in responses:
        print('Status_code is: ', r.get("statusCode"))
        print('Headers are: ', r.get("headers"))
        print('Cookies are: ', r.get("cookies"))
        # print('Text is: ', r.get("body"))

        errors = re.search("There is an SQL Error", r.get("body"))
        if errors:
            print("There are errors!!! Take a closer look.")
        else:
            print("Nothing to see here.")


if "__SQLI__name__" == "__main__":
    start_time = time.perf_counter()
    asyncio.run(sqli_main())
    ellapsed_time = round(time.perf_counter() - start_time, 2)
    print(f'Finished in {ellapsed_time} seconds(s)')

# END of Asyncio POC code

def regex_tips_python():
    """
    regex tips from https://www.youtube.com/watch?v=sa-TUpSx1JA
    Cheatsheet for general regex
    Snippets taken from https://github.com/CoreyMSchafer/code_snippets/blob/master/Regular-Expressions/snippets.txt

    .       - Any Character Except New Line
    \d      - Digit (0-9)
    \D      - Not a Digit (0-9)
    \w      - Word Character (a-z, A-Z, 0-9, _)
    \W      - Not a Word Character
    \s      - Whitespace (space, tab, newline)
    \S      - Not Whitespace (space, tab, newline)

    \b      - Word Boundary
    \B      - Not a Word Boundary
    ^       - Beginning of a String
    $       - End of a String

    []      - Matches Characters in brackets
    [^ ]    - Matches Characters NOT in brackets
    |       - Either Or
    ( )     - Group

    Quantifiers:
    *       - 0 or More
    +       - 1 or More
    ?       - 0 or One
    {3}     - Exact Number
    {3,4}   - Range of Numbers (Minimum, Maximum)


    #### Sample Regexs ####

    Email regex:
    [a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+

    URL regex:
        Basic: https?://(www\.)?\w+\.\w+
        Grouping: https?://(www\.)?(\w+)(\.\w+)
            Replace: $1$2$3\n$0
    """
