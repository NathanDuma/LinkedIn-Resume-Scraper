import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from linkedinscraper import LinkedinScraper
from validate_email import validate_email


def init_browser():
    browser_options = Options()
    options = ['--disable-blink-features', '--no-sandbox', '--start-maximized', '--disable-extensions',
               '--ignore-certificate-errors', '--disable-blink-features=AutomationControlled']

    for option in options:
        browser_options.add_argument(option)

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=browser_options)

    driver.set_window_position(0, 0)
    driver.maximize_window()

    return driver


def validate_yaml():
    with open("config.yaml", 'r') as stream:
        try:
            parameters = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc

    mandatory_params = ['email', 'password', 'disableAntiLock', 'jobId']

    for mandatory_param in mandatory_params:
        if mandatory_param not in parameters:
            raise Exception(mandatory_param + ' is not inside the yml file!')

    assert validate_email(parameters['email'])
    assert len(parameters['password']) > 0

    assert isinstance(parameters['disableAntiLock'], bool)

    assert isinstance(parameters['jobId'], int)

    return parameters


if __name__ == '__main__':
    parameters = validate_yaml()
    browser = init_browser()

    scraper = LinkedinScraper(parameters, browser)
    scraper.login()
    scraper.security_check()
    scraper.start_scrape()

    browser.close()




