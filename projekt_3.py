"""
projekt_3.py: Third project for Engeto Online Python Academy
author: Dmytro Zhura
email: zhura.dm@seznam.cz
discord: twitch_dariys68
"""

import requests
from bs4 import BeautifulSoup
import argparse
import csv

def validate_url(url: str) -> bool:
    """Function to validate the URL using the requests library."""
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def validate_command_line_arguments() -> tuple:
    """Function to validate command line arguments and return URL and file name as a tuple."""
    parser = argparse.ArgumentParser(description="Election results scraper.")
    parser.add_argument("url", type=str, help="URL for scraping election results.")
    parser.add_argument("file_name", type=str, help="Output CSV file name.")
    args = parser.parse_args()
    url, file_name = args.url, args.file_name

    if not url.startswith("https://volby.cz/pls/ps2017nss/"):
        raise ValueError("URL must start with 'https://volby.cz/pls/ps2017nss/'.")

    if not file_name.endswith(".csv"):
        raise ValueError("File name must end with '.csv'.")

    if not validate_url(url):
        raise ValueError("Invalid URL: " + url)

    return url, file_name

def get_city_urls(url: str) -> list[str]:
    """Function to get URLs of individual cities from the main URL."""
    response = requests.get(url)
    doc = BeautifulSoup(response.text, "html.parser")
    city_urls = []
    
    # Get all links on the page that contain 'xobec='
    for a in doc.find_all("a", href=True):
        if "xobec=" in a["href"]:
            full_url = "https://volby.cz/pls/ps2017nss/" + a["href"]
            if full_url not in city_urls:
                city_urls.append(full_url)
    
    return city_urls

def city_names_scraper(url) -> list:
    """Function to get city codes and names from the URL."""
    response = requests.get(url)
    doc = BeautifulSoup(response.text, "html.parser")
    city_codes = [city.text.strip() for city in doc.find_all("td", class_="cislo")]
    city_names = [city.text.strip() for city in doc.find_all("td", class_="overflow_name")]
    return city_codes, city_names

def voter_turnout_data(city_urls) -> list:
    """Function to get voter turnout data from city URLs."""
    registered_voters = []
    ballot_papers = []
    valid_votes = []

    for url in city_urls:
        response = requests.get(url)
        doc = BeautifulSoup(response.text, "html.parser")
        registered_voters.extend(
            j.text.replace("\xa0", "").strip() for j in doc.find_all("td", class_="cislo", headers="sa2")
        )
        ballot_papers.extend(
            j.text.replace("\xa0", "").strip() for j in doc.find_all("td", class_="cislo", headers="sa3")
        )
        valid_votes.extend(
            j.text.replace("\xa0", "").strip() for j in doc.find_all("td", class_="cislo", headers="sa6")
        )

    return [registered_voters, ballot_papers, valid_votes]

def get_political_parties(city_urls: list) -> list[str]:
    """Function to get names of political parties from city URL."""
    if not city_urls:
        raise ValueError("City URL list is empty.")
    
    political_parties = []
    response = requests.get(city_urls[0])
    doc = BeautifulSoup(response.text, "html.parser")
    table1 = [
        j.text.replace("\xa0", "").strip() for j in doc.find_all("td", class_="overflow_name", headers="t1sa1 t1sb2")
    ]
    table2 = [
        j.text.replace("\xa0", "").strip() for j in doc.find_all("td", class_="overflow_name", headers="t2sa1 t2sb2")
    ]
    political_parties.extend(table1 + table2)
    return political_parties

def get_votes(city_urls: list) -> list:
    """Function to get votes for individual political parties from city URLs."""
    total_votes = []
    for url in city_urls:
        response = requests.get(url)
        doc = BeautifulSoup(response.text, "html.parser")
        table1 = [
            j.text.replace("\xa0", "").strip() for j in doc.find_all("td", class_="cislo", headers="t1sa2 t1sb3")
        ]
        table2 = [
            j.text.replace("\xa0", "").strip() for j in doc.find_all("td", class_="cislo", headers="t2sa2 t2sb3")
        ]
        total_votes.append(table1 + table2)
    return total_votes

def write_csv(file_name, city_codes, city_names, data_collection, political_parties, total_votes) -> None:
    """Function to write data to a CSV file."""
    head = [
        "City Code",
        "City Name",
        "Registered Voters",
        "Issued Ballots",
        "Valid Votes",
    ]
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(head + political_parties)
        for i in range(len(city_codes)):
            writer.writerow(
                [city_codes[i], city_names[i]]
                + [data_collection[0][i]]
                + [data_collection[1][i]]
                + [data_collection[2][i]]
                + total_votes[i]
            )

def main() -> None:
    """Main function of the program."""
    try:
        url, file_name = validate_command_line_arguments()
        print(f'Initializing program with URL "{url}" and file name "{file_name}"\nExtracting data...')
        city_codes, city_names = city_names_scraper(url)
        city_urls = get_city_urls(url)
        if not city_urls:
            raise ValueError("City URL list is empty.")
        data_collection = voter_turnout_data(city_urls)
        political_parties = get_political_parties(city_urls)
        total_votes = get_votes(city_urls)
        write_csv(
            file_name, city_codes, city_names, data_collection, political_parties, total_votes
        )
        print(f"File {file_name} has been successfully generated.")
    except ValueError as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    main()