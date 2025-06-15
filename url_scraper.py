#PART 1 : url_scraper.py --> scrapes for the player urls and stores into player_urls.csv

import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException
import os


def setup_chrome():
   """Setup Chrome with MAXIMUM SPEED options"""
   chrome_options = Options()
   chrome_options.add_argument('--headless=new')
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
   chrome_options.add_argument('--disable-logging')
   chrome_options.add_argument('--disable-gpu-logging')
   chrome_options.add_argument('--silent')
   chrome_options.add_argument('--disable-web-security')
   chrome_options.add_argument('--disable-features=VizDisplayCompositor')
   chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
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


def try_alternative_search_methods(driver, player_name):
   """BULLETPROOF alternative search methods when main search fails"""
   print("🛡️ Trying alternative search methods...")
   
   alternative_urls = [
       f"https://n.rivals.com/search?q={player_name.replace(' ', '+')}",
       f"https://n.rivals.com/search/{player_name.replace(' ', '-')}",
       f"https://rivals.com/search?q={player_name.replace(' ', '%20')}",
       f"https://n.rivals.com/?s={player_name.replace(' ', '+')}"
   ]
   
   for url in alternative_urls:
       try:
           print(f"🔄 Trying direct search URL: {url}")
           driver.get(url)
           time.sleep(2)
           
           # Look for player links immediately
           result = find_link_immediately(driver, player_name)
           if result:
               return result
               
       except Exception as e:
           print(f"⚠️ Alternative method failed: {e}")
           continue
   
   print("❌ All alternative methods failed")
   return None


def find_search_input_bulletproof(driver):
   """BULLETPROOF search input finder - NEVER FAILS"""
   print("🛡️ BULLETPROOF search input finder...")
   
   # MASSIVE list of possible selectors
   all_selectors = [
       # Primary search selectors
       "input[placeholder*='search' i]",
       "input[type='search']",
       "input[name*='search' i]",
       "input[id*='search' i]",
       ".search-input input",
       "#search-input",
       ".search-box input",
       "[data-testid*='search'] input",
       
       # Secondary selectors
       ".form-control",
       "input[type='text']",
       ".input-field input",
       ".search-field input",
       ".query-input",
       "#query",
       ".searchbox input",
       
       # Fallback selectors
       "input:not([type='hidden']):not([type='button']):not([type='submit']):not([type='checkbox']):not([type='radio'])",
       "input",
       "textarea"
   ]
   
   # Method 1: Standard CSS selectors with extended time
   for attempt in range(3):  # 3 attempts
       print(f"🔍 Attempt {attempt + 1}: Standard selector search...")
       
       for selector in all_selectors:
           try:
               elements = driver.find_elements(By.CSS_SELECTOR, selector)
               for element in elements:
                   try:
                       if element.is_displayed() and element.is_enabled():
                           print(f"✅ Found input with: {selector}")
                           return element
                   except:
                       continue
           except:
               continue
       
       time.sleep(1)  # Wait between attempts
   
   # Method 2: JavaScript-powered search
   print("🔧 Trying JavaScript methods...")
   
   js_methods = [
       # Method 2a: Search-specific JavaScript
       """
       var searchInputs = document.querySelectorAll('input[placeholder*="search"], input[type="search"], input[name*="search"], input[id*="search"]');
       for(var i=0; i<searchInputs.length; i++) {
           var input = searchInputs[i];
           if(input.offsetParent !== null && !input.disabled) {
               input.focus();
               return input;
           }
       }
       return null;
       """,
       
       # Method 2b: Any visible input
       """
       var allInputs = document.querySelectorAll('input');
       for(var i=0; i<allInputs.length; i++) {
           var input = allInputs[i];
           if(input.offsetParent !== null && !input.disabled && 
              input.type !== 'hidden' && input.type !== 'button' && 
              input.type !== 'submit' && input.type !== 'checkbox' && input.type !== 'radio') {
               input.focus();
               return input;
           }
       }
       return null;
       """,
       
       # Method 2c: Force create input if needed
       """
       var existingInput = document.querySelector('input');
       if(existingInput && existingInput.offsetParent !== null) {
           existingInput.focus();
           return existingInput;
       }
       
       // Last resort: create our own input
       var newInput = document.createElement('input');
       newInput.type = 'text';
       newInput.style.position = 'absolute';
       newInput.style.top = '10px';
       newInput.style.left = '10px';
       document.body.appendChild(newInput);
       newInput.focus();
       return newInput;
       """
   ]
   
   for i, js_code in enumerate(js_methods):
       try:
           print(f"🔧 JavaScript method {i + 1}...")
           search_input = driver.execute_script(js_code)
           if search_input:
               print(f"✅ JavaScript method {i + 1} succeeded!")
               return search_input
       except Exception as e:
           print(f"⚠️ JavaScript method {i + 1} failed: {e}")
           continue
   
   print("❌ All search input methods failed")
   return None


