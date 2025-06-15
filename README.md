__Rivals Football Recruit Scraper 🏈__

A lightning-fast Python tool that searches for high school football players on Rivals.com and extracts their recruiting information using AI-powered data extraction.

__What It Does__

This scraper helps you quickly gather recruiting data for high school football players by:

- Searching Rivals.com for any player by name
- Extracting detailed player information from their profile pages
- Using Claude AI to intelligently parse player data
- Saving all results to a CSV file for easy analysis

__Features__

- ⚡ Ultra Fast - Optimized for speed with aggressive timeouts and minimal waiting
- 🤖 AI-Powered - Uses Claude AI to extract data accurately from complex web pages
- 📊 CSV Export - Automatically saves player data to a spreadsheet
- 🔍 Smart Search - Finds player profiles even with partial name matches
- 📈 Data Tracking - Prevents duplicates and appends new players to existing data

__Player Information Extracted__

- Name - Full player name
- High School - Current or former high school
- College Commitment - Which college they've committed to (if any)
- Position - Football position (QB, RB, WR, etc.)
- Height & Weight - Physical measurements
- Class Year - Graduation year
- Rating - Rivals recruiting rating
- Star Rating - Star ranking (3-star, 4-star, etc.)
- Location - City and state
- Profile URL - Direct link to their Rivals profile

__Installation__

1. Install Python packages:
   `pip install selenium pandas webdriver-manager requests bs4 anthropic`
2. **Download the script**: Save the Python file to your computer
3. **Get Claude API key**:
  - Sign up at Anthropic
  - Get your API key
  - Replace the API key in the code with your own
4. Install Chrome browser (required for web scraping)

__Setup__

**Important**: You need to add your own Claude API key to make this work.

In the `info_scraper.py` file, find this line:
`CLAUDE_API_KEY = "your-api-key-here"`

Replace "your-api-key-here" with your actual Claude API key from Anthropic.

__How to Use__

STEP 1. Find Player URLs
- Run the URL scraper: `python url_scraper.py`
- Enter a player name when prompted: `Enter player name: Jackson Smith`
- Wait for results - Takes 10-15 seconds per search
- Repeat for all players you want to search
- Results saved automatically to `player_urls.csv`

Step 2: Extract Player Information
- Run the info scraper: `python info_scraper.py`
- Script automatically processes all URLs from `player_urls.csv`
- Wait for AI extraction - Takes 3-5 seconds per player
- Final results saved to `scraped_players.csv`

__Example Output__

`Player info:
  name: Jackson Smith
  high_school: Central High School
  college_commitment: Ohio State
  position: Quarterback
  height: 6-2
  weight: 195
  class_year: 2024
  rating: 5.8
  stars: 4-star
  city_state: Columbus, OH`

__How It Works__

URL Scraper (url_scraper.py)
- Fast Setup - Configures Chrome browser with speed optimizations
- Smart Search - Goes to Rivals search page and looks for the player
- Profile Finding - Uses multiple methods to locate player profile URLs
- Data Saving - Stores URLs in player_urls.csv

Info Scraper (info_scraper.py)

- Page Fetching - Grabs player profile page content efficiently
- AI Processing - Sends page content to Claude AI for data extraction
- Data Parsing - Converts AI response to structured data
- CSV Export - Saves results to scraped_players.csv

__Speed Optimizations__

This scraper is built for speed with:

- Headless Chrome browser (no visual interface)
- Disabled images, plugins, and unnecessary features
- Aggressive timeouts (2-3 seconds max per page)
- Direct HTTP requests when possible
- Minimal AI processing time

__Files Created__

- player_urls.csv - Contains player names and their Rivals profile URLs
- scraped_players.csv - Contains all extracted player data in spreadsheet format
- Gets updated automatically each time you run the scripts
- Prevents duplicate entries

__Troubleshooting__

**"No profile found"** - Try:
- Different spelling of the player name
- Just first and last name
- Check if the player has a Rivals profile

**"API failed"** - Check:
- Your Claude API key is correct
- You have API credits available
- Internet connection is working

**Chrome issues** - Make sure:
- Chrome browser is installed
- ChromeDriver is compatible with your Chrome version

__Requirements__

- Python 3.7+
- Chrome browser
- Claude API key (from Anthropic)
- Internet connection
