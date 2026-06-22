import logging
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)

class LeetCodeActions:
    def __init__(self, page: Page):
        self.page = page

    async def navigate_to(self, url: str, wait_until: str = "domcontentloaded"):
        logger.info(f"Navigating to {url}")
        try:
            await self.page.goto(url, wait_until=wait_until, timeout=30000)
        except PlaywrightTimeoutError:
            logger.error(f"Timeout while navigating to {url}")
            raise

    async def check_is_logged_in(self) -> bool:
        """Check if user is logged into LeetCode by looking for the avatar/profile element"""
        try:
            # Wait a bit for the navbar to load
            await self.page.wait_for_selector("nav", timeout=5000)
            
            # Check for sign-in button or user avatar
            # Usually Leetcode has a "Sign in" text on the navbar if logged out
            sign_in_text = await self.page.query_selector("text='Sign in'")
            if sign_in_text:
                logger.info("User is NOT logged in")
                return False
                
            logger.info("User appears to be logged in")
            return True
        except Exception as e:
            logger.warning(f"Could not determine login status: {e}")
            return False

    async def click_daily_challenge(self):
        """Navigate to the daily challenge using LeetCode's GraphQL API"""
        logger.info("Looking for daily challenge link via GraphQL")
        try:
            query = """
            query questionOfToday {
                activeDailyCodingChallengeQuestion {
                    link
                }
            }
            """
            
            response = await self.page.context.request.post(
                "https://leetcode.com/graphql",
                data={"query": query},
                headers={"Content-Type": "application/json"}
            )
            
            if not response.ok:
                raise Exception(f"GraphQL request failed: {response.status}")
                
            data = await response.json()
            daily_url_path = data["data"]["activeDailyCodingChallengeQuestion"]["link"]
            
            full_url = f"https://leetcode.com{daily_url_path}"
            logger.info(f"Found daily challenge: {full_url}")
            await self.navigate_to(full_url)
            return full_url
        except Exception as e:
            logger.error(f"Failed to find or click daily challenge: {e}")
            raise
