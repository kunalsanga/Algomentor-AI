import logging
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class BrowserManager:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self._playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def start(self) -> Tuple[Browser, BrowserContext, Page]:
        logger.info(f"Starting browser (headless={self.headless})")
        self._playwright = await async_playwright().start()
        
        # Launch Chromium. LeetCode is heavy, we set some standard viewport and agent to avoid bot detection
        self.browser = await self._playwright.chromium.launch(
            headless=self.headless,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        self.page = await self.context.new_page()
        
        # Mask automation scripts
        await self.page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return self.browser, self.context, self.page

    async def close(self):
        logger.info("Closing browser")
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self._playwright:
            await self._playwright.stop()
