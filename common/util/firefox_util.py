from selenium import webdriver


def get_firefox_options() -> webdriver.FirefoxOptions:
    firefox_options: webdriver.FirefoxOptions = webdriver.FirefoxOptions()
    firefox_options.add_argument(argument="-headless")
    firefox_options.add_argument(argument="-kiosk")
    return firefox_options


def get_firefox_profile() -> webdriver.FirefoxProfile:
    firefox_profile: webdriver.FirefoxProfile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    return firefox_profile
