import logging
from playwright.async_api import Page
from typing import Dict, Any, List
import re

logger = logging.getLogger(__name__)

class LeetCodeParser:
    def __init__(self, page: Page):
        self.page = page

    async def extract_problem_data(self) -> Dict[str, Any]:
        """Extract all metadata from a loaded LeetCode problem page."""
        logger.info("Extracting problem metadata")
        
        # Wait for the problem title to be visible. Leetcode usually has a format like "1. Two Sum"
        try:
            await self.page.wait_for_selector('[data-cy="question-title"]', timeout=10000)
        except:
            # Fallback for new UI
            try:
                await self.page.wait_for_selector('a[href^="/problems/"]', state='attached', timeout=10000)
            except Exception as e:
                logger.error(f"Could not find problem title element: {e}")

        # Evaluate extraction script in browser context
        data = await self.page.evaluate('''() => {
            const result = {
                title: "",
                difficulty: "",
                tags: [],
                description: "",
                constraints: "",
                examples: ""
            };

            // Title
            const titleEl = document.querySelector('[data-cy="question-title"]') || 
                            document.querySelector('.text-title-large a') ||
                            document.querySelector('div.flex.items-start > div > a');
            if (titleEl) result.title = titleEl.innerText;

            // Difficulty
            const diffEl = document.querySelector('[diff="easy"]') || 
                           document.querySelector('[diff="medium"]') || 
                           document.querySelector('[diff="hard"]') ||
                           document.querySelector('.text-difficulty-easy, .text-difficulty-medium, .text-difficulty-hard');
            if (diffEl) result.difficulty = diffEl.innerText;

            // Tags (Need to click "Topics" usually, or read if expanded)
            const tagEls = document.querySelectorAll('a[href^="/tag/"]');
            tagEls.forEach(el => result.tags.push(el.innerText));

            // Content
            const contentEl = document.querySelector('[data-track-load="description_content"]');
            if (contentEl) {
                result.description = contentEl.innerHTML;
                result.examples = contentEl.innerText.substring(0, 500); // Placeholder extraction
            }

            return result;
        }''')

        # Clean title (remove leading '1. ' or '1234. ')
        raw_title = data.get("title", "Unknown")
        clean_title = re.sub(r'^\d+\.\s*', '', raw_title)

        # Clean tags to string
        tags_str = ",".join(data.get("tags", [])) if data.get("tags") else None
        
        return {
            "title": clean_title,
            "difficulty": data.get("difficulty", "Unknown"),
            "tags": tags_str,
            "statement": data.get("description", ""),
            "constraints": data.get("constraints", ""),
            "examples": data.get("examples", "")
        }
