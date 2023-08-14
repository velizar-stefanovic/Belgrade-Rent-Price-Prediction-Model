from bs4 import BeautifulSoup
import requests
import re
import time
import datetime
from utils import translate_to_utf, get_properties
import pandas as pd

def fetch_property_data(list_of_properties, base_url="https://www.nekretnine.rs/"):
    """
    This functions scrapes the property data from the
    provided property IDs on website www.nekretnine.rs, and stores it in the CSV file.
    
    Args:
        list_of_properties: a list of property IDs
        base_url: a base URL of the website

    Returns:
        a data frame with scraped data
    """

    now = datetime.datetime.today()
    print(datetime.date(now.year, now.month, now.day))
    count = 0
    # create empty data frame
    columns = ["id_property", "date_scrape", "property_name", "date_post", "date_update", "area_m2", "price_eur", 'rooms', 'heating', 'parking', 'furniture', 'details', 'description', 'location']
    df = pd.DataFrame(columns=columns)

    # iterate through the list of properties
    for property_id in list_of_properties:
        page = requests.get(base_url + property_id)
        property = BeautifulSoup(page.content, "html.parser")
        id_property = property_id

        # sometimes the property is not available anymore
        try:
            property_name = property.find(
                "h1", class_="detail-title pt-3 pb-2"
            ).text.strip()

            dates = property.find("div", class_="updated").text.strip()

            date_post = re.findall("\S*Objavljen: (\S+)", dates)[0]

            date_update = re.findall("\S*Ažuriran: (\S+)\nObjavljen", dates)[0]

            area_m2 = property.find("h4", class_="stickyBox__size").text[:-3]

            # sometimes the price is not provided
            try:
                price_eur = re.findall(
                    "(.*) EUR", property.find("h4", class_="stickyBox__price").text
                )[0].replace(" ", "")
            except IndexError:
                price_eur = "N/A"
                
            # sometimes the number of rooms is not provided
            try:
                rooms = float(
                    re.findall(
                        ":(\S*)",
                        property.find("div", class_="property__main-details")
                        .find_all("span")[2]
                        .text,
                    )[0]
                )
            except:
                rooms = "N/A"

            heating = re.findall(
                ":(\S+)",
                property.find("div", class_="property__main-details")
                .find_all("span")[4]
                .text,
            )[0]

            parking = re.findall(
                ":(\S+)",
                property.find("div", class_="property__main-details")
                .find_all("span")[6]
                .text,
            )[0]

            furniture = re.findall(
                ":(.+)",
                property.find("div", class_="property__main-details")
                .find_all("span")[10]
                .text,
            )[0]

            details = " ".join(
                property.find("div", class_="property__amenities").text.split()
            )

            # sometimes, the description could be shown in different places, or is not provided at all
            try:
                description = (
                    (property.find("div", class_="cms-content-inner").find_all("p")[2].text)
                    .strip()
                    .replace("\n", " ")
                    .replace("\r", " ")
                )
            except:
                try:
                    description = (
                        property.find("div", class_="cms-content-inner")
                        .text.strip()
                        .replace("\n", " ")
                        .replace("\r", " ")
                    )
                except:
                    description = "could not find"
            location = ", ".join(
                property.find("div", class_="property__location").text.strip().split("\n")
            )

            property_dict = {
                "id_property": id_property,
                "date_scrape": datetime.date(now.year, now.month, now.day),
                "property_name": translate_to_utf(property_name),
                "date_post": date_post,
                "date_update": date_update,
                "area_m2": area_m2,
                "price_eur": price_eur,
                "rooms": rooms,
                "heating": translate_to_utf(heating),
                "parking": parking,
                "furniture": translate_to_utf(furniture),
                "details": translate_to_utf(details),
                "description": translate_to_utf(description),
                "location": translate_to_utf(location),
            }

            # add property_dict to the data frame
            new_row = pd.DataFrame(property_dict, index=[0])
            df = pd.concat([df, new_row], ignore_index=True)

            print(f"Property number {list_of_properties.index(property_id)+1} is scraped: {id_property}")
            count += 1

        except:
            print(f"Property number {list_of_properties.index(property_id)+1} is not scraped: {id_property}")
            count += 1

        # pause scraping every 10 pages
        if count % 10 == 0 and count != len(list_of_properties):
            print("Pausing for a bit...")
            time.sleep(2)

    # save the data frame to the CSV file
    file_name = f"property_data_{datetime.date(now.year, now.month, now.day)}.csv"
    df.to_csv(file_name, index=False)

    return df

properties = get_properties("nekretnine_2023-08-08.csv")

fetch_property_data(properties)