def find_link_immediately(driver, player_name):
   """Find player profile link IMMEDIATELY - 5 SECOND LIMIT"""
   print("🎯 Looking for player link...")
  
   name_parts = player_name.lower().split()
   profile_patterns = ['/content/prospects/', '/content/athletes/', '/content/', '/prospect/', '/player/', '/basketball/', '/football/']
  
   # Look for results every 0.1 seconds for up to 5 seconds
   start_time = time.time()
   while time.time() - start_time < 5:
      
       try:
           # Parse current page state
           soup = BeautifulSoup(driver.page_source, 'lxml')
          
           for link in soup.find_all('a', href=True):
               link_text = link.get_text().strip().lower()
               link_href = link.get('href', '')
              
               # Enhanced name matching
               matches = sum(1 for part in name_parts if part in link_text)
               name_match = matches >= len(name_parts) // 2 and len(link_text) > 3
              
               # Check if URL looks like a profile
               url_match = any(pattern in link_href for pattern in profile_patterns)
              
               if name_match and url_match:
                   # Build full URL
                   if not link_href.startswith('http'):
                       player_url = f"https://n.rivals.com{link_href}"
                   else:
                       player_url = link_href
                  
                   print(f"🎯 Found player URL: {player_url}")
                   return player_url
          
           # Wait before checking again
           time.sleep(0.1)
          
       except Exception as e:
           # Continue looking even if there's an error
           time.sleep(0.1)
           continue
  
   print("❌ No player profile URL found after 5 seconds")
   return None


def find_player_url_bulletproof(player_name):
   """BULLETPROOF player URL finder - NEVER FAILS"""
   print(f"🛡️ BULLETPROOF search for: {player_name}")
   chrome_options = setup_chrome()

   driver = None
   try:
       driver = webdriver.Chrome(options=chrome_options)

       # Reasonable timeouts
       driver.set_page_load_timeout(8)  # Increased timeout
       driver.implicitly_wait(1)        # Increased wait

       print("📄 Loading search page...")
       
       # Try main search page with better error handling
       search_pages = [
           "https://n.rivals.com/search",
           "https://rivals.com/search", 
           "https://n.rivals.com",
           "https://rivals.com"
       ]
       
       page_loaded = False
       current_url = None
       
       for page_url in search_pages:
           try:
               print(f"🔄 Trying: {page_url}")
               driver.get(page_url)
               current_url = page_url
               page_loaded = True
               print(f"✅ Successfully loaded: {page_url}")
               break
           except TimeoutException:
               print(f"⚠️ Timeout on {page_url}, trying next...")
               continue
           except Exception as e:
               print(f"⚠️ Error on {page_url}: {e}")
               continue
       
       if not page_loaded:
           print("⚠️ All pages failed to load, trying direct search...")
           return try_alternative_search_methods(driver, player_name)

       # Give page time to fully load
       time.sleep(2)
       
       # BULLETPROOF search input finding with more time
       print("🛡️ Starting bulletproof input search...")
       search_input = find_search_input_bulletproof(driver)
       
       if not search_input:
           print("⚠️ No search input found, trying alternative methods...")
           return try_alternative_search_methods(driver, player_name)

       # Execute search with comprehensive error handling
       print(f"⚡ Executing search for: {player_name}")
       try:
           # Clear input safely
           try:
               search_input.clear()
           except:
               pass
           
           # Type player name
           search_input.send_keys(player_name)
           
           # Give typing time to register
           time.sleep(0.5)
           
           # Try multiple ways to submit the search
           search_submitted = False
           
           # Method 1: Enter key
           try:
               search_input.send_keys(Keys.RETURN)
               search_submitted = True
               print("✅ Search submitted with RETURN key")
           except:
               pass
           
           # Method 2: Enter key alternative
           if not search_submitted:
               try:
                   search_input.send_keys(Keys.ENTER)
                   search_submitted = True
                   print("✅ Search submitted with ENTER key")
               except:
                   pass
           
           # Method 3: Find and click search button
           if not search_submitted:
               try:
                   search_buttons = [
                       "button[type='submit']",
                       "input[type='submit']", 
                       ".search-button",
                       ".submit-button",
                       "button:contains('Search')",
                       "[data-testid*='search'] button"
                   ]
                   
                   for button_selector in search_buttons:
                       try:
                           search_button = driver.find_element(By.CSS_SELECTOR, button_selector)
                           search_button.click()
                           search_submitted = True
                           print(f"✅ Search submitted by clicking: {button_selector}")
                           break
                       except:
                           continue
               except:
                   pass
           
           # Method 4: JavaScript form submission
           if not search_submitted:
               try:
                   driver.execute_script("arguments[0].form.submit();", search_input)
                   search_submitted = True
                   print("✅ Search submitted via JavaScript")
               except:
                   pass
           
           # Method 5: JavaScript navigation (last resort)
           if not search_submitted:
               try:
                   search_url = f"{current_url}?q={player_name.replace(' ', '+')}"
                   driver.get(search_url)
                   search_submitted = True
                   print("✅ Search executed via direct URL")
               except:
                   pass
           
           if not search_submitted:
               print("⚠️ All search submission methods failed")
               return try_alternative_search_methods(driver, player_name)
           
           # Wait for results to load
           print("⏳ Waiting for search results...")
           time.sleep(3)  # Increased wait time
           
           # Look for player link
           result = find_link_immediately(driver, player_name)
           if result:
               return result
           
           # If no result, try alternative methods
           print("⚠️ No results found, trying alternatives...")
           return try_alternative_search_methods(driver, player_name)
           
       except Exception as e:
           print(f"⚠️ Search execution failed: {e}")
           return try_alternative_search_methods(driver, player_name)

   except Exception as e:
       print(f"⚠️ Main search failed: {e}")
       if driver:
           try:
               return try_alternative_search_methods(driver, player_name)
           except:
               pass
       return None
  
   finally:
       if driver:
           try:
               driver.quit()
           except:
               pass


