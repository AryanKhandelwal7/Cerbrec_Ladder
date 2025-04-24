!pip install selenium pandas webdriver-manager requests bs4

import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import re
import urllib.parse

# Function to set up and install Chrome for Colab
def setup_chrome_for_colab():
    try:
        # Install Chrome and ChromeDriver using system commands
        import subprocess
        print("Updating packages...")
        subprocess.run(["apt-get", "update"], check=True)
        print("Installing chromium-browser...")
        subprocess.run(["apt-get", "install", "-y", "chromium-browser"], check=True)

        # Try to find chromedriver location
        import glob
        chromedriver_paths = glob.glob("/usr/lib/chromium*/chromedriver")
        if chromedriver_paths:
            print(f"Found chromedriver at: {chromedriver_paths[0]}")
            subprocess.run(["cp", chromedriver_paths[0], "/usr/bin/"], check=True)
        else:
            print("ChromeDriver not found in expected locations, installing via chromedriver-py")
            !pip install chromedriver-py
            from chromedriver_py import binary_path
            print(f"Using chromedriver from chromedriver-py at: {binary_path}")
    except Exception as e:
        print(f"Error during Chrome setup: {e}")

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    return chrome_options

def search_player_and_extract_info(player_name):
    print(f"Setting up Chrome to search for player: {player_name}")
    chrome_options = setup_chrome_for_colab()

    # Initialize driver
    try:
        # Try standard approach first
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Standard Chrome initialization failed: {e}")
        try:
            # Try with chromedriver-py
            from selenium.webdriver.chrome.service import Service
            from chromedriver_py import binary_path
            service = Service(executable_path=binary_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e2:
            print(f"Alternative Chrome initialization failed: {e2}")
            try:
                # Last resort - webdriver_manager
                print("Attempting with webdriver_manager...")
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.chrome.service import Service
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
            except Exception as e3:
                print(f"All Chrome initialization methods failed: {e3}")
                raise Exception("Unable to initialize Chrome driver")

    player_info = None
    os.makedirs("debug_pages", exist_ok=True)

    try:
        # Mask WebDriver properties using JavaScript
        driver.execute_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        """)

        # Method 1: Try constructing a direct search URL
        encoded_name = urllib.parse.quote(player_name)
        direct_search_url = f"https://n.rivals.com/search?q={encoded_name}&sport=Football"
        print(f"Navigating to direct search URL: {direct_search_url}")

        driver.get(direct_search_url)
        print("Waiting for page to load...")
        time.sleep(10)

        # Save the page
        with open("debug_pages/direct_search_results.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Saved direct search results page")

        # Take a screenshot
        driver.save_screenshot("debug_pages/direct_search_results.png")

        # Analyze the page structure
        print("Analyzing page structure...")
        page_html = driver.page_source
        soup = BeautifulSoup(page_html, 'html.parser')

        # Print basic page info for debugging
        print(f"Page title: {driver.title}")
        print(f"Current URL: {driver.current_url}")

        # Look for any tables
        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables on the page")

        # Look for rows in any table
        rows = soup.find_all('tr')
        print(f"Found {len(rows)} table rows on the page")

        # Look for links that might be player profiles
        all_links = soup.find_all('a')
        print(f"Found {len(all_links)} links on the page")

        # Extract player links - look for any link that might contain the player name
        player_links = []
        player_name_parts = player_name.lower().split()

        for link in all_links:
            link_text = link.get_text().strip().lower()
            link_href = link.get('href', '')

            # Check if all parts of the player name are in the link text
            name_match = all(part in link_text for part in player_name_parts)

            # Or check if the link URL looks like a player profile
            url_match = '/prospect/' in link_href or '/player/' in link_href

            if name_match or url_match:
                player_links.append({
                    'text': link.get_text().strip(),
                    'href': link.get('href')
                })

        print(f"Found {len(player_links)} potential player links")
        for idx, link in enumerate(player_links):
            print(f"  {idx + 1}. {link['text']} - {link['href']}")

        # Try to find a match for our player
        player_link = None
        for link in player_links:
            # Prioritize links that match the player name closely
            if all(part in link['text'].lower() for part in player_name_parts):
                player_link = link
                print(f"Found matching player link: {link['text']}")
                break

        # If we found a player link, navigate to it
        if player_link:
            player_url = player_link['href']
            if not player_url.startswith('http'):
                player_url = f"https://n.rivals.com{player_url}"

            print(f"Navigating to player profile: {player_url}")
            driver.get(player_url)
            time.sleep(10)

            # Save the player profile page
            with open("debug_pages/player_profile.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Saved player profile page")

            # Take a screenshot
            driver.save_screenshot("debug_pages/player_profile.png")

            # Extract player information
            player_info = extract_player_info_from_page(driver.page_source, player_url)
        else:
            # If Method 1 fails, try Method 2: Use the basic search page
            print("No player links found in direct search. Trying standard search page...")

            driver.get("https://n.rivals.com/search")
            time.sleep(5)

            # Try to find and use the search input
            try:
                # First take a screenshot to see what we're working with
                driver.save_screenshot("debug_pages/search_page.png")

                # Look for the search input
                search_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search Prospects']")

                # Wait for it to be clickable
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Search Prospects']"))
                )

                # Use ActionChains for more robust interaction
                from selenium.webdriver.common.action_chains import ActionChains

                actions = ActionChains(driver)
                actions.move_to_element(search_input)
                actions.click()
                actions.send_keys(player_name)
                actions.send_keys(Keys.RETURN)
                actions.perform()

                print(f"Entered {player_name} in search field and submitted")
                time.sleep(10)

                # Save the search results
                with open("debug_pages/search_results_method2.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                driver.save_screenshot("debug_pages/search_results_method2.png")

                # Try to find player links again
                # The rest follows the same pattern as Method 1...
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                all_links = soup.find_all('a')

                player_links = []
                for link in all_links:
                    link_text = link.get_text().strip().lower()
                    link_href = link.get('href', '')

                    name_match = all(part in link_text for part in player_name_parts)
                    url_match = '/prospect/' in link_href or '/player/' in link_href

                    if name_match or url_match:
                        player_links.append({
                            'text': link.get_text().strip(),
                            'href': link.get('href')
                        })

                print(f"Found {len(player_links)} potential player links in Method 2")

                # Try to find a match for our player
                player_link = None
                for link in player_links:
                    if all(part in link['text'].lower() for part in player_name_parts):
                        player_link = link
                        print(f"Found matching player link: {link['text']}")
                        break

                # If we found a player link, navigate to it
                if player_link:
                    player_url = player_link['href']
                    if not player_url.startswith('http'):
                        player_url = f"https://n.rivals.com{player_url}"

                    print(f"Navigating to player profile: {player_url}")
                    driver.get(player_url)
                    time.sleep(10)

                    # Save the player profile page
                    with open("debug_pages/player_profile_method2.html", "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                    driver.save_screenshot("debug_pages/player_profile_method2.png")

                    # Extract player information
                    player_info = extract_player_info_from_page(driver.page_source, player_url)
                else:
                    print("Could not find player links in Method 2")

            except Exception as search_error:
                print(f"Error during Method 2 search: {search_error}")

    except Exception as e:
        print(f"Error during processing: {e}")

    finally:
        driver.quit()

    return player_info

def extract_player_info_from_page(html_content, player_url):
    """Extract player information from HTML content"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract player name
        player_name = None
        name_elements = soup.select("h1, .prospect-name, .player-name")

        if name_elements:
            player_name = name_elements[0].get_text().strip()
            print(f"Found player name: {player_name}")

        # If no name found, try to extract from URL
        if not player_name:
            try:
                from urllib.parse import urlparse
                path = urlparse(player_url).path
                name_part = path.split('/')[-1]  # Get last part of URL
                if name_part:
                    player_name = name_part.replace('-', ' ').title()
                    print(f"Extracted player name from URL: {player_name}")
            except:
                pass

        # Extract school information
        school = None
        school_elements = soup.select(".school, .college, [class*='school']")

        if school_elements:
            school_text = school_elements[0].get_text().strip()
            # Remove any "School:" prefix
            school = re.sub(r'^(High\s+)?School:\s*', '', school_text).strip()
            print(f"Found school: {school}")

        # If no school found directly, look for it in text patterns
        if not school:
            # Look for text that might contain school information
            for element in soup.find_all(string=re.compile(r'(High\s+)?School|College|University')):
                parent = element.parent
                text = parent.get_text().strip()
                if ':' in text:
                    school = text.split(':', 1)[1].strip()
                    print(f"Found school in text pattern: {school}")
                    break

        # Create player info dictionary
        player_info = {
            "Player Name": player_name if player_name else "Unknown",
            "School": school if school else "Unknown",
            "Profile URL": player_url
        }

        print(f"Extracted player info: {player_info}")
        return player_info

    except Exception as e:
        print(f"Error extracting player information: {e}")
        return None

def main():
    # Get player name from user
    player_name = input("Enter the player name to search for: ")

    # Search for the player and extract info
    player_info = search_player_and_extract_info(player_name)

    output_file = 'player_info.csv'

    if player_info:
        # Create a DataFrame for the current player
        player_df = pd.DataFrame([player_info])

        # Check if the CSV file already exists
        if os.path.exists(output_file):
            # Read existing CSV and append new data
            try:
                existing_df = pd.read_csv(output_file)
                combined_df = pd.concat([existing_df, player_df], ignore_index=True)

                # Remove duplicates if any (based on Profile URL)
                combined_df = combined_df.drop_duplicates(subset=["Profile URL"], keep="last")

                # Save updated DataFrame
                combined_df.to_csv(output_file, index=False)
                print(f"Player information appended to existing file '{output_file}'")
                print("\nExtracted Player Information:")
                print(player_df)
                print("\nCSV now contains information for these players:")
                print(combined_df[["Player Name", "School"]])
            except Exception as e:
                print(f"Error appending to existing CSV: {e}")
                # Fallback to creating a new file
                player_df.to_csv(output_file, index=False)
                print(f"Saved player information to new file '{output_file}'")
        else:
            # Create a new CSV file
            player_df.to_csv(output_file, index=False)
            print(f"Player information saved to new file '{output_file}'")
            print("\nExtracted Player Information:")
            print(player_df)
    else:
        print("Failed to extract player information.")

if __name__ == "__main__":
    main()