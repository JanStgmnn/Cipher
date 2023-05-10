from pyppeteer.page import Page

from .chrome_app import chrome_app
from .chrome_runtime import chrome_runtime
from .iframe_content_window import iframe_content_window
from .media_codecs import media_codecs
from .sourceurl import sourceurl
from .navigator_hardware_concurrency import navigator_hardware_concurrency
from .navigator_languages import navigator_languages
from .navigator_permissions import navigator_permissions
from .navigator_plugins import navigator_plugins
from .navigator_vendor import navigator_vendor
from .navigator_webdriver import navigator_webdriver
from .user_agent_override import user_agent_override
from .webgl_vendor import webgl_vendor
from .window_outerdimensions import window_outerdimensions
from .utils import with_utils


async def stealth(page: Page, disabled_evasions: list = [], **kwargs) -> None:
    if not isinstance(page, Page):
        raise ValueError("page must be pyppeteer.page.Page")
    if not isinstance(disabled_evasions, list):
        raise ValueError("disabled_evasions must be a list")

    evasion_dict = {
        "chrome_app": chrome_app,
        "chrome_runtime": chrome_runtime,
        "iframe_content_window": iframe_content_window,
        "media_codecs": media_codecs,
        "sourceurl": sourceurl,
        "navigator_hardware_concurrency": navigator_hardware_concurrency,
        "navigator_languages": navigator_languages,
        "navigator_permissions": navigator_permissions,
        "navigator_plugins": navigator_plugins,
        "navigator_vendor": navigator_vendor,
        "navigator_webdriver": navigator_webdriver,
        "user_agent_override": user_agent_override,
        "webgl_vendor": webgl_vendor,
        "window_outerdimensions": window_outerdimensions,
    }

    for evasion in disabled_evasions:
        if evasion not in evasion_dict:
            raise ValueError("{} is not a valid evasion name".format(evasion))
        del evasion_dict[evasion]

    await with_utils(page, **kwargs)

    for evasion in evasion_dict.values():
        await evasion(page, **kwargs)
