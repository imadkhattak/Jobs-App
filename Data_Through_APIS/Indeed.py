import asyncio
from playwright.async_api import async_playwright
import random
import time
import re
from bs4 import BeautifulSoup

jobs_link_list = []

with open("../user_agents.txt", "r") as f:
    user_agents = [ua.strip() for ua in f.readlines()]


async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent=random.choice(user_agents),
            viewport={"width": 1280, "height": 800},
            locale="en-US"
        )

        page = await context.new_page()

        url = "https://www.indeed.com"  

        await page.goto(url, wait_until="load", timeout=10000)
        time.sleep(10)
        await browser.close()

asyncio.run(run())
