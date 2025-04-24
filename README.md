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

- Run the script using : python rivals_scraper.py
