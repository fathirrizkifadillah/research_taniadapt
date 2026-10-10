import asyncio
import json
import os
from playwright.async_api import async_playwright

async def fetch_more_jabar():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        await page.goto("https://galura.jabarprov.go.id/", timeout=30000, wait_until="networkidle")
        await page.wait_for_timeout(2000)
        
        extra_targets = [
            ("produktivitas_padi_sawah_jabar.json", "https://galura.jabarprov.go.id/api/bigdata/produktivitas-padi-sawah-berdasarkan-kabupatenkota-di-jawa-barat?per_page=1000", "data/raw/DS03_west_java_rice_productivity/"),
            ("produktivitas_padi_ladang_jabar.json", "https://galura.jabarprov.go.id/api/bigdata/produktivitas-padi-ladang-berdasarkan-kabupatenkota-di-jawa-barat?per_page=1000", "data/raw/DS03_west_java_rice_productivity/")
        ]
        
        for fname, url, dest_dir in extra_targets:
            print(f"Fetching {url}...")
            try:
                await page.goto(url, timeout=20000)
                text = (await page.inner_text("body")).strip()
                if text.startswith("{") or text.startswith("["):
                    os.makedirs(dest_dir, exist_ok=True)
                    target_path = os.path.join(dest_dir, fname)
                    with open(target_path, "w", encoding="utf-8") as fp:
                        fp.write(text)
                    print(f"  -> Saved {len(text)} chars to {target_path}")
                else:
                    print(f"  -> Non-JSON: {text[:100]}")
            except Exception as e:
                print("  -> Error:", e)
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_more_jabar())
