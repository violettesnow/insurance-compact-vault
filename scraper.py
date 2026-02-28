"""
InsuScout ATL: GA SERFF Portal Scraper
Phase 1: Extract insurance rate filings for State Farm and Auto-Owners
"""

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright

# import parser bridge
from parser import parse_insurance_pdf

# Load environment variables
load_dotenv()

SERFF_URL = os.getenv("GA_SERFF_PORTAL_URL", "https://filingaccess.serff.com/sfa/home/ga")
INSURERS_TO_SCRAPE = ["State Farm", "Auto-Owners"]


async def scrape_ga_serff():
    """
    Scrape GA SERFF portal for 2026 rate filings.
    Uses Playwright with slow_mo=500 to prevent "Page Unresponsive" errors.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        
        try:
            # create context that allows downloads automatically
            context = await browser.new_context(accept_downloads=True)
            page = await context.new_page()
            # Stability settings from ARCH.md
            page.set_default_timeout(30000)
            
            print(f"🔗 Connecting to {SERFF_URL}...")
            await page.goto(SERFF_URL, wait_until="networkidle", slow_mo=500)
            
            print("✅ Portal loaded. Starting scrape...")
            
            # TODO: Implement navigation logic
            # 1. Search for each insurer in INSURERS_TO_SCRAPE
            # 2. Find 2026 rate filing documents
            # 3. Download PDF files and parse them
            # 4. Extract rate factors (Age, Zip Code, Vehicle Symbol)
            # 5. Parse multipliers and store in Supabase
            
            # Example download flow (look for 'View' or 'Download Zip File')
            print("⏳ Scrape in progress...")
            # try clicking either link text; adjust logic to your needs
            for link_text in ["View", "Download Zip File"]:
                try:
                    async with page.expect_download() as download_info:
                        await page.click(f"text=^{link_text}$")
                    download = await download_info.value
                    tmp_dir = Path("tmp")
                    tmp_dir.mkdir(exist_ok=True)
                    file_path = tmp_dir / download.suggested_filename
                    await download.save_as(str(file_path))
                    print(f"📥 PDF saved to {file_path}")

                    # hand off to parser
                    try:
                        parsed = parse_insurance_pdf(str(file_path))
                        print(f"🧠 Parsed JSON:\n{parsed}")
                    except Exception as e:
                        print(f"❌ Parser error: {e}")
                    break
                except Exception:
                    # didn't find this link text or download failed, try next
                    continue
            await page.wait_for_timeout(2000)  # allow time to observe
            
        finally:
            await browser.close()
            print("🏁 Scrape complete.")


if __name__ == "__main__":
    print("🚀 InsuScout ATL Scraper Starting...\n")
    asyncio.run(scrape_ga_serff())
