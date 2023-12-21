import requests
import re
from bs4 import BeautifulSoup
from seleniumbase import SB

def get_discount(source : str) -> list:
    print("Getting dicount...")
    #the website comments the code, so we have to use regex to find the links from the source
    pattern = r'" ?(/offer[^"]*)"'
    matches = re.findall(pattern, source)
    matches.pop() #Last element is always a unwanted link
    return [match for match in matches]
        
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
    
def get_source() -> str:
    with SB(uc=True) as sb:
        print("Getting source...")
        sb.driver.get("https://www.real.discount/")
        sb.driver.click("label.tgl-btn") #free button
        try:
            sb.driver.click('input[value="Load More"]') #gets more link
            sb.driver.click('input[value="Load More"]')
        except Exception as e:
            print(e)
        finally:
            return sb.driver.page_source

def get_links(url):
    for link in url:
        response = requests.get('https://real.discount'+link)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('https://click.linksynergy.com/'): #udemy link
                links.append(href)
    return links

def main():
    pass

if __name__ == "__main__":
    main()
