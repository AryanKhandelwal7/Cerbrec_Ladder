__Rivals Football Player Scraper__

This Python project scrapes football player data (names and profile URLs) from Rivals.com using Selenium, BeautifulSoup, and direct requests as a backup. It is designed to work in environments like Google Colab, where installing Chrome and ChromeDriver may require custom setup.

__🚀 Features__

- Scrapes football players' names and profile URLs from Rivals search results.

- Supports execution in Google Colab with automatic Chrome setup.

- Saves a debug HTML snapshot for fallback scraping and troubleshooting.

- Implements three scraping strategies:

- Standard Selenium HTML parsing

- JavaScript DOM extraction

- Direct HTTP Request fallback (requests + BeautifulSoup)
