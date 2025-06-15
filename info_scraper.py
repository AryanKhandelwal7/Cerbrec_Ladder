#PART 2 : info_scraper.py --> utilizes the urls from player_urls.csv and sends over to Claude to create the scraped_players.csv

import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import json
import requests
from selenium.common.exceptions import TimeoutException


# Configure your Claude API key here
CLAUDE_API_KEY = "ADD_CLAUDE_KEY"
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"


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
    chrome_options.add_argument('--aggressive-cache-discard')
    chrome_options.add_argument('--disable-client-side-phishing-detection')
    chrome_options.add_argument('--disable-hang-monitor')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-sync')
    chrome_options.add_argument('--disable-web-resources')
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


def extract_player_info_claude_api(html_content, player_url, player_name=""):
    """Send HTML directly to Claude API for extraction - ULTRA FAST"""
    
    print(f"🚀 Sending to Claude API for: {player_name}")
    
    # ULTRA FAST HTML cleaning
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove junk FAST
    for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'iframe', 'img']):
        tag.decompose()
    
    # Get text and cut it down FAST
    text = soup.get_text()
    text = ' '.join(text.split())  # Remove whitespace
    
    # AGGRESSIVE truncation for speed
    if len(text) > 3000:
        text = text[:3000]
    
    # ENHANCED prompt for better extraction
    prompt = f"""Extract player data from this football recruit page. Return ONLY valid JSON:

{text}

JSON format:
{{"name":"","high_school":"","college_commitment":"","position":"","height":"","weight":"","class_year":"","rating":"","stars":"","city_state":"","hometown":"","state":"","recruiting_status":"","offers":""}}"""
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    
    data = {
        "model": "claude-3-haiku-20240307",  # FASTEST model
        "max_tokens": 400,  # Increased for more data
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        start = time.time()
        response = requests.post(CLAUDE_API_URL, headers=headers, json=data, timeout=5)
        api_time = time.time() - start
        print(f"⚡ Claude API: {api_time:.1f}s")
        
        if response.status_code == 200:
            content = response.json()['content'][0]['text'].strip()
            
            # ENHANCED JSON extraction
            if '{' in content and '}' in content:
                json_str = content[content.find('{'):content.rfind('}')+1]
                try:
                    player_data = json.loads(json_str)
                    player_data['profile_url'] = player_url
                    player_data['source'] = 'rivals'
                    player_data['scraped_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
                    print("✅ SUCCESS!")
                    return player_data
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    
        else:
            print(f"API error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ API failed: {e}")
    
    # INSTANT fallback
    return create_fallback_data(player_name, player_url)


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
        'hometown': 'Unknown',
        'state': 'Unknown',
        'recruiting_status': 'Unknown',
        'offers': 'Unknown',
        'profile_url': player_url,
        'source': 'rivals',
        'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }


def fetch_player_page(player_url, player_name=""):
    """Fetch player page using fastest method available"""
    print(f"📄 Fetching: {player_url}")
    
    # Method 1: Direct HTTP request (FASTEST)
    try:
        print("⚡ Trying direct HTTP fetch...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(player_url, headers=headers, timeout=5)
        
        if response.status_code == 200 and len(response.text) > 1000:
            print(f"✅ Direct fetch successful ({len(response.text)} chars)")
            return response.text
            
    except Exception as e:
        print(f"Direct fetch failed: {e}")
    
    # Method 2: Selenium fallback
    try:
        print("🔄 Falling back to Selenium...")
        chrome_options = setup_chrome()
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.set_page_load_timeout(3)
        driver.get(player_url)
        time.sleep(0.5)  # Minimal wait
        
        html = driver.page_source
        driver.quit()
        
        print(f"✅ Selenium fetch successful ({len(html)} chars)")
        return html
        
    except Exception as e:
        print(f"Selenium fetch failed: {e}")
        try:
            driver.quit()
        except:
            pass
    
    return None


def process_csv_file(csv_file_path, url_column='profile_url', name_column='player_name'):
    """Process entire CSV file and scrape all player information"""
    
    print(f"📁 Processing CSV: {csv_file_path}")
    
    # Read CSV file
    try:
        df = pd.read_csv(csv_file_path)
        print(f"📊 Found {len(df)} rows in CSV")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return None
    
    # Validate required columns
    if url_column not in df.columns:
        print(f"❌ Column '{url_column}' not found in CSV")
        print(f"Available columns: {list(df.columns)}")
        return None
    
    # Create results list
    all_results = []
    successful_scrapes = 0
    failed_scrapes = 0
    
    print(f"🚀 Starting to scrape {len(df)} players...")
    start_time = time.time()
    
    for index, row in df.iterrows():
        player_url = row[url_column]
        player_name = row.get(name_column, f"Player_{index}")
        
        print(f"\n{'='*50}")
        print(f"🎯 [{index+1}/{len(df)}] Processing: {player_name}")
        print(f"🔗 URL: {player_url}")
        
        # Skip if URL is invalid
        if pd.isna(player_url) or player_url == 'NOT_FOUND' or not str(player_url).startswith('http'):
            print("⏭️ Skipping invalid URL")
            failed_scrapes += 1
            continue
        
        try:
            # Fetch the page
            html_content = fetch_player_page(player_url, player_name)
            
            if html_content:
                # Extract info using Claude API
                player_info = extract_player_info_claude_api(html_content, player_url, player_name)
                
                if player_info:
                    # Add original CSV data
                    for col in df.columns:
                        if col not in player_info:
                            player_info[f'original_{col}'] = row[col]
                    
                    all_results.append(player_info)
                    successful_scrapes += 1
                    print(f"✅ Success! Extracted info for {player_info.get('name', player_name)}")
                else:
                    failed_scrapes += 1
                    print("❌ Failed to extract player info")
            else:
                failed_scrapes += 1
                print("❌ Failed to fetch page content")
                
        except Exception as e:
            print(f"❌ Error processing {player_name}: {e}")
            failed_scrapes += 1
        
        # Add small delay to be respectful
        time.sleep(0.5)
    
    # Save results - AMEND to existing file or create new
    if all_results:
        output_file = "scraped_players.csv"
        results_df = pd.DataFrame(all_results)
        
        # Check if file exists and amend
        if os.path.exists(output_file):
            try:
                print(f"📁 Found existing {output_file} - amending...")
                existing_df = pd.read_csv(output_file)
                
                # Combine dataframes
                combined_df = pd.concat([existing_df, results_df], ignore_index=True, sort=False)
                
                # Remove duplicates based on profile_url (keep latest)
                combined_df = combined_df.drop_duplicates(subset=['profile_url'], keep='last')
                
                # Save combined results
                combined_df.to_csv(output_file, index=False)
                
                print(f"✅ Amended existing file with {len(results_df)} new records")
                print(f"📊 Total records in file: {len(combined_df)}")
                
            except Exception as e:
                print(f"⚠️ Error amending file: {e}")
                print("💾 Creating backup and saving new file...")
                # Backup existing file
                backup_file = f"scraped_players_backup_{int(time.time())}.csv"
                if os.path.exists(output_file):
                    os.rename(output_file, backup_file)
                    print(f"📋 Existing file backed up as: {backup_file}")
                
                # Save new results
                results_df.to_csv(output_file, index=False)
                print(f"✅ New file created: {output_file}")
        else:
            # Create new file
            results_df.to_csv(output_file, index=False)
            print(f"✅ Created new file: {output_file}")
        
        elapsed_time = time.time() - start_time
        
        print(f"\n🎉 SCRAPING COMPLETE!")
        print(f"⏱️ Total time: {elapsed_time:.1f} seconds")
        print(f"✅ Successful: {successful_scrapes}")
        print(f"❌ Failed: {failed_scrapes}")
        print(f"📁 Results in: {output_file}")
        print(f"📊 Columns extracted: {list(results_df.columns)}")
        
        return output_file
    else:
        print("❌ No results to save")
        return None


def main():
    """Main function to run the CSV scraper - AUTOMATIC"""
    
    print("🏈 AUTOMATIC Player Information Scraper with Claude API")
    print("=" * 50)
    
    # Automatically look for player_urls.csv
    csv_file = "player_urls.csv"
    
    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
        print("Make sure 'player_urls.csv' exists in the current directory")
        return
    
    print(f"✅ Found: {csv_file}")
    
    # Auto-detect column names
    try:
        sample_df = pd.read_csv(csv_file, nrows=1)
        columns = list(sample_df.columns)
        print(f"📊 Detected columns: {columns}")
        
        # Auto-detect URL column
        url_column = None
        for col in ['profile_url', 'url', 'player_url', 'link']:
            if col in columns:
                url_column = col
                break
        
        if not url_column:
            # Take first column that might contain URLs
            for col in columns:
                if 'url' in col.lower() or 'link' in col.lower():
                    url_column = col
                    break
        
        if not url_column:
            url_column = 'profile_url'  # Default
        
        # Auto-detect name column
        name_column = None
        for col in ['player_name', 'name', 'full_name']:
            if col in columns:
                name_column = col
                break
        
        if not name_column:
            name_column = 'player_name'  # Default
        
        print(f"🎯 Auto-detected URL column: '{url_column}'")
        print(f"🎯 Auto-detected name column: '{name_column}'")
        
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return
    
    # Process the CSV automatically
    print(f"\n🚀 Starting automatic scraping...")
    result_file = process_csv_file(csv_file, url_column, name_column)
    
    if result_file:
        print(f"\n🎯 SCRAPING COMPLETED SUCCESSFULLY!")
        print(f"📁 Results saved to: {result_file}")
    else:
        print("\n❌ Scraping failed")


if __name__ == "__main__":
    main()