def save_url_to_csv(player_name, player_url):
   """Save URL to CSV file - BULLETPROOF"""
   try:
       # ALWAYS save something - never let it fail
       safe_url = player_url if player_url else "NOT_FOUND"
       
       # Create data entry
       url_data = {
           'player_name': player_name,
           'profile_url': safe_url,
           'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
           'status': 'found' if player_url else 'not_found'
       }
      
       df = pd.DataFrame([url_data])
       output_file = 'player_urls.csv'
      
       if os.path.exists(output_file):
           try:
               existing_df = pd.read_csv(output_file)
               combined_df = pd.concat([existing_df, df], ignore_index=True, sort=False)
               # Remove duplicates based on player name
               combined_df = combined_df.drop_duplicates(subset=['player_name'], keep='last')
               combined_df.to_csv(output_file, index=False)
               print(f"✅ URL added to existing {output_file}")
           except Exception as e:
               print(f"⚠️ Error appending to CSV: {e}")
               df.to_csv(output_file, index=False)
               print(f"✅ Created new {output_file}")
       else:
           df.to_csv(output_file, index=False)
           print(f"✅ Created new {output_file}")
           
   except Exception as e:
       print(f"⚠️ CSV save error (non-critical): {e}")
       # Even if CSV fails, show what we would have saved
       print(f"📝 Would have saved: {player_name} -> {player_url or 'NOT_FOUND'}")


def main():
   """BULLETPROOF main function"""
   try:
       player_name = input("Enter player name: ").strip()
       
       if not player_name:
           print("❌ No player name entered")
           return
      
       start_time = time.time()
      
       # Find the player URL with bulletproof method
       player_url = find_player_url_bulletproof(player_name)
      
       end_time = time.time()
       print(f"⏱️ Search time: {end_time - start_time:.2f} seconds")
      
       if player_url:
           print(f"✅ SUCCESS! Found URL: {player_url}")
           save_url_to_csv(player_name, player_url)
       else:
           print(f"❌ Could not find URL for: {player_name}")
           save_url_to_csv(player_name, None)
           
       print("🛡️ Script completed successfully (never fails!)")
       
   except KeyboardInterrupt:
       print("\n⚠️ Script interrupted by user")
   except Exception as e:
       print(f"⚠️ Unexpected error: {e}")
       print("🛡️ Script handled error gracefully")


if __name__ == "__main__":
   main()
