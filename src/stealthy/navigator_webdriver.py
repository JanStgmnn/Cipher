from pathlib import Path

from pyppeteer.page import Page


async def navigator_webdriver(page: Page, **kwargs) -> None:
    await page.evaluateOnNewDocument(
        """
        () => {
  delete Object.getPrototypeOf(navigator).webdriver
}
        """
    )
