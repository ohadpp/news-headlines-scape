from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os
import sys
from datetime import datetime

application_path = os.path.dirname(sys.executable)
now = datetime.now()
month_day_year = now.strftime("%d%m%y")  # DDMMYYYY



website = "https://www.thesun.co.uk/"
path = '/usr/local/bin/chromedriver'

# Set up Chrome options
chrome_options = Options()
chrome_options._ignore_local_proxy = True



service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(website)

containers = driver.find_elements(by='xpath', value="//div[@class='teaser__copy-container']")

# List to store dictionaries for each container
container_data_list = []

for container in containers:
    try:
        # Find the title within the current container
        title_element = container.find_element(by="xpath", value=".//span[@class='teaser__headline t-p-color']")
        title = title_element.text

        # Find the subtitle within the current container
        subtitle_element = container.find_element(by="xpath", value="./a/p")
        subtitle = subtitle_element.text

        # Find the link within the current container
        link_element = container.find_element(by="xpath", value="./a")
        link = link_element.get_attribute("href")

        # Create a dictionary for the current container
        container_data = {
            "Title": title,
            "Subtitle": subtitle,
            "Link": link
        }

        # Append the dictionary to the list
        container_data_list.append(container_data)
    except NoSuchElementException as e:
        # Handle the case where an element is not found
        print(f"Skipping container due to NoSuchElementException: {e}")

# Print the list of dictionaries
for container_data in container_data_list:
    print(container_data)
    print("\n")

df = pd.DataFrame(container_data_list)

file_name = f'headline-{month_day_year}.csv'
final_path = os.path.join(application_path, file_name)
df.to_csv(final_path)
#df.to_excel("head_lines.xlsx")
#df.to_csv("head_lines.csv")



driver.quit()