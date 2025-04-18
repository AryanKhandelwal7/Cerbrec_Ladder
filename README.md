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

**🔧 How It Works**

1. Chrome Setup (Colab Friendly)
  - Automatically installs Chromium and moves chromedriver to /usr/bin/.

  - Uses headless mode and predefined Chrome user-agent for compatibility.

2. Scraping Process
  - Loads Rivals search URL for football prospects.

  - Waits for the table or rows to appear using Selenium's WebDriverWait.

  - Extracts player name and profile link using:

  - HTML parsing (BeautifulSoup)

  - JavaScript DOM evaluation (execute_script)

  - Backup scraping from saved HTML (debug_pages/rivals_search_page.html)

  - Optional direct HTTP request
