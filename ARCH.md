# Technical Architecture
- **Scraper:** Python + Playwright (to navigate the GA SERFF portal).
- **Intelligence:** LLM-based PDF Parsing (to turn messy insurance tables into JSON).
- **Database:** Supabase (PostgreSQL) to store extracted rate factors.
- **Frontend:** Next.js + Tailwind CSS (using shadcn/ui for an Apple-style look).
- **Core Logic:** A local "Rating Engine" function that multiplies Base Rates by Age and Vehicle factors.
- **Scraper Stability:** Use `slow_mo=500` in Playwright and implement `wait_for_load_state("networkidle")` after every click to prevent "Page Unresponsive" errors on the GA SERFF portal.