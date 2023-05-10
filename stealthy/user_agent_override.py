import re

from pyppeteer.page import Page


async def user_agent_override(
    page: Page,
    user_agent: str = None,
    locale: str = "en-US,en",
    mask_linux: str = True,
    **kwargs
) -> None:


    ua = user_agent or (await page.browser.userAgent()).replace('HeadlessChrome', 'Chrome')

    if mask_linux and 'Linux' in ua and 'Android' not in ua: # Skip Android user agents since they also contain Linux
        ua = re.sub(r'\(([^)]+)\)', '(Windows NT 10.0; Win64; x64)', ua, 1) # Replace the first part in parentheses with Windows data

    ua_version = re.search(r'Chrome\/([\d|.]+)', ua)[1] if 'Chrome/' in ua else re.search(r'\/([\d|.]+)', (await page.browser.version()))[1]

    # Get platform identifier (short or long version)
    def _get_platform(extended=False):
      if 'Mac OS X' in ua:
        return 'Mac OS X' if extended else 'MacIntel'
      elif 'Android' in ua:
        return 'Android'
      elif 'Linux' in ua:
        return 'Linux'
      else:
        return 'Windows' if extended else 'Win32'
    
    # Source in C++: https://source.chromium.org/chromium/chromium/src/+/master:components/embedder_support/user_agent_utils.cc;l=55-100
    def _get_brands():
        seed = ua_version.split('.')[0] # the major version number of Chrome

        order = [
            [0, 1, 2],
            [0, 2, 1],
            [1, 0, 2],
            [1, 2, 0],
            [2, 0, 1],
            [2, 1, 0]
        ][int(seed) % 6]
        escaped_chars = [' ', ' ', ';']

        greasey_brand = '{}Not{}A{}Brand'.format(escaped_chars[order[0]], escaped_chars[order[1]], escaped_chars[order[2]])

        greased_brand_version_list = [None]*3
        greased_brand_version_list [order[0]] = {
            'brand': greasey_brand,
            'version': '99'
        }
        greased_brand_version_list [order[1]] = {
            'brand': 'Chromium',
            'version': seed
        }
        greased_brand_version_list [order[2]] = {
            'brand': 'Google Chrome',
            'version': seed
        }

        return greased_brand_version_list 
    
    # Return OS version
    def _get_platform_version():
      if 'Mac OS X ' in ua:
        return re.search(r'Mac OS X ([^)]+)', ua)[1]
      elif 'Android ' in ua:
        return re.search(r'Android ([^;]+)', ua)[1]
      elif 'Windows ' in ua:
        return re.search(r'Windows .*?([\d|.]+);', ua)[1]
      else:
        return ''
    
    # Get architecture, this seems to be empty on mobile and x86 on desktop
    def _get_platform_arch():
        return '' if _get_mobile() else 'x86'

    # Return the Android model, empty on desktop
    def _get_platform_model():
        return re.search(r'Android.*?;\s([^)]+)', ua)[1] if _get_mobile() else ''

    def _get_mobile():
        return 'Android' in ua
    
    override = {
      'userAgent': ua,
      'platform': _get_platform(),
      'userAgentMetadata': {
        'brands': _get_brands(),
        'fullVersion': ua_version,
        'platform': _get_platform(True),
        'platformVersion': _get_platform_version(),
        'architecture': _get_platform_arch(),
        'model': _get_platform_model(),
        'mobile': _get_mobile()
      }
    }

    # In case of headless, override the acceptLanguage in CDP.
    # This is not preferred, as it messed up the header order.
    # On headful, we set the user preference language setting instead.
    if page.browser.process is not None and '--headless' in page.browser.process.args:
        override['acceptLanguage'] = locale or 'en-US,en'

    await page._client.send('Network.setUserAgentOverride', override)
