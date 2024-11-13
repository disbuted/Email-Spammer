# WORKS ON ALL OF THESE, YET TO TEST MORE MAINSTREAM EMAIL SERVICE PROVIDERS 
# https://mail.tm/en/
# https://mail.gw/en/
# https://temp-mail.io/en
# https://tempmailo.com/

import asyncio, aiohttp, time, re, random, string, itertools, os, json, pystyle, fade, sys, colorama, threading
from pystyle import Colors, Colorate, Center
from colorama import Fore, Style, init

# need to move this configuration to an external config.json file
size = 600 # Threads + Process / Iteration
cap = None  # thread limit / set to None for unlimited. Only go higher than 500 is u got a fucking beast of a pc CPU wise.
random_threads = True # True = Threads Random. False = They Arent Random
timeout = aiohttp.ClientTimeout(total=20)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def update_title():
    while True:
        title = "[t.me/influenceable] " + ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=30))
        os.system(f"title {title}" if os.name == 'nt' else f"\033]0;{title}\007")
        time.sleep(0.1)   

    # skidded from chatgpt
def generate_email_variants(email):
    username, domain = email.split("@")
    variants = []

    funnylimit = 5000

    for i in range(1, len(username)):
        if len(variants) >= funnylimit:
            break
        for combo in itertools.combinations(range(1, len(username)), i):
            if len(variants) >= funnylimit:
                break
            variant = username
            for index in reversed(combo):
                if len(variants) >= funnylimit:
                    break
                variant = variant[:index] + "." + variant[index:]
            variants.append(variant)

    data = list(sorted(dict.fromkeys([variant + "@" + domain for variant in variants])))
    results = [email] + random.sample(data, k=len(data))
    return results

def generate(length: int = 5):
    ba = bytearray(os.urandom(length)) 
    for i, b in enumerate(ba):
        ba[i] = ord("a") + b % 26
    return str(time.time()).replace(".", "") + ba.decode("ascii")

def validate_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)

def is_html_string(text: str) -> bool:
    return bool(re.compile(r"<[^>]+>").search(text))

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def divide():
    print("-" * 40)

progress = 0

def update_progress():
    global progress
    progress += 1
    decimal = progress / total
    amount = 30
    white = "█" * int(amount - int((1 - decimal) * amount))
    black = "░" * int(amount - int(decimal * amount))
    print(
        f"⚡ {progress}/{total} {round(decimal*100, 1):.1f}%「{white}{black}」", end="\r"
    )
    if progress >= total:
        print("\r")

status_codes = {}
working = []

async def fetch(
    session: aiohttp.ClientSession,
    sub: str,
    info,
    name: str = None,
    testing: bool = False,
):
    def fix(lol):
        try:
            required = isinstance(lol, (dict, tuple, list))
            result = json.dumps(lol) if required else lol
            result = (
                result.replace("{email}", sub)
                .replace("{password}", password)
                .replace("{random}", generate())
                .replace("{username}", generate())
                .replace(
                    "{frenchnumber}",
                    str(random.randint(100_000_000, 999_999_999)).replace(
                        "{timestamp}", str(int(time.time()))
                    ),
                )
            )
            result = json.loads(result) if required else result
        except Exception:
            import traceback

            print(traceback.format_exc())
        return result

    try:
        url = fix(info.get("url"))
        method = info.get("method", "POST").upper()
        js = info.get("json", None)
        if js is not None:
            js = fix(js)
        data = info.get("data", None)
        if data is not None:
            data = fix(data)
        params = info.get("params", None)
        if params is not None:
            params = fix(params)
        headers = info.get("headers", None)
        cookies = info.get("cookies", None)
        async with session.request(
            method=method,
            url=url,
            json=js,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
        ) as resp:
            if status_codes.get(name) is None:
                status = resp.status
                resp = await resp.text()
                evaluation = "FAILURE" if status >= 400 else "SUCCESS"
                if is_html_string(resp):
                    words = [
                        "denied",
                        "error",
                        "bad request",
                        "bad",
                        "wrong",
                        "forbidden",
                    ]
                    if any([word in evaluation.lower() for word in words]):
                        evaluation = "FAILURE"
                        status = 400
                resp = (
                    resp.strip()
                    .replace("\n", "")
                    .replace("\r", "")
                    .replace("\t", "")[:1000]
                )
                if status_codes.get(name) is None:
                    status_codes[name] = {
                        "method": method,
                        "status": status,
                        "evaluation": evaluation,
                        "url": url,
                        "resp": resp,
                    }
    except (Exception, asyncio.CancelledError, AssertionError, TimeoutError) as err:
        pass
    return update_progress()

