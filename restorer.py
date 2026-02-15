import json
import asyncio
import os
import time
import sys
import easygui
import colorama
from colorama import Fore
from pystyle import Colors, Colorate, Center
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

colorama.init(autoreset=True)

def print_header():
    os.system("cls" if os.name == "nt" else "clear")
    text = """
███████╗███╗   ██╗ █████╗ ██████╗ ██╗   ██╗
██╔════╝████╗  ██║██╔══██╗██╔══██╗╚██╗ ██╔╝
███████╗██╔██╗ ██║███████║██████╔╝ ╚████╔╝ 
╚════██║██║╚██╗██║██╔══██║██╔═══╝   ╚██╔╝  
███████║██║ ╚████║██║  ██║██║        ██║   
╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝        ╚═╝"""
    
    try:
        terminal_width = os.get_terminal_size().columns
    except:
        terminal_width = 80

    lines = text.splitlines()
    max_len = max(len(line) for line in lines)
    
    centered_lines = []
    for line in lines:
        left_padding = (terminal_width - max_len) // 2
        centered_lines.append((" " * left_padding) + line.ljust(max_len))
    
    full_centered_text = "\n".join(centered_lines)
    
    print()
    print(Colorate.Vertical(Colors.purple_to_blue, full_centered_text))
    
    version_text = f"Snapy v.1.0.1 by Beatsbyluca"
    print(version_text.center(terminal_width))
    print()

def log(msg, status="info"):
    timestamp = f"{Fore.LIGHTBLACK_EX}[{time.strftime('%H:%M:%S')}]{Fore.RESET}"
    if status == "info":
        prefix = f"{Fore.BLUE}[INFO]{Fore.RESET}"
    elif status == "success":
        prefix = f"{Fore.GREEN}[SUCCESS]{Fore.RESET}"
    elif status == "error":
        prefix = f"{Fore.RED}[ERROR]{Fore.RESET}"
    elif status == "wait":
        prefix = f"{Fore.YELLOW}[WAIT]{Fore.RESET}"
    
    print(f"{timestamp} {prefix} {msg}", flush=True)

async def restore_streak():
    print_header()
    log("Initializing Snapy...", "info")
    
    try:
        if not os.path.exists('config.json'):
            log("config.json not found!", "error")
            easygui.msgbox("Error: config.json not found!", "Error")
            return
            
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            log("Configuration loaded.", "success")
            
        friends = config.get("friends", [])
        if not friends and config.get("friend_username"):
            friends = [config["friend_username"]]
            
        if not friends:
            log("No friends found in config!", "error")
            easygui.msgbox("Error: No friends list found in config.json!", "Error")
            return

        log(f"Found {len(friends)} friends to process.", "info")

    except Exception as e:
        log(f"Configuration error: {e}", "error")
        return

    try:
        async with async_playwright() as p:
            log("Starting Snapy Engine...", "info")
            browser = await p.chromium.launch(headless=False)
            
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            
            await Stealth().apply_stealth_async(page)

            async def block_resources(route):
                try:
                    url = route.request.url.lower()
                    if route.request.resource_type == "image":
                        await route.continue_()
                        return

                    if route.request.resource_type in ["media", "font"]:
                        await route.abort()
                    elif "google-analytics" in url or "analytics" in url:
                        await route.abort()
                    else:
                        await route.continue_()
                except:
                    pass

            await page.route("**/*", block_resources)

            for idx, friend in enumerate(friends, 1):
                try:
                    log(f"Processing {idx}/{len(friends)}: {Fore.CYAN}{friend}{Fore.RESET}", "info")
                    
                    url = "https://help.snapchat.com/hc/en/requests/new?co=true&ticket_form_id=149423"
                    await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                    
                    try:
                        await page.wait_for_selector("#new_request", timeout=10000)
                    except:
                        pass

                    try:
                        cookie_selectors = ["#onetrust-accept-btn-handler", "button:has-text('Alle akzeptieren')", "button:has-text('Accept all')"]
                        for selector in cookie_selectors:
                            if await page.locator(selector).is_visible(timeout=500):
                                await page.click(selector)
                                break
                    except:
                        pass

                    async def fill_field(selectors, value, name):
                        if not value or value == "DEIN_NICKNAME":
                            return False
                        for selector in selectors:
                            try:
                                loc = page.locator(selector)
                                if await loc.count() > 0:
                                    target = loc.first
                                    await target.scroll_into_view_if_needed(timeout=1000)
                                    await target.fill(value, timeout=2000)
                                    return True
                            except:
                                continue
                        try:
                            label_loc = page.get_by_label(name, exact=False)
                            if await label_loc.count() > 0:
                                await label_loc.first.fill(value, timeout=2000)
                                return True
                        except:
                            pass
                        return False

                    await fill_field(["#request_anonymous_requester_email", "input[type='email']"], config['email'], "Email-Adresse")
                    await fill_field(["#request_custom_fields_24281229", "input[name*='user']"], config['username'], "Nutzername")
                    await fill_field(["#request_custom_fields_24335325"], config['email'], "Extra E-Mail")
                    await fill_field(["#request_custom_fields_24369716", "input[type='tel']"], config['phone'], "Handynummer")
                    await fill_field(["#request_custom_fields_24369736"], friend, "Freund")

                    log(f"Fields ready for {friend}. Solve CAPTCHA & Submit!", "wait")
                    
                    success = False
                    while not success:
                        try:
                            success_texts = ["Wir haben deine Anfrage erhalten", "Erfolgreich", "Vielen Dank", "Successfully", "Thank you"]
                            for text in success_texts:
                                if await page.locator(f"text={text}").is_visible(timeout=500):
                                    log(f"Success for {friend}!", "success")
                                    success = True
                                    break
                            if not success:
                                await asyncio.sleep(1)
                        except Exception as e:
                            if "closed" in str(e).lower():
                                log("Browser window closed.", "error")
                                return
                            await asyncio.sleep(1)
                    
                    if idx < len(friends):
                        log("Moving to next friend in 3s...", "info")
                        await asyncio.sleep(3)
                
                except Exception as e:
                    if "closed" in str(e).lower():
                        log("Navigation failed: Browser closed.", "error")
                        return
                    log(f"Error during processing {friend}: {e}", "error")
                    if "target page, context or browser has been closed" in str(e).lower():
                        return

            log("All tasks completed!", "success")
            easygui.msgbox(f"Snapy COMPLETED!\nProcessed {len(friends)} friends.", "Snapy")

    except Exception as e:
        if "closed" in str(e).lower():
             log("Snapy Engine stopped (Browser closed).", "info")
        else:
            log(f"Critical error: {e}", "error")
            easygui.msgbox(f"Error: {e}", "Critical Error")
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        asyncio.run(restore_streak())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Snapy terminated.")
