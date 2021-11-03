import json
import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from rich.console import Console
from . import utils


console = Console()


def command_capture(args):
    console.print("[cyan]NOTE:[/cyan] if streams are playing but window doesn't closed automatically, then re-run the command")
    console.print("[cyan]INFO:[/cyan] try troubleshooting with [green]--scan-ext m3u8[/green] flag")

    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    
    try:
        driver = webdriver.Chrome(executable_path=args.driver, desired_capabilities=capabilities)
    except TypeError:
        console.print("[red bold]VSDownloadError:[/red bold] use [green]--driver <chromedriver path>[/green] flag")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red bold]{e.__class__.__name__}:[/red bold] {e.__str__()}")
        console.print("[red bold]VSDownloadError:[/red bold] incorrect driver path or unsupported driver version")
        sys.exit(1)
        
    driver.get(args.url)

    logs = []
    while True:
        logs.extend(driver.get_log("performance"))

        if utils.find_urls_by_ext(f"{logs}", args.scan_ext) != []:
            driver.quit()
            break

    m3u8_links = utils.find_urls_by_ext(f"{logs}", "m3u8")
    json_data = {
        'baseurl': utils.find_baseurl_by_urls(m3u8_links, "m3u8") if args.baseurl else None,
        'm3u8_urls': m3u8_links,
    }

    console.print(json_data)

    with open(args.output, "w") as f:
        json.dump(json_data, f, indent=4, sort_keys=True)
