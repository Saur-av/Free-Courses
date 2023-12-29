import requests
import re
from bs4 import BeautifulSoup
from seleniumbase import SB

def enroll_udemy(courseurls : list) -> list:
    with SB(uc=True) as sb:
        sb.driver.get("https://www.udemy.com/")
        sb.click('a[data-purpose="header-login"]')
        sb.get_element('[name="email"]').send_keys("username@gmail.com")
        sb.get_element('[name="password"]').send_keys("password")
        sb.click('button:contains("Log in")')
        enrolled = []
        for url in courseurls:
            sb.driver.open(url)
            button = sb.get_element('div.sidebar-container--purchase-section--2DONZ div div div:nth-of-type(5) button')
            if button.text == "Share":
                print("Already Enrolled!")
            elif button.text == "Enroll now":        
                sb.driver.click("div.sidebar-container--purchase-section--2DONZ div div div:nth-of-type(5) button")
                sb.driver.click("#udemy > div.ud-main-content-wrapper > div.ud-main-content > div > div > div > aside > div > div > div.marketplace-checkout--button-term-wrapper--2_M-- > div.checkout-button--checkout-button--container--RQKAM > button")
                enrolled.append(url)
            elif button.text == "Buy now":
                print("Course is not free!")
            sb.sleep(1)
        return enrolled

def main():
    pass

if __name__ == "__main__":
    main()
