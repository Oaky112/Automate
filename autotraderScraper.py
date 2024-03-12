# Joshua Oakman
# Data Scraping

import os
import re
import time
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_user_criteria():
    criteria = {}
    criteria["postcode"] = input("Enter your postcode: ")
    age_input = input("Enter the age of the car you're looking for (e.g., 6 Years): ")
    age = re.findall(r"\d+", age_input)
    criteria["age"] = (
        age[0] if age else "0"
    )  # Extract only the numeric part or default to "0"
    return criteria


def scrape_autotrader(cars, criteria):
    data = []

    chrome_options = Options()
    chrome_options.add_argument("_tt_enable_cookie=1")
    driver = webdriver.Chrome(options=chrome_options)

    for car in cars:
        url = (
            "https://www.autotrader.co.uk/car-search?"
            + "advertising-location=at_cars&"
            + "include-delivery-option=on&"
            + f"make={car['make']}&"
            + f"model={car['model']}&"
            + f"postcode={criteria['postcode']}&"
            + f"radius={criteria['radius']}&"
            + "sort=relevance&"
            + f"year-from={datetime.datetime.now().year - int(criteria['age'])}&"
            + f"year-to={criteria['year_to']}&"
            + f"price-from={criteria['price_from']}&"
            + f"price-to={criteria['price_to']}"
        )

        driver.get(url)
        print(f"Searching for {car['make']} {car['model']}...")
        time.sleep(5)
        source = driver.page_source
        content = BeautifulSoup(source, "html.parser")

        try:
            number_of_pages = content.find(
                "p", text=re.compile(r"Page \d{1,2} of \d{1,2}")
            ).text[-1]
        except:
            print("No results found.")
            continue

        print(f"There are {number_of_pages} pages in total.")

        for i in range(int(number_of_pages)):
            driver.get(url + f"&page={str(i + 1)}")
            time.sleep(5)
            page_source = driver.page_source
            content = BeautifulSoup(page_source, "html.parser")
            articles = content.findAll(
                "section", attrs={"data-testid": "trader-seller-listing"}
            )

            print(f"Scraping page {str(i + 1)}...")

            for article in articles:
                # Check if the listing is an ad or belongs to an unknown make/model
                if article.find(
                    "span", class_="dealer-name--non-primary"
                ) or article.find("h2", class_="advertised-title"):
                    print("Skipping ad or unknown make/model.")
                    continue

                details = {
                    "name": car["make"] + " " + car["model"],
                    "price": re.search("[£]\d+(\,\d{3})?", article.text).group(0),
                    "year": None,
                    "mileage": None,
                    "transmission": None,
                    "fuel": None,
                    "engine": None,
                    "owners": None,
                    "location": None,
                    "distance": None,
                    "colour": None,  # New field for colour
                    "link": article.find(
                        "a", {"href": re.compile(r"/car-details/")}
                    ).get("href"),
                    "image_html_link": str(
                        article.find("img")
                    ),  # Extract HTML image link
                }

                try:
                    seller_info = article.find(
                        "p", attrs={"data-testid": "search-listing-seller"}
                    ).text
                    location = seller_info.split("Dealer location")[1]
                    details["location"] = location.split("(")[0]
                    details["distance"] = (
                        location.split("(")[1]
                        .replace(" mile)", "")
                        .replace(" miles)", "")
                    )
                except:
                    print("Seller information not found.")

                # New: Extract colour information
                try:
                    colour_text = article.find(
                        "ul", attrs={"data-testid": "listing-key-specs"}
                    ).text
                    if criteria["colour"].lower() in colour_text.lower():
                        details["colour"] = criteria["colour"]
                except:
                    print("Colour information not found.")

                specs_list = article.find(
                    "ul", attrs={"data-testid": "search-listing-specs"}
                )
                for spec in specs_list:
                    if "reg" in spec.text:
                        details["year"] = spec.text

                    if "miles" in spec.text:
                        details["mileage"] = spec.text

                    if spec.text in ["Manual", "Automatic"]:
                        details["transmission"] = spec.text

                    if "." in spec.text and "L" in spec.text:
                        details["engine"] = spec.text

                    if spec.text in ["Petrol", "Diesel"]:
                        details["fuel"] = spec.text

                    if "owner" in spec.text:
                        details["owners"] = spec.text[0]

                data.append(details)

            print(f"Page {str(i + 1)} scraped. ({len(articles)} articles)")
            time.sleep(5)

    driver.quit()  # Close the driver after scraping all pages for all makes/models

    print("\n\n")
    print(f"{len(data)} cars total found.")

    return data


def output_data_to_csv(data, criteria):
    df = pd.DataFrame(data)

    df["price"] = df["price"].str.replace("£", "").str.replace(",", "")
    df["price"] = pd.to_numeric(df["price"], errors="coerce").astype("Int64")

    df["year"] = df["year"].str.replace(r"\s(\(\d\d reg\))", "", regex=True)
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    df["mileage"] = df["mileage"].str.replace(",", "").str.replace(" miles", "")
    df["mileage"] = pd.to_numeric(df["mileage"], errors="coerce").astype("Int64")

    now = datetime.datetime.now()
    df["miles_pa"] = df["mileage"] / (now.year - df["year"])
    df["miles_pa"].fillna(0, inplace=True)
    df["miles_pa"] = df["miles_pa"].astype(int)

    df["owners"] = df["owners"].fillna("-1")
    df["owners"] = df["owners"].astype(int)

    df["distance"] = df["distance"].fillna("-1")
    df["distance"] = df["distance"].astype(int)

    df["link"] = "https://www.autotrader.co.uk" + df["link"]

    df = df[
        [
            "name",
            "link",
            "price",
            "year",
            "mileage",
            "miles_pa",
            "owners",
            "distance",
            "location",
            "engine",
            "transmission",
            "fuel",
            "colour",  # Include colour in the dataframe
            "image_html_link",  # Include HTML image link in the dataframe
        ]
    ]

    df = df[df["price"] < int(criteria["price_to"])]

    df = df.sort_values(by="distance", ascending=True)

    output_dir = "car_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Check for existing files and increment the count
    file_count = 1
    while True:
        output_file = os.path.join(output_dir, f"cars{file_count}.csv")
        if not os.path.exists(output_file):
            break
        file_count += 1

    df.to_csv(output_file, index=False)
    print(f"Output saved to '{output_file}'.")


if __name__ == "__main__":
    cars = [
        {"make": "Ford", "model": "Fiesta"},
        {"make": "Volkswagen", "model": "Golf"},
        {"make": "Skoda", "model": "Octavia"},
        {"make": "BMW", "model": "1 Series"},
    ]

    user_criteria = get_user_criteria()
    criteria = {
        "radius": "80",
        "year_to": "2024",
        "price_from": "6000",
        "price_to": "9000",
    }
    criteria.update(user_criteria)

    data = scrape_autotrader(cars, criteria)
    output_data_to_csv(data, criteria)
