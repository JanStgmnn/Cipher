from pathlib import Path

from pyppeteer.page import Page


async def window_outerdimensions(page: Page, **kwargs) -> None:
    await page.evaluateOnNewDocument(
        """
        () => {
  try {
    if (window.outerWidth && window.outerHeight) {
      return // nothing to do here
    }
    const windowFrame = 85 // probably OS and WM dependent
    window.outerWidth = window.innerWidth
    window.outerHeight = window.innerHeight + windowFrame
  } catch (err) { }
}
        """
    )
