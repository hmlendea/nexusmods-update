import os
import re

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class Action:
    account_email_address: str
    account_password: str
    nexus_game_id: str
    nexus_mod_id: str
    mod_file_name: str
    mod_version: str
    file_description: str
    file_path: str

    def __init__(self):
        """Initialise and validate the input parameters passed via the environment variables."""
        self.account_email_address = os.environ["ACCOUNT_EMAIL_ADDRESS"]
        self.account_password = os.environ["ACCOUNT_PASSWORD"]
        self.nexus_game_id = os.environ["NEXUS_GAME_ID"]
        self.nexus_mod_id = os.environ["NEXUS_MOD_ID"]
        self.mod_file_name = os.environ["MOD_FILE_NAME"]
        self.mod_version = os.environ["MOD_VERSION"]
        self.file_description = os.environ["FILE_DESCRIPTION"]
        self.file_path = os.environ["FILE_PATH"]

        assert self.account_email_address, "The account's email address cannot be empty"
        assert self.account_password, "The account's password cannot be empty"
        assert self.nexus_game_id, "The Nexus Game ID cannot be empty"
        assert self.nexus_mod_id, "The Nexus Mod ID cannot be empty"
        assert self.mod_file_name, "The mod's file name cannot be empty"
        assert self.mod_version, "The mod's version cannot be empty"
        assert self.file_description, "file_description must not be empty"
        assert self.file_path, "file_path must not be empty"

        if not self.file_description or self.file_description.isspace():
            self.file_description = self.mod_file_name + ' version ' + self.mod_version

        assert len(self.file_description) <= 255
        assert os.path.isfile(self.file_path)

        _, extension = os.path.splitext(self.file_path)
        assert extension.lower() in (".rar", ".zip", ".7z", ".exe", ".omod")

    def login(self, driver):
        driver.get("https://users.nexusmods.com/auth/sign_in")

        driver.find_element(By.ID, "user_login").send_keys(self.username)
        driver.find_element(By.ID, "password").send_keys(self.password)
        driver.find_element(By.NAME, "commit").click()

        try:
            driver.find_element(By.XPATH, "//*[contains(text(), 'Invalid Login')]")
        except:
            print("Login successful!")
        else:
            raise ValueError("Invalid Login")

    def update(self, driver):
        driver.get(f"https://nexusmods.com/{self.nexus_game_id}/mods/edit/?id={self.nexus_mod_id}&step=files")

        driver.find_element(By.NAME, "name").send_keys(self.mod_file_name)
        driver.find_element(By.NAME, "file-version").send_keys(self.mod_version)
        driver.find_element(By.NAME, "update-version").click()
        driver.find_element(By.NAME, "new-existing").click()
        driver.find_element(By.ID, "select2-select-original-file-container").click()

        for option in driver.find_elements(By.CLASS_NAME, "select2-results__option"):
            if re.search(self.mod_file_name + '.*', option.text):
                option.click()
                break
        else:
            raise ValueError("Original file not found!")

        driver.find_element(By.NAME, "remove-old-version").click()
        driver.find_element(By.NAME, "brief-overview").send_keys(self.file_description)
        driver.find_element(By.NAME, "set_as_main_nmm").click()
        driver.find_element(By.NAME, "requirements_pop_up").click()
        driver.find_element(By.ID, "add_file_browse").find_elements(By.XPATH, ".//*")[0].send_keys(os.path.abspath(self.file_path))

        WebDriverWait(driver, 1500).until(lambda x: x.find_element(By.ID, "upload_success").is_displayed())

        driver.find_element(By.ID, "js-save-file").click()

        print("Finished!")

if __name__ == "__main__":
    print("Validating the input parameters...")
    action = Action()

    print("Configuring the WebDriver...")
    opt = webdriver.chrome.options.Options()
    opt.headless = False

    print("Starting the WebDriver...")
    driver = uc.Chrome(options=opt)
    driver.implicitly_wait(30)

    print("Logging in to Nexus...")
    action.login(driver)

    print("Updating the mod...")
    action.update(driver)
