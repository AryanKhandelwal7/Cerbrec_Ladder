!pip install selenium pandas webdriver-manager requests bs4
!pip install anthropic

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
import json
import requests


# Configure your Claude API key here
CLAUDE_API_KEY = "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"
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"


def get_text_or_none(element):
    """Helper function to safely extract text from BeautifulSoup elements"""
    return element.text.strip() if element else None


def setup_chrome():
    """Setup Chrome with MAXIMUM SPEED options"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-images')
    chrome_options.add_argument('--disable-plugins')
    chrome_options.add_argument('--disable-background-timer-throttling')
    chrome_options.add_argument('--disable-backgrounding-occluded-windows')
    chrome_options.add_argument('--disable-renderer-backgrounding')
    chrome_options.add_argument('--disable-features=TranslateUI')
    chrome_options.add_argument('--disable-default-apps')
    chrome_options.add_argument('--no-first-run')
    chrome_options.add_argument('--fast-start')
    chrome_options.add_argument('--disable-background-networking')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values": {
            "images": 2,
            "plugins": 2,
            "popups": 2,
            "geolocation": 2,
            "notifications": 2,
            "media_stream": 2,
        }
    })
    return chrome_options


def extract_player_info_quick(html_content, player_url):
    """Send HTML directly to Claude API for extraction - ULTRA FAST"""

    print("🚀 Sending to Claude API...")

    # ULTRA FAST HTML cleaning
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove junk FAST
    for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
        tag.decompose()

    # Get text and cut it down FAST
    text = soup.get_text()
    text = ' '.join(text.split())  # Remove whitespace

    # AGGRESSIVE truncation for speed
    if len(text) > 3000:
        text = text[:3000]

    # MINIMAL prompt for SPEED
    prompt = f"""Extract player data from this football recruit page. Return JSON only:


{text}


