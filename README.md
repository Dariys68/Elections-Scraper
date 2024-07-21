# Author

Name: Dmytro Zhura
Email: zhura.dm@seznam.cz
Discord: twitch_dariys68

# Election Scraper

Engeto Project #3: This script scrapes election data from the 2017 Chamber of Deputies elections in the Czech Republic via the official election results website: https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ. The data is stored in a CSV file. To run this program, you need to select an election district from the website (e.g., for the Karlovy Vary district, use the URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4102) and pass a name for the CSV file with a .csv extension (see Deployment section).

## Libraries

The script is written in Python and uses the following libraries:

- Requests
- BeautifulSoup
- Argparse
- CSV

## Features

- **URL Validation**: Ensures the URL is valid using the requests library.
- **Command Line Argument Validation**: Validates the command line arguments, ensuring the URL starts with `https://www.volby.cz/pls/ps2017nss/`  and the file name ends with `.csv`.
- **City Names Scraper**: Extracts a list of city codes and names from the main URL using BeautifulSoup.
- **City URL Scraper**: Extracts all city URLs from the main page.
- **Voter Turnout Data**: Extracts voter turnout data (registered voters, issued ballots, and valid votes) from the city URLs.
- **Political Parties and Votes Scraper**: Extracts names of political parties and their respective votes from each city.
- **Data Storage**: Saves the extracted data into a CSV file.

## Deployment

To run the script, pass two command-line arguments: the URL and the file name. For example:

```bash
python projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4102" "results_KV.csv"