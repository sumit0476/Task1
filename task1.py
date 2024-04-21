from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import pymongo
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["financial_data"]
collection = db["bse_updates"]

# Selenium setup
driver = webdriver.Chrome(
    "path_to_chromedriver"
)  # Update the path to your ChromeDriver


# Function to scrape data
def scrape_data(url, start_date, end_date, category):
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    # Filtering data based on input parameters
    filtered_data = []
    for item in soup.find_all("a", href=True):  # assuming data is in 'a' tags
        date_str = (
            item.text.strip()
        )  # Example: extract date from the text or a sibling/child tag
        try:
            current_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            if start_date <= current_date <= end_date:
                if category in item["href"]:  # Example: category filter on href content
                    pdf_link = item["href"]
                    heading = item.text
                    filtered_data.append(
                        {"date": current_date, "heading": heading, "link": pdf_link}
                    )
        except ValueError:
            continue

    return filtered_data


# Function to save data to MongoDB
def save_to_mongodb(data):
    if data:
        collection.insert_one({"run_date": datetime.datetime.now(), "data": data})


# Main execution function
def main():
    url = "http://www.bseindia.com"
    start_date = datetime.datetime(2023, 1, 1)
    end_date = datetime.datetime(2023, 12, 31)
    category = "finance"

    scraped_data = scrape_data(url, start_date, end_date, category)
    save_to_mongodb(scraped_data)


# Run the script
main()

# Close the Selenium browser
driver.quit()
