from pathlib import Path

from pyppeteer.page import Page


async def navigator_vendor(page: Page, vendor: str = "Google Inc.", **kwargs) -> None:
    await page.evaluateOnNewDocument(
        """
        vendor => {
  // Overwrite the `vendor` property to use a custom getter.
  utils.replaceGetterWithProxy(
    Object.getPrototypeOf(navigator),
    'vendor',
    utils.makeHandler().getterValue(vendor)
  )
}

        """, vendor
    )
