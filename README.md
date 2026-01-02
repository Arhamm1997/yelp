# Business Profile Scrapers

This repository contains two powerful web scrapers for extracting business information:

1. **Yelp Business Scraper** - Scrapes business data from Yelp.com
2. **Google Business Profile Scraper** - Scrapes business data from Google Maps

## Features

Both scrapers include:
- 🤖 **Advanced Anti-Detection** - Stealth mode with randomized user agents and human-like behavior
- 🌍 **Multi-Location Support** - Scrape businesses across different states and cities
- 📊 **Comprehensive Data Extraction** - Business name, ratings, reviews, address, phone, website, hours
- 💾 **CSV Export** - Save all data to structured CSV files
- ⏱️ **Smart Delays** - Random timing to avoid detection
- 🔒 **Session Management** - Handles verification and captchas

## Installation

### Requirements
- Python 3.7+
- Chrome browser installed on your system

### Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd yelp
```

2. Install required packages:
```bash
pip install selenium webdriver-manager
```

The scrapers will automatically install any missing dependencies on first run.

## Usage

### Google Business Profile Scraper

The Google scraper supports **multiple states and cities** in a single run!

```bash
python google_business_scraper.py
```

**Example Usage:**
```
Enter business category: restaurants
Location 1: New York, NY
Location 2: Los Angeles, CA
Location 3: Chicago, IL
Location 4: done
Max results per location: 20
```

**Features:**
- Search across unlimited cities/states
- Specify max results per location (up to 50)
- Automatically generates timestamped CSV files
- Extracts: name, rating, reviews, address, phone, website, category, hours, Google Maps URL

**Output File Example:**
```
google_restaurants_20260102_143025.csv
```

### Yelp Business Scraper

```bash
python yelp_search_scraper.py
```

**Example Usage:**
```
Enter business category: pizza
Enter location: San Francisco, CA
How many pages to scrape: 3
```

**Features:**
- Search specific category and location
- Scrape multiple pages of results (up to 10)
- Extracts: name, rating, reviews, address, phone, website, category, hours, Yelp URL

**Output File Example:**
```
yelp_pizza_San_Francisco_CA.csv
```

## Extracted Data Fields

Both scrapers extract the following information for each business:

| Field | Description |
|-------|-------------|
| `business_name` | Name of the business |
| `rating` | Star rating (e.g., 4.5) |
| `review_count` | Number of reviews |
| `address` | Full business address |
| `phone` | Contact phone number |
| `website` | Business website URL |
| `categories` | Business category/type |
| `business_hours` | Operating hours |
| `yelp_url` / `google_maps_url` | Link to the business listing |

## Important Notes

### Anti-Detection Features

Both scrapers include:
- Randomized user agents
- Human-like scrolling and delays
- Stealth JavaScript to hide automation
- Session establishment before scraping
- Random timing between requests

### Handling Verification

If you encounter CAPTCHA or verification:

1. **Don't panic** - This is normal on first run
2. Complete the verification in the browser window
3. Browse normally for 30-60 seconds
4. Press ENTER when prompted to continue
5. The scraper will resume automatically

### Best Practices

1. **Don't scrape too aggressively**
   - Use reasonable delays (already built-in)
   - Limit results per location (20-50 recommended)
   - Take breaks between large scraping sessions

2. **Headless Mode** (Optional)
   - Uncomment `chrome_options.add_argument("--headless")` in both scripts
   - Useful for automated/server deployment
   - May increase detection risk

3. **Legal & Ethical**
   - Respect robots.txt and terms of service
   - Use data responsibly
   - Don't overload servers
   - Consider API alternatives for production use

## Troubleshooting

### Browser Not Opening
- Ensure Chrome browser is installed
- webdriver-manager will auto-install ChromeDriver

### No Results Found
- Check your search terms (category and location)
- Try different selectors if page structure changed
- Verify you're not blocked (complete CAPTCHA if prompted)

### "Element not found" Errors
- Website layouts change frequently
- The scraper includes multiple fallback selectors
- May need updates if major site redesign occurs

### Slow Performance
- Delays are intentional to avoid detection
- You can reduce delays in the code (not recommended)
- Headless mode may be slightly faster

## Advanced Configuration

### Modify Delays

Edit the delay ranges in either script:

```python
# Quick delays
time.sleep(random.uniform(0.5, 1))  # Change range as needed

# Medium delays
time.sleep(random.uniform(1, 2))    # Between page loads

# Long delays
time.sleep(random.uniform(3, 6))    # Between locations
```

### Change Maximum Results

**Google Scraper:**
```python
max_results = 50  # Change in main() or via prompt
```

**Yelp Scraper:**
```python
max_pages = 10    # Change in main() or via prompt
```

### Add Custom User Agents

Add more user agents to the list in `get_driver()`:

```python
user_agents = [
    "Your custom user agent here",
    # ... existing agents
]
```

## Comparison: Google vs Yelp Scraper

| Feature | Google Scraper | Yelp Scraper |
|---------|---------------|--------------|
| Multi-location | ✅ Unlimited | ❌ One at a time |
| Results per search | Up to 50+ | ~10 per page |
| Category detection | ✅ Auto-detected | Uses search term |
| Hours format | Detailed table | Semicolon-separated |
| Session handling | ✅ Maps homepage | ✅ Yelp homepage |
| Best for | Wide geographic coverage | Deep local search |

## Output Examples

### Google Scraper Output
```csv
business_name,rating,review_count,address,phone,website,categories,business_hours,google_maps_url
"Joe's Pizza",4.6,1234,"123 Main St, New York, NY 10001",(212) 555-0100,https://joespizza.com,Pizza restaurant,"Mon-Sun 11AM-11PM",https://maps.google.com/...
```

### Yelp Scraper Output
```csv
business_name,rating,review_count,address,phone,website,categories,business_hours,yelp_url
"Tony's Pizzeria",4.5,856,"456 Oak Ave, San Francisco, CA 94102",(415) 555-0200,https://tonyspizzeria.com,pizza,"Monday 11:00 AM - 10:00 PM; Tuesday...",https://yelp.com/biz/...
```

## Contributing

Feel free to submit issues or pull requests to improve the scrapers!

## License

This project is for educational purposes. Always review and comply with the terms of service of websites you scrape.

## Disclaimer

These scrapers are provided as-is for educational and research purposes. The user is responsible for:
- Complying with all applicable laws and regulations
- Respecting website terms of service
- Using scraped data ethically and legally
- Not causing harm or overload to target websites

**Use responsibly and at your own risk.**

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the code comments for detailed explanations
3. Open an issue on GitHub

---

**Happy Scraping! 🚀**