JSON format:
{{"name":"","high_school":"","college_commitment":"","position":"","height":"","weight":"","class_year":"","rating":"","stars":"","city_state":""}}"""


    headers = {
        "Content-Type": "application/json",
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01"
    }

    data = {
        "model": "claude-3-haiku-20240307",  # FASTEST model
        "max_tokens": 300,  # MINIMAL tokens
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        start = time.time()
        response = requests.post(CLAUDE_API_URL, headers=headers, json=data, timeout=3)  # 3 second timeout
        api_time = time.time() - start
        print(f"⚡ Claude API: {api_time:.1f}s")

        if response.status_code == 200:
            content = response.json()['content'][0]['text'].strip()

            # FAST JSON extraction
            if '{' in content and '}' in content:
                json_str = content[content.find('{'):content.rfind('}')+1]
                player_data = json.loads(json_str)
                player_data['profile_url'] = player_url
                player_data['source'] = 'rivals'
                print("✅ SUCCESS!")
                return player_data

    except Exception as e:
        print(f"❌ API failed: {e}")

    # INSTANT fallback
    return create_fallback_data("Jackson Cantwell", player_url)


def create_fallback_data(player_name, player_url):
    """Create basic fallback data when Claude fails"""
    try:
        # Try to extract name from URL
        path = player_url.split('/')[-1]
        if '-' in path:
            parts = path.split('-')[:2]
            name = ' '.join(parts).title()
        else:
            name = player_name
    except:
        name = player_name

    return {
        'name': name,
        'high_school': 'Unknown',
        'college_commitment': 'Unknown',
        'position': 'Unknown',
        'height': 'Unknown',
        'weight': 'Unknown',
        'class_year': 'Unknown',
        'rating': 'Unknown',
        'stars': 'Unknown',
        'city_state': 'Unknown',
        'profile_url': player_url,
        'source': 'rivals'
    }


def search_player_quick(player_name):
    """ULTRA FAST player search"""
    print(f"🔍 Searching: {player_name}")
    chrome_options = setup_chrome()

    # ADD EXTREME SPEED OPTIONS
    chrome_options.add_argument('--aggressive-cache-discard')
    chrome_options.add_argument('--disable-background-timer-throttling')
    chrome_options.add_argument('--disable-renderer-backgrounding')
    chrome_options.add_argument('--disable-backgrounding-occluded-windows')
    chrome_options.add_argument('--disable-client-side-phishing-detection')
    chrome_options.add_argument('--disable-default-apps')
    chrome_options.add_argument('--disable-hang-monitor')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-prompt-on-repost')
    chrome_options.add_argument('--disable-sync')
    chrome_options.add_argument('--disable-web-resources')
    chrome_options.add_argument('--max_old_space_size=4096')
    chrome_options.add_argument('--no-first-run')
    chrome_options.add_argument('--no-service-autorun')
    chrome_options.add_argument('--password-store=basic')
    chrome_options.add_argument('--use-mock-keychain')


    try:
        driver = webdriver.Chrome(options=chrome_options)

        # AGGRESSIVE timeouts
        driver.set_page_load_timeout(2)  # 2 seconds max
        driver.implicitly_wait(0.3)


        print("📄 Loading search...")
        try:
            driver.get("https://n.rivals.com/search")
            time.sleep(0.5)  # Minimal wait
        except:
            print("⚠️ Timeout - continuing...")


        # FAST search input finding
        search_input = None
        for selector in ["input[placeholder*='Search']", "input[type='search']", "input"]:
            try:
                search_input = driver.find_element(By.CSS_SELECTOR, selector)
                if search_input.is_displayed():
                    break
            except:
                continue


        if not search_input:
            driver.quit()
            return None


        # INSTANT search
        search_input.clear()
        search_input.send_keys(player_name)
        search_input.send_keys(Keys.RETURN)
        print(f"🔎 Searched: {player_name}")


        # MINIMAL wait for results
        time.sleep(0.8)


        # FAST link scanning
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        name_parts = player_name.lower().split()


        for link in soup.find_all('a', href=True):
            link_text = link.get_text().strip().lower()
            link_href = link.get('href', '')


            # Quick name match
            if any(part in link_text for part in name_parts) and len(link_text) > 5:
                # Quick URL match
                if any(x in link_href for x in ['/content/', '/athletes/', '/prospect/']):

                    if not link_href.startswith('http'):
                        player_url = f"https://n.rivals.com{link_href}"
                    else:
                        player_url = link_href


                    print(f"🎯 Found: {player_url}")


                    # SPEED HACK: Try direct HTTP request first (bypasses Selenium loading)
                    try:
                        print("⚡ Trying direct fetch...")
                        import requests
                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                        resp = requests.get(player_url, headers=headers, timeout=2)

                        if resp.status_code == 200 and len(resp.text) > 1000:
                            driver.quit()
                            return extract_player_info_quick(resp.text, player_url)
                    except:
                        pass


                    # Fallback to Selenium with MINIMAL wait
                    try:
                        driver.set_page_load_timeout(1.5)  # Even more aggressive
                        driver.get(player_url)
                        time.sleep(0.3)  # Tiny wait

                        html = driver.page_source
                        driver.quit()
                        return extract_player_info_quick(html, player_url)

                    except:
                        driver.quit()
                        return create_fallback_data(player_name, player_url)


        print("❌ No profile found")
        driver.quit()
        return None


    except Exception as e:
        print(f"💥 Error: {e}")
        try:
            driver.quit()
        except:
            pass
        return None


def main():
    player_name = input("Enter player name: ")


    start_time = time.time()
    player_info = search_player_quick(player_name)
    end_time = time.time()


    print(f"Time: {end_time - start_time:.2f} seconds")


    if player_info:
        # Save to CSV with ALL the new fields
        df = pd.DataFrame([player_info])
        output_file = 'quick_rivals.csv'


        if os.path.exists(output_file):
            try:
                existing_df = pd.read_csv(output_file)
                # Combine dataframes, handling any missing columns
                combined_df = pd.concat([existing_df, df], ignore_index=True, sort=False)
                # Remove duplicates based on profile URL
                combined_df = combined_df.drop_duplicates(subset=['profile_url'], keep='last')
                combined_df.to_csv(output_file, index=False)
                print(f"Added to existing {output_file}")
            except Exception as e:
                print(f"Error appending to CSV: {e}")
                # Fallback: create new file
                df.to_csv(output_file, index=False)
                print(f"Created new {output_file}")
        else:
            df.to_csv(output_file, index=False)
            print(f"Created new {output_file}")


        print("Player info:")
        for key, value in player_info.items():
            print(f"  {key}: {value}")
    else:
        print("Failed to find player")


if __name__ == "__main__":
    main()
