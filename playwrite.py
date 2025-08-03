import asyncio
from playwright.async_api import async_playwright
import random
import re
from bs4 import BeautifulSoup



jobs_link_list = []

with open("user-agents.txt", "r") as f:
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

        url = "https://www.linkedin.com"  
        await page.goto(url, wait_until="load", timeout=10000)

        await page.get_by_role("link", name=re.compile("Jobs|Search")).nth(0).click()

        await page.wait_for_timeout(1000)

        try:
            await page.get_by_role("button", name="Dismiss").click()
        except:
            pass  

        job_input = page.get_by_placeholder("Search job titles or companies")
        await job_input.click()
        await job_input.fill("Data Scientist")
        await job_input.press("Enter")

        await page.wait_for_timeout(1000)

        location_input = page.get_by_placeholder("Location")
        await location_input.click()
        await location_input.fill("")
        await location_input.fill("Pakistan")
        await location_input.press("Enter")

        await page.wait_for_timeout(1000)

        jobs_link = await page.locator('a.base-card__full-link').evaluate_all("""(links) => links.map(link => link.href)""")

        for job_link in jobs_link[:1]:
            jobs_link_list.append(job_link)
        
        for job in jobs_link_list:
            await page.goto(job, wait_until="load", timeout=10000)

            try:
                await page.get_by_role("button", name="Dismiss").click()
            except:
                pass

            html_content = await page.content()
            
            soup = BeautifulSoup(html_content, "html.parser")

            job_details = soup.find("div", class_="top-card-layout__entity-info-container flex flex-wrap papabear:flex-nowrap")
            if job_details:
                job_title = job_details.find("h1").get_text(strip=True)
                company_name = job_details.find("a", class_="top-card-layout__second-subline font-sans text-sm leading-open text-color-text-low-emphasis mt-0.5").get_text(strip=True)
                print(f"Job Title: {job_title}, Company: {company_name}")


        await page.wait_for_load_state("load")
        await browser.close()

asyncio.run(run())
