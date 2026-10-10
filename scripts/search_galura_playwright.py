import asyncio
import json
from playwright.async_api import async_playwright

async def search_galura():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        keywords = ["opt", "hama", "penyakit", "kedelai"]
        results = {}
        
        for kw in keywords:
            url = f"https://galura.jabarprov.go.id/api/bigdata/dataset?search={kw}&per_page=10"
            try:
                await page.goto(url, wait_until="networkidle", timeout=20000)
                content = await page.inner_text("body")
                try:
                    data = json.loads(content)
                    items = data.get('data', [])
                    results[kw] = [it.get('title', it.get('name')) for it in items]
                except:
                    results[kw] = "Non-JSON response"
            except Exception as e:
                results[kw] = f"Error: {e}"
        
        await browser.close()
        print(json.dumps(results, indent=2))

asyncio.run(search_galura())