text = """   
                        ███████╗██████╗  █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗ 
                        ██╔════╝██╔══██╗██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗
                        ███████╗██████╔╝███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝
                        ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗
                        ███████║██║     ██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║
                        ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
                                                                    t.me/influenceable
"""

# refer to here if u wann change the color :3 
# https://github.com/venaxyt/fade

faded_text = fade.pinkred(text)

# just come basic [-] for color coding with different meanings!
# makes my life so much fucking easier

yellow_dash = f"{Fore.YELLOW}-{Style.RESET_ALL}"
red_dash = f"{Fore.RED}-{Style.RESET_ALL}"
green_dash = f"{Fore.GREEN}-{Style.RESET_ALL}"

async def main():
    threading.Thread(target=update_title, daemon=True).start()
    print(Center.XCenter(faded_text))
    try:
        async with aiohttp.ClientSession() as session:
            directory = os.path.dirname(__file__)
            try:
                with open(os.path.join(directory, "functions.json"), "r") as file:
                    functions = json.load(file)
            except Exception:
                # no functions.json found in the directory, gonna load via async session.get
                print(f"\r[{red_dash}] No Data Found, Refering To Backup Data")
                time.sleep(0.5)
                clear_console()
                print(Center.XCenter(faded_text)) 
                print(f"\r[{yellow_dash}] Connecting now...")
                time.sleep(3)
                async with session.get(
                    "https://raw.githubusercontent.com/Inkthirsty/cute-email-spammer/main/functions.json"
                ) as resp:
                    functions = json.loads(await resp.text())
                    clear_console()
                    print(Center.XCenter(faded_text)) 
                    # Connection successful! If error, will go to error string and close 
                    print(f"\r[{green_dash}] Backup Valid! Program Should Be Working Now.")
                    time.sleep(1.5)
                    clear_console()
                    print(Center.XCenter(faded_text)) 

            functions = {i: functions[i] for i in list(functions)[:-1]}
            global progress, total, password, threads
            password = ""
            # randomising password or something idfk
            samples = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
            for _ in samples:
                password += "".join(random.sample(_, k=5))
            password = "!" + "".join(random.sample(password, k=len(password)))

            email = None
            while True:
                email = input(f"\r[{yellow_dash}] Enter Your Email Address: ").strip().lower()
                if validate_email(email):
                    break
                clear_console()
                print(Center.XCenter(faded_text)) 
                # invalid email or the user is just slow :d
                print(f"\r[{red_dash}] That isnt a fucking email address you retard")
                time.sleep(2)
                sys.exit()

            variants = generate_email_variants(email)
            threads = None
            while True:
                try:
                    limit = clamp(len(variants), 1, cap or float("inf"))
                    threads = input(f"\r[{yellow_dash}] threads per batch (1-{limit}): ")
                    if threads == "":
                        threads = cap // 2
                    threads = clamp(int(threads), 1, limit)
                    break
                except:
                    clear_console()
                    print(Center.XCenter(faded_text)) 
                    # Amount of threads needed, not a word, just numbers :3
                    print(f"\r[{red_dash}] Are you fucking retarded? That isnt a number 🤬🤬")
                    time.sleep(3)
                    sys.exit()

            variants = random.sample(variants, k=threads)
            total = len(functions) * len(variants)
            divide()
            # Debug info
            print(f"\r[{green_dash}] Useless Infomation Here:")
            global debug
            debug = threads == 1
            info = {
                "EMAIL": email,
                "PASSWORD": password,
                "THREADS": threads,
                "DEBUG MODE": debug,
            }
            print("\n".join([f"{k.upper()}: {v}" for k, v in info.items()]))
            divide()
            if debug:
                testlast = (
                    input(f"\r[{yellow_dash}] Debug Mode is active, type Y to only test the last function")
                    .strip()
                    .lower()
                    == "y"
                )
                if testlast:
                    total = 1
                    functions = dict([next(reversed(functions.items()))])
            else:
                # Testing endpoints, need to ask max for more soon or the tutorial on how to get valid ones :(
                print(f"\r[{green_dash}] Pretesting endpoints to grant 2 minutes of life ♥ ♥ ♥!!!")
                test_tasks = [
                    asyncio.create_task(fetch(session, email, values, name, True))
                    for name, values in functions.items()
                ]
                total = len(test_tasks)
                try:
                    await asyncio.gather(*test_tasks)
                except Exception:
                    pass
                working = [k for k, v in status_codes.items() if v.get("status") < 400]
                print(f"\r[{yellow_dash}] {len(working)} of {len(test_tasks)} endpoints may be working")
                functions = {k: v for k, v in functions.items() if k in working}
                variants = variants[1:]
                print(f"\r[{green_dash}] {len(test_tasks):,} endpoints have been tested -- {round((len(functions)/len(test_tasks))*100, 1):.1f}% success rate")
                total = len(functions) * len(variants)
                progress = 0
            with open(
                os.path.join(directory, "results.txt"), "w", encoding="utf-8"
            ) as file:
                e = "\n\n".join(
                    [
                        (
                            f"{name or 'Unknown'} -- {values.get('method')} -- {values.get('status')} -- {values.get('evaluation')}\nURL: {values.get('url')}\nRESPONSE: {values.get('resp')}"
                        )
                        for name, values in status_codes.items()
                    ]
                )
                file.write(e)
            print(f"\r[{green_dash}] Initializing threads...")
            start = time.time()
            global timeout
            timeout = aiohttp.ClientTimeout(total=3)
            queue = [
                (session, sub, values, name)
                for sub in variants
                for name, values in functions.items()
            ]
            if random_threads == True:
                queue = random.sample(queue, k=len(queue))
                # All went successful and is not running the process
            print(f"\r[{green_dash}] Sending Emails!")
            for j in range(0, len(queue), size):
                tasks = [
                    asyncio.create_task(fetch(*task)) for task in queue[j : j + size]
                ]
                try:
                    await asyncio.gather(*tasks)
                except Exception:
                    pass
                await asyncio.sleep(0)
            taken = time.time() - start
            minutes, seconds = int(taken // 60), int(taken % 60)
            print(f"\r[{green_dash}] Attempted to send {total:,} emails in {minutes}:{seconds:02}")
            print(f"\r[{yellow_dash}] remember that some emails will be delayed or never arrive")
            async with session.get(
                "https://raw.githack.com/Inkthirsty/cute-email-spammer/main/adjectives.json" # Valid working CDN as of 11/11/2024 
            ) as resp:
                words = ", ".join(random.sample(await resp.json(), k=5))
            prefix = "an" if words[0] in "aeiou" else "a"
            print(f"\r[{green_dash}] I hope you have {prefix} {words} day ^_^")
            time.sleep(2)
            sys.exit()
            with open(
                os.path.join(directory, "results.txt"), "w", encoding="utf-8"
            ) as file:
                e = "\n\n".join(
                    [
                        (
                            f"{name or 'Unknown'} -- {values.get('method')} -- {values.get('status')} -- {values.get('evaluation')}\nURL: {values.get('url')}\nRESPONSE: {values.get('resp')}"
                        )
                        for name, values in status_codes.items()
                    ]
                )
                file.write(e)
    except Exception as error:
        print(error)
        # Program died due to an error :(
        print(f"\r[{red_dash}] It seems like the program has died before pope francis :(( womp womp")
        await asyncio.sleep(5)  
        time.sleep(2)
        sys.exit()

if __name__ == "__main__":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass
    asyncio.run(main())
