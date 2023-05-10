from pathlib import Path

from pyppeteer.page import Page


async def navigator_hardware_concurrency(page: Page, hardwareConcurrency: int = 4, **kwargs) -> None:
    await page.evaluateOnNewDocument(
        """
        (hardwareConcurrency) => {
    utils.replaceGetterWithProxy(
        Object.getPrototypeOf(navigator),
        'hardwareConcurrency',
        utils.makeHandler().getterValue(hardwareConcurrency)
      )
}
        """,
        hardwareConcurrency,
    )
