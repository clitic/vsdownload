import json
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from . import utils


def command_capture(args):
    print("note: if streams are playing but window doesn't closed automatically, then re-run the command")
    print("troubleshoot with flag: --scan-ext m3u8")
    
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    driver = webdriver.Chrome(executable_path=args.driver, desired_capabilities=capabilities)
    driver.get(args.url)

    logs = []
    while True:
        logs.extend(driver.get_log("performance"))

        if utils.find_urls_by_ext(f"{logs}", args.scan_ext) != []:
            driver.quit()
            break

    m3u8_links = utils.find_urls_by_ext(f"{logs}", "m3u8")
    json_data = {"m3u8_urls": m3u8_links}
    json_data["blob"] = utils.find_blob_by_urls(m3u8_links, "m3u8")

    pprint(json_data)

    with open(args.output, "w") as f:
        json.dump(json_data, f, indent=4, sort_keys=True)
