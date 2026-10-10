import asyncio
import json
import os
from playwright.async_api import async_playwright

ENDPOINTS = {
    "DS03_padi": {
        "url": "https://galura.jabarprov.go.id/api/bigdata/produktivitas-padi-berdasarkan-kabupatenkota-di-jawa-barat?per_page=1000",
        "dest": "data/raw/DS03_west_java_rice_productivity/produktivitas_padi_jabar.json"
    },
    "DS05_jagung": {
        "url": "https://galura.jabarprov.go.id/api/bigdata/produktivitas-jagung-berdasarkan-kabupatenkota-di-jawa-barat?per_page=1000",
        "dest": "data/raw/DS05_subang_maize_productivity/produktivitas_jagung_jabar.json"
    },
    "DS06_sbs": {
        "url": "https://galura.jabarprov.go.id/api/bigdata/produktivitas-sayuran-dan-buah-buahan-semusim-sbs-berdasarkan-komoditi-di-jawa-barat?per_page=1000",
        "dest": "data/raw/DS06_west_java_horticulture/produktivitas_sbs_jabar.json"
    },
    "DS06_sayuran_komoditas": {
        "url": "https://galura.jabarprov.go.id/api/bigdata/produksi-sayuran-berdasarkan-komoditas-di-jawa-barat?per_page=1000",
        "dest": "data/raw/DS06_west_java_horticulture/produksi_sayuran_komoditas_jabar.json"
    }
}

async def fetch_all():
    async with async_playwright() as p:
        # Launch browser with stealth settings
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # First visit main page to establish session/cookies
        print("Visiting home page to establish session...")
        try:
            await page.goto("https://galura.jabarprov.go.id/", timeout=30000, wait_until="networkidle")
            print("Home page title:", await page.title())
        except Exception as e:
            print("Home page load notice:", e)
            
        await page.wait_for_timeout(3000)
        
        for key, item in ENDPOINTS.items():
            url = item["url"]
            dest = item["dest"]
            print(f"\nFetching {key} from {url}...")
            try:
                resp = await page.goto(url, timeout=30000)
                content = await page.content()
                # Check if JSON
                text = await page.inner_text("body")
                text = text.strip()
                if text.startswith("{") or text.startswith("["):
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    with open(dest, "w", encoding="utf-8") as fp:
                        fp.write(text)
                    print(f"  -> SUCCESS! Saved {len(text)} chars to {dest}")
                else:
                    print(f"  -> Non-JSON response ({len(text)} chars). Prefix: {text[:100]}")
            except Exception as e:
                print(f"  -> ERROR fetching {key}:", e)
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_all())
