from pathlib import Path

from pyppeteer.page import Page


async def navigator_languages(page: Page, languages: [str] = ["en-US", "en"], **kwargs) -> None:
    await page.evaluateOnNewDocument(
        """
        (languages) => {
  // Overwrite the `languages` property to use a custom getter.
  const languages_to_pass = languages.length
    ? languages
    : ['en-US', 'en']
  utils.replaceGetterWithProxy(
    Object.getPrototypeOf(navigator),
    'languages',
    utils.makeHandler().getterValue(Object.freeze([...languages_to_pass]))
  )
}
        """,
        languages,
    )
