from pathlib import Path
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep


class MyDesk:
    def __init__(self):
        self.username = ''
        self.password = ''
        self.pin = ''
        self.downloadsFolder = ''
        self.fetchDetails()

    def login(self):
        self.deleteExistingLauncher()
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(
            executable_path=r"chromedriver", options=options)

        print("Opening Mydesk")
        self.driver.get(
            "https://tier2.mydesk.morganstanley.com/vpn/mydesk.html#/login")

        while 1:
            try:
                self.driver.find_element_by_id("userName")
                break
            except:
                continue
        isValidUser = False
        while not isValidUser:
            self.enterCredentials()
            sleep(3)
            while 1:
                try:
                    if(self.driver.find_element_by_xpath("//span[contains(.,'Login failed;')]")):
                        print("Login Failed")
                        break
                    if(self.driver.find_element_by_xpath("//a[contains(.,'Hosted Workstation')]")):
                        print('Logged In Successfully')
                        self.driver.find_element_by_xpath(
                            "//a[contains(.,'Hosted Workstation')]").click()
                        isValidUser = True
                        print("Downloaading Launcher please wait...")
                        break
                except:
                    continue
        self.openLauncher()

    def enterCredentials(self):
        securid = input("\nEnter securid : ")

        self.driver.find_element_by_id("userName").send_keys(self.username)

        self.driver.find_element_by_id("pw_elem").send_keys(self.password)

        self.driver.find_element_by_id(
            "securid_elem").send_keys(self.pin+securid)

        print("Logging in please wait...")
        while 1:
            try:
                self.driver.find_element_by_xpath(
                    "//button[text()='Go']").click()
                break
            except:
                continue

    def fetchDetails(self):
        file = open('constants.txt', 'r')
        lines = file.readlines()
        for line in lines:
            try:
                key, val = line.split("=")
                key, val = key.strip().strip("\""), val.strip().strip("\"")
                # print(key, val)
                if key == "username":
                    self.username = val
                elif key == "password":
                    self.password = val
                elif key == "pin":
                    self.pin = val
                elif key == "downloadsFolder":
                    self.downloadsFolder = val
            except:
                pass
        # print(self.username, self.password, self.pin, self.downloadsFolder)

    def deleteExistingLauncher(self):
        print("Checking if previous Launcher exists")
        file = self.downloadsFolder + "/launchExtMSAD.ica"
        if Path(file).exists():
            print("Found")
            os.remove(file)
            print("Deleted")
        else:
            print("Not found")

    def openLauncher(self):
        file = self.downloadsFolder + "/launchExtMSAD.ica"
        while 1:
            if Path(file).exists():
                print("Opening Launcher")
                os.system(file)
                break
            else:
                continue
        os._exit(0)


mydesk = MyDesk()
mydesk.login()
