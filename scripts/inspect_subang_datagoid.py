import asyncio
import json
import os
from playwright.async_api import async_playwright

async def inspect_subang_datagoid():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Track all network requests
        page.on("request", lambda req: print(">> REQ:", req.url))
        page.on("response", lambda resp: print("<< RESP:", resp.status, resp.url))
        
        url = "https://data.go.id/dataset/dataset/produktivitas-jagung-menurut-kecamatan-di-kabupaten-subang"
        print(f"Opening {url}...")
        await page.goto(url, wait_until="networkidle")
        
        # Take a screenshot to inspect
        os.makedirs("reports/dataset_audit/figures", exist_ok=True)
        await page.screenshot(path="reports/dataset_audit/figures/subang_datagoid_page.png")
        print("Screenshot saved to reports/dataset_audit/figures/subang_datagoid_page.png")
        
        # Try clicking any download button
        buttons = await page.query_selector_all("button")
        for btn in buttons:
            txt = (await btn.inner_text()).strip()
            print("Button:", txt)
            if "unduh" in txt.lower() or "download" in txt.lower():
                print("Clicking button:", txt)
                await btn.click()
                await page.wait_for_timeout(3000)
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect_subang_datagoid())
