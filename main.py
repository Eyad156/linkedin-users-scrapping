import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Setup Selenium WebDriver with custom user agent
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)

# Open LinkedIn and login
driver.get("https://www.linkedin.com/login")
username = driver.find_element(By.ID, "username")   
password = driver.find_element(By.ID, "password")
username.send_keys("email")  # Replace with your LinkedIn login email
password.send_keys("password")  # Replace with your LinkedIn password
password.send_keys(Keys.RETURN)

# Wait for login to complete and redirect
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-global-typeahead__input")))

# List of LinkedIn profile URLs
profile_urls = [
    "https://www.linkedin.com/in/frank-joung-76-fjo/",
    "https://www.linkedin.com/in/sara-grzybek/",
    "https://www.linkedin.com/in/alexandermuehl/",
    "https://www.linkedin.com/in/mirrianne-mahn-72727614a/",
    "https://www.linkedin.com/in/andrewdeast/",
    "https://www.linkedin.com/in/tom-eggleston-73a50a12/",
    "https://www.linkedin.com/in/ryan-killian-1200b91/",
    "https://www.linkedin.com/in/adamhaleck/",
    "https://www.linkedin.com/in/david-morgan-b80a4732/",
    "https://www.linkedin.com/in/zeya-tun-2782b943/",
    "https://www.linkedin.com/in/paul-jansson-mba-62b49ba/",
    "https://www.linkedin.com/in/jae-lee-cpa/",
    "https://www.linkedin.com/in/angela-alvino-93947a1b2/",
    "https://www.linkedin.com/in/junia-abaidoo-92a17540/",
    "https://www.linkedin.com/in/evan-owens-5b58bb40/",
    "https://www.linkedin.com/in/oliviadorsey31/",
    "https://www.linkedin.com/in/rodneymjolicoeur/",
    "https://www.linkedin.com/in/alex-jones-776985123/",
    "https://www.linkedin.com/in/kpalwankar/",
    "https://www.linkedin.com/in/sridhar-ramaswamy/",
    "https://www.linkedin.com/in/benoit-dageville-3011845/",
    "https://www.linkedin.com/in/prasanna-krishnan-1944aa1/",
]

# Define the CSV file name
csv_file_name = "linkedin_profile_data.csv"

# Open the CSV file to write data
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Headline", "Location", "Followers", "About", "Experience", "Contact info"])

    # Loop through each profile URL
    for profile_url in profile_urls:
        driver.get(profile_url)
        time.sleep(5)  # Wait between 5 to 7 seconds
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extracting name, headline, location, followers, about, experience
        name = soup.find("h1", class_="text-heading-xlarge")
        name = name.get_text(strip=True) if name else "Name not found"

        headline = soup.find("div", class_="text-body-medium")
        headline = headline.get_text(strip=True) if headline else "Headline not found"

        location = soup.find("span", class_="text-body-small inline t-black--light break-words")
        location = location.get_text(strip=True) if location else "Location not found"

        followers = soup.find("span", "t-bold")
        followers = followers.get_text(strip=True) if followers else "Followers not found"

        about = soup.find("div", class_="display-flex ph5 pv3")
        about = about.get_text(strip=True) if about else "About not found"

        experience = soup.find("div", class_="display-flex flex-column full-width align-self-center")
        experience = experience.get_text(strip=True) if experience else "Experience not found"

        # Clicking on the contact info
        try:
            click_on_info = driver.find_element(By.ID, 'top-card-text-details-contact-info')
            click_on_info.click()

            # Wait for the modal to load and get the updated page source
            WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CLASS_NAME, "artdeco-modal__content")))
            time.sleep(2)  # Give some time for the modal content to load

            # Parse the updated page source
            soup = BeautifulSoup(driver.page_source, "html.parser")
            modal_content = soup.find("div", class_="artdeco-modal__content ember-view")
            contact_info = modal_content.get_text(strip=True) if modal_content else "Contact info not found"

        except Exception as e:
            contact_info = "Contact info not found"
        writer.writerow(["Name: ",name,"\nHeadline: ", headline,"\nLocation: ", location,"\nFollowers: ", followers, "\nAbout: ",about,"\nExperience: ", experience,"\nContactInfo: ", contact_info])
        print(f"Data successfully exported for {profile_url}")

# Close the driver
driver.quit()
