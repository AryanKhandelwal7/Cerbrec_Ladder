__Rivals Football Player Scraper__

This repository contains a Python-based web scraper that uses Selenium and BeautifulSoup to automatically search for American football players on [Rivals.com](https://n.rivals.com), extract key information such as the player’s name, school, and profile URL, and save the data into a CSV file.

__🚀 Features__

- Automates the search process on Rivals.com using Selenium WebDriver
- Extracts player name, school, and profile URL from the results or profile page
- Supports two fallback search methods for robust results
- Saves and appends results into a `player_info.csv` file
- Captures HTML pages and screenshots for debugging
- Works in both local environments and Google Colab

__Installation__

- Install the required dependencies using pip:
```bash
pip install selenium pandas webdriver-manager requests beautifulsoup4
```

__Usage__

- Run the script using the following command
```
python rivals_scraper.py
```

__Functioning of the scraper__

This code is meant to scrape the players information present on the rivals website. Following is a step by step procedure of it's execution:
- STEP 1: INPUT PLAYER NAME -- Given the name of the player, the scraper starts its execution process by navigating to the website and searching for the name
- STEP 2: SEARCHING PROCESS -- Over a database of more than 10,000 players, the scraper finds the player and navigates to the player information page
- STEP 3: LOADING PLAYER INFORMATION -- The scraper initially extracts the player name, school, and the URL from the webpage
- STEP 4: STORED IN A CSV FILE -- The data is then stored into a CSV file
