import logging
from typing import Dict, Any

from app.playwright_agent.browser import BrowserManager
from app.playwright_agent.actions import LeetCodeActions
from app.playwright_agent.parser import LeetCodeParser

logger = logging.getLogger(__name__)

class LeetCodeAgent:
    def __init__(self, headless: bool = False):
        self.browser_manager = BrowserManager(headless=headless)
        self.actions = None
        self.parser = None

    async def initialize(self):
        _, _, page = await self.browser_manager.start()
        self.actions = LeetCodeActions(page)
        self.parser = LeetCodeParser(page)

    async def close(self):
        await self.browser_manager.close()

    async def extract_problem(self, url: str) -> Dict[str, Any]:
        """Navigate to a problem and extract its details."""
        if not self.actions or not self.parser:
            raise Exception("Agent not initialized")
            
        await self.actions.navigate_to(url)
        data = await self.parser.extract_problem_data()
        data["url"] = url
        
        # Extract slug
        slug = url.rstrip("/").split("/")[-1]
        data["slug"] = slug
        
        return data

    async def extract_daily_challenge(self) -> Dict[str, Any]:
        """Find the daily challenge and extract its details."""
        if not self.actions or not self.parser:
            raise Exception("Agent not initialized")
            
        url = await self.actions.click_daily_challenge()
        data = await self.parser.extract_problem_data()
        data["url"] = url
        
        # Extract slug
        slug = url.rstrip("/").split("/")[-1]
        data["slug"] = slug
        
        data["daily_challenge"] = True
        return data
