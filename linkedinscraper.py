import time, random, traceback, pyautogui
from selenium.common.exceptions import TimeoutException


class LinkedinScraper:
    def __init__(self, parameters, driver):
        self.browser = driver
        self.disable_lock = parameters['disableAntiLock']
        self.email = parameters['email']
        self.password = parameters['password']
        self.job_id = parameters['jobId']

    def login(self):
        try:
            self.browser.get("https://www.linkedin.com/login")
            time.sleep(random.uniform(5, 10))
            self.browser.find_element_by_id("username").send_keys(self.email)
            self.browser.find_element_by_id("password").send_keys(self.password)
            self.browser.find_element_by_css_selector(".btn__primary--large").click()
            time.sleep(random.uniform(5, 10))
        except TimeoutException:
            raise Exception("Could not login!")

    def security_check(self):
        current_url = self.browser.current_url
        page_source = self.browser.page_source

        if '/checkpoint/challenge/' in current_url or 'security check' in page_source:
            input("Please complete the security check and press enter in this console when it is done.")
            time.sleep(random.uniform(5.5, 10.5))

    def start_scrape(self):
        page_sleep = 0
        minimum_page_time = time.time() + 240

        applicants_page_number = -1

        try:
            while True:
                page_sleep += 1
                applicants_page_number += 1
                print("Going to applicant page " + str(applicants_page_number))
                self.next_applicant_page(applicants_page_number)
                time.sleep(random.uniform(1.5, 3.5))
                print("Starting the scraping for this page...")
                self.scrape_applicants()
                print("Scraping for this page has been completed.")

                time_left = minimum_page_time - time.time()
                if time_left > 0:
                    print("Sleeping for " + str(time_left) + " seconds.")
                    time.sleep(time_left)
                    minimum_page_time = time.time() + 240
                if page_sleep % 5 == 0:
                    sleep_time = random.randint(500, 900)
                    print("Sleeping for " + str(sleep_time / 60) + " minutes.")
                    time.sleep(sleep_time)
                    page_sleep += 1
        except:
            traceback.print_exc()
            pass


    def scrape_applicants(self):
        try:
            applicant_results = self.browser.find_element_by_class_name("hiring-applicants__list-container")
            self.scroll_slow(page=True)
            self.scroll_slow(step=300, reverse=True, page=True)

            applicants_list = applicant_results.find_elements_by_class_name('hiring-applicants__list-item')
        except:
            raise Exception("No more applicants")

        if len(applicants_list) == 0:
            raise Exception("No more applicants")

        for applicant_tile in applicants_list:
            try:
                applicant_tile.click()

                application_description_area = self.browser.find_element_by_class_name("hiring-applicants__right-column")
                self.scroll_slow(application_description_area, end=1600)
                self.scroll_slow(application_description_area, end=1600, step=400, reverse=True)

                time.sleep(random.uniform(3, 5))

                try:
                    print("Downloading resume...")
                    link = ""
                    try:
                        link = application_description_area.find_element_by_class_name('hiring-resume-viewer__word-download-link').get_attribute('href')
                    except:
                        try:
                            link = application_description_area.find_element_by_class_name('link-without-visited-state').get_attribute('href')
                        except:
                            print("Could not get resume link!")
                            pass

                    self.browser.execute_script('''window.open("{}","_blank");'''.format(link))
                    time.sleep(random.uniform(3, 5))
                except:
                    print("Failed to download resume!")
                    pass
            except:
                pass

    def scroll_slow(self, scrollable_element=None, start=0, end=3600, step=100, reverse=False, page=False):
        if reverse:
            start, end = end, start
            step = -step

        for i in range(start, end, step):
            if page:
                self.browser.execute_script("window.scrollTo(0, {})".format(i))
            else:
                self.browser.execute_script("arguments[0].scrollTo(0, {})".format(i), scrollable_element)
            time.sleep(random.uniform(0.4, 1.6))

    def avoid_lock(self):
        if self.disable_lock:
            return

        pyautogui.keyDown('ctrl')
        pyautogui.press('esc')
        pyautogui.keyUp('ctrl')
        time.sleep(1.0)
        pyautogui.press('esc')

    def next_applicant_page(self, page_number):
        self.browser.get("https://www.linkedin.com/hiring/jobs/" + str(self.job_id) + "/applicants/?start=" + str(page_number*25))

        self.avoid_lock()

