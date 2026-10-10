import asyncio
import json
import os
from playwright.async_api import async_playwright

async def fetch_subang_kecamatan():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Check Galura search for Subang jagung
        search_url = "https://galura.jabarprov.go.id/api/bigdata/produktivitas-jagung-menurut-kecamatan-di-kabupaten-subang?per_page=1000"
        print("Testing direct Galura endpoint for Subang kecamatan...")
        try:
            resp = await page.goto(search_url, timeout=20000)
            text = (await page.inner_text("body")).strip()
            print("Response length:", len(text))
            if text.startswith("{") or text.startswith("["):
                dest = "data/raw/DS05_subang_maize_productivity/produktivitas_jagung_subang_kecamatan.json"
                with open(dest, "w", encoding="utf-8") as fp:
                    fp.write(text)
                print(f"Saved to {dest}")
            else:
                print("Text prefix:", text[:100])
        except Exception as e:
            print("Error:", e)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_subang_kecamatan())
