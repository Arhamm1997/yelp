import csv
import time
import random
import re
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    """Initialize Chrome WebDriver with enhanced anti-detection settings"""
    chrome_options = Options()

    # Enhanced anti-detection measures
    # chrome_options.add_argument("--headless")  # Uncomment for headless mode

    # For production/deployment
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-background-networking")

    # Randomize user agent from a pool of recent Chrome versions
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    ]

    selected_ua = random.choice(user_agents)
    chrome_options.add_argument(f"user-agent={selected_ua}")

    # Additional stealth measures
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("detach", True)

    # Add some realistic browser preferences
    prefs = {
        "profile.default_content_setting_values": {
            "notifications": 2,
            "geolocation": 1,  # Allow geolocation for Google Maps
        },
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.images": 1
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Add window size randomization
    window_sizes = ["1920,1080", "1366,768", "1536,864", "1440,900"]
    selected_size = random.choice(window_sizes)
    chrome_options.add_argument(f"--window-size={selected_size}")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    # Enhanced stealth JavaScript execution
    stealth_js = """
    // Remove webdriver property
    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});

    // Override the plugins property to add realistic values
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5]
    });

    // Override languages property
    Object.defineProperty(navigator, 'languages', {
        get: () => ['en-US', 'en']
    });

    // Override platform
    Object.defineProperty(navigator, 'platform', {
        get: () => 'Win32'
    });

    // Add realistic viewport
    Object.defineProperty(screen, 'availHeight', {get: () => 1040});
    Object.defineProperty(screen, 'availWidth', {get: () => 1920});

    // Override permission query
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
            Promise.resolve({ state: Notification.permission }) :
            originalQuery(parameters)
    );

    // Add realistic timing
    const originalPerformanceNow = performance.now;
    let startTime = Date.now();
    performance.now = () => Date.now() - startTime;
    """

    driver.execute_script(stealth_js)

    # Set realistic viewport and simulate human behavior
    driver.execute_script("window.scrollTo(0, 100);")
    time.sleep(random.uniform(0.5, 1.5))

    return driver

def establish_session(driver):
    """Establish a verified session with Google Maps before starting scraping"""
    print("🔐 Establishing verified session with Google Maps...")

    # Visit Google Maps homepage first
    print("🏠 Visiting Google Maps homepage...")
    driver.get("https://www.google.com/maps")
    time.sleep(random.uniform(3, 5))

    # Check for initial bot detection or CAPTCHA
    page_source = driver.page_source.lower()
    bot_indicators = [
        'verify', 'captcha', 'robot', 'security check', 'unusual traffic',
        'blocked', 'suspicious', 'automation', 'bot', 'verify you are human',
        'prove you are not a robot', 'please verify', 'access denied'
    ]

    if any(indicator in page_source for indicator in bot_indicators):
        print("\n" + "="*70)
        print("🚨 INITIAL GOOGLE VERIFICATION REQUIRED!")
        print("="*70)
        print("❌ Google requires verification before we can start scraping.")
        print("🔧 This is a one-time setup step.")
        print("")
        print("📋 MANUAL STEPS REQUIRED:")
        print("1. ✅ Complete any verification (CAPTCHA, etc.) in the browser")
        print("2. ✅ Browse normally for 30-60 seconds (scroll, click around)")
        print("3. ✅ Close any popup windows or notifications")
        print("4. ✅ Navigate to any Google Maps search to confirm access")
        print("5. ✅ Press ENTER here when ready to continue...")
        print("")
        print("💡 Note: This verification only needs to be done once per session!")
        print("="*70)

        input("🔑 Press ENTER after completing verification: ")
        print("✅ Session verification completed! Starting scraping...")
        time.sleep(2)
    else:
        print("✅ No initial verification required. Session established!")

    # Simulate human browsing on homepage
    print("👁️ Simulating natural browsing behavior...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
    time.sleep(random.uniform(1, 2))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(random.uniform(1, 2))
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(random.uniform(1, 2))

def search_google_maps_businesses(driver, category, location, max_results=20):
    """Search Google Maps for businesses based on category and location"""
    business_data = []

    try:
        # Construct search query
        search_query = f"{category} in {location}"
        search_url = f"https://www.google.com/maps/search/{urllib.parse.quote(search_query)}"

        print(f"🔍 Searching: {search_query}")
        print(f"🔗 URL: {search_url}")

        driver.get(search_url)

        # Wait for results to load
        time.sleep(random.uniform(3, 5))

        # Simulate human reading behavior
        print("👁️ Simulating human reading behavior...")
        driver.execute_script("window.scrollTo(0, 200);")
        time.sleep(random.uniform(0.5, 1))
        driver.execute_script("window.scrollTo(0, 400);")
        time.sleep(random.uniform(0.5, 1))
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(0.3, 0.7))

        # Find the results panel
        print("📋 Looking for business results...")

        # Scroll through results to load more businesses
        results_panel_selectors = [
            "div[role='feed']",
            "div.m6QErb",
            "div[aria-label*='Results']",
            "div.m6QErb.DxyBCb.kA9KIf.dS8AEf"
        ]

        results_panel = None
        for selector in results_panel_selectors:
            try:
                results_panel = driver.find_element(By.CSS_SELECTOR, selector)
                if results_panel:
                    print(f"✅ Found results panel using selector: {selector}")
                    break
            except:
                continue

        if not results_panel:
            print("❌ Could not find results panel. Trying alternative approach...")
            return business_data

        # Scroll to load more results
        print("📜 Scrolling to load more results...")
        for i in range(5):  # Scroll multiple times to load more results
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight",
                results_panel
            )
            time.sleep(random.uniform(1, 2))
            print(f"  Scroll {i+1}/5 completed...")

        # Extract business links/data
        print("🔗 Extracting business information...")

        # Find all business result elements
        business_selectors = [
            "a[href*='/maps/place/']",
            "div.Nv2PK a",
            "a.hfpxzc",
            "div[role='article'] a"
        ]

        business_links = []
        for selector in business_selectors:
            try:
                links = driver.find_elements(By.CSS_SELECTOR, selector)
                if links:
                    business_links = links
                    print(f"✅ Found {len(links)} business links using selector: {selector}")
                    break
            except Exception as e:
                print(f"⚠️ Selector {selector} failed: {str(e)[:50]}")
                continue

        # Process each business link
        processed_count = 0
        for i, link in enumerate(business_links):
            if processed_count >= max_results:
                break

            try:
                # Get the business URL
                href = link.get_attribute('href')
                if href and '/maps/place/' in href:
                    business_data.append({
                        'url': href,
                        'index': i
                    })
                    processed_count += 1
            except Exception as e:
                print(f"⚠️ Error processing link {i}: {str(e)[:50]}")
                continue

        print(f"📊 Found {len(business_data)} businesses")

    except Exception as e:
        print(f"❌ Error during search: {str(e)}")

    return business_data

def extract_business_name(driver):
    """Extract business name from Google Maps"""
    try:
        name_selectors = [
            "h1.DUwDvf",
            "h1[class*='fontHeadline']",
            "h1",
            "div.lMbq3e h1"
        ]

        for selector in name_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                name = element.text.strip()
                if name and len(name) > 1:
                    return name
            except:
                continue
        return "N/A"
    except Exception as e:
        print(f"Error extracting name: {e}")
        return "N/A"

def extract_rating(driver):
    """Extract business rating from Google Maps"""
    try:
        rating_selectors = [
            "div.F7nice span[aria-hidden='true']",
            "span.ceNzKf[aria-hidden='true']",
            "div[jsaction*='rating'] span",
            "span[role='img'][aria-label*='stars']"
        ]

        for selector in rating_selectors:
            try:
                rating_element = driver.find_element(By.CSS_SELECTOR, selector)
                rating_text = rating_element.text.strip()
                if rating_text:
                    # Extract number from rating text
                    rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                    if rating_match:
                        return rating_match.group(1)
            except:
                continue

        # Try to extract from aria-label
        try:
            rating_element = driver.find_element(By.CSS_SELECTOR, "span[role='img'][aria-label*='star']")
            aria_label = rating_element.get_attribute('aria-label')
            rating_match = re.search(r'(\d+\.?\d*)', aria_label)
            if rating_match:
                return rating_match.group(1)
        except:
            pass

        return "N/A"
    except Exception as e:
        print(f"Error extracting rating: {e}")
        return "N/A"

def extract_review_count(driver):
    """Extract number of reviews from Google Maps"""
    try:
        review_selectors = [
            "div.F7nice span[aria-label*='reviews']",
            "span.RDApEe",
            "div.F7nice button[aria-label*='reviews']",
            "button[jsaction*='reviews'] span"
        ]

        for selector in review_selectors:
            try:
                review_element = driver.find_element(By.CSS_SELECTOR, selector)
                review_text = review_element.text.strip() or review_element.get_attribute('aria-label')
                if review_text:
                    # Extract number from text like "(3,456)" or "3456 reviews"
                    review_match = re.search(r'[\(\s]([0-9,]+)\s*(?:reviews?|\))', review_text, re.IGNORECASE)
                    if review_match:
                        return review_match.group(1).replace(',', '')
                    # Try simpler extraction
                    simple_match = re.search(r'([0-9,]+)', review_text)
                    if simple_match:
                        return simple_match.group(1).replace(',', '')
            except:
                continue
        return "N/A"
    except Exception as e:
        print(f"Error extracting review count: {e}")
        return "N/A"

def extract_address(driver):
    """Extract business address from Google Maps"""
    try:
        address_selectors = [
            "button[data-item-id='address'] div.fontBodyMedium",
            "button[data-tooltip='Copy address'] div.fontBodyMedium",
            "div.Io6YTe.fontBodyMedium",
            "button[aria-label*='Address'] div",
            "div[data-item-id='address']"
        ]

        for selector in address_selectors:
            try:
                address_element = driver.find_element(By.CSS_SELECTOR, selector)
                address_text = address_element.text.strip()
                if address_text and len(address_text) > 5:
                    # Validate it looks like an address
                    if any(char.isdigit() for char in address_text) or 'serving' in address_text.lower():
                        return address_text
            except:
                continue

        # Alternative approach: look for address patterns in buttons
        try:
            buttons = driver.find_elements(By.CSS_SELECTOR, "button[data-item-id*='address']")
            for button in buttons:
                aria_label = button.get_attribute('aria-label') or ""
                if 'address' in aria_label.lower():
                    text = button.text.strip()
                    if text and len(text) > 5:
                        return text
        except:
            pass

        return "N/A"
    except Exception as e:
        print(f"Error extracting address: {e}")
        return "N/A"

def extract_phone_number(driver):
    """Extract business phone number from Google Maps"""
    try:
        phone_selectors = [
            "button[data-item-id='phone:tel:'] div.fontBodyMedium",
            "button[data-tooltip='Copy phone number'] div.fontBodyMedium",
            "button[aria-label*='Phone'] div",
            "a[href^='tel:']",
            "button[data-item-id*='phone'] div.fontBodyMedium"
        ]

        for selector in phone_selectors:
            try:
                phone_element = driver.find_element(By.CSS_SELECTOR, selector)
                phone_text = phone_element.text.strip() or phone_element.get_attribute('aria-label')
                # Validate it's actually a phone number
                if phone_text and any(char.isdigit() for char in phone_text):
                    # Clean up the phone number
                    phone_match = re.search(r'[\+\d\(\)\-\s\.]+', phone_text)
                    if phone_match and len([c for c in phone_match.group() if c.isdigit()]) >= 10:
                        return phone_match.group().strip()
            except:
                continue

        # Try to extract from href
        try:
            tel_link = driver.find_element(By.CSS_SELECTOR, "a[href^='tel:']")
            href = tel_link.get_attribute('href')
            phone = href.replace('tel:', '').strip()
            if phone:
                return phone
        except:
            pass

        return "N/A"
    except Exception as e:
        print(f"Error extracting phone number: {e}")
        return "N/A"

def extract_website(driver):
    """Extract business website from Google Maps"""
    try:
        website_selectors = [
            "a[data-item-id='authority']",
            "a[data-tooltip='Open website']",
            "a[aria-label*='Website']",
            "button[data-item-id='authority'] a",
            "a[href^='http']:not([href*='google.com'])"
        ]

        # Domains to exclude
        exclude_domains = [
            'google.com', 'maps.google.com', 'goo.gl', 'facebook.com',
            'instagram.com', 'twitter.com', 'linkedin.com', 'youtube.com'
        ]

        for selector in website_selectors:
            try:
                website_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for website_element in website_elements:
                    website_url = website_element.get_attribute('href')
                    if website_url:
                        # Filter out excluded domains
                        is_excluded = any(domain in website_url.lower() for domain in exclude_domains)
                        if not is_excluded and website_url.startswith('http'):
                            return website_url
            except:
                continue

        # Try to find website in aria-label
        try:
            buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-label*='website'], a[aria-label*='website']")
            for button in buttons:
                href = button.get_attribute('href')
                if href and href.startswith('http'):
                    is_excluded = any(domain in href.lower() for domain in exclude_domains)
                    if not is_excluded:
                        return href
        except:
            pass

        return "N/A"
    except Exception as e:
        print(f"Error extracting website: {e}")
        return "N/A"

def extract_business_hours(driver):
    """Extract business hours from Google Maps"""
    try:
        # Try to click on hours section to expand it
        try:
            hours_button_selectors = [
                "button[data-item-id='oh']",
                "button[aria-label*='Hours']",
                "div.t39EBf.GUrTGd button"
            ]

            for selector in hours_button_selectors:
                try:
                    hours_button = driver.find_element(By.CSS_SELECTOR, selector)
                    # Check if we need to click to expand
                    aria_expanded = hours_button.get_attribute('aria-expanded')
                    if aria_expanded == 'false':
                        driver.execute_script("arguments[0].click();", hours_button)
                        time.sleep(random.uniform(0.5, 1))
                        break
                except:
                    continue
        except:
            pass

        # Extract hours
        hours_selectors = [
            "table.eK4R0e tr",
            "div[aria-label*='Hours'] table tr",
            "table tbody tr"
        ]

        hours_data = []
        for selector in hours_selectors:
            try:
                hour_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if hour_elements:
                    for element in hour_elements:
                        hours_text = element.text.strip()
                        if hours_text and len(hours_text) > 3:
                            # Clean up the text
                            cleaned_text = re.sub(r'\s+', ' ', hours_text)
                            if any(day in cleaned_text.lower() for day in
                                 ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']):
                                hours_data.append(cleaned_text)
                    if hours_data:
                        return "; ".join(hours_data)
            except:
                continue

        # Try to get current status (Open/Closed)
        try:
            status_selectors = [
                "span.ZDu9vd span",
                "div.OqCZI.fontBodyMedium span"
            ]

            for selector in status_selectors:
                try:
                    status_element = driver.find_element(By.CSS_SELECTOR, selector)
                    status_text = status_element.text.strip()
                    if status_text and ('open' in status_text.lower() or 'closed' in status_text.lower()):
                        return status_text
                except:
                    continue
        except:
            pass

        return "N/A"
    except Exception as e:
        print(f"Error extracting business hours: {e}")
        return "N/A"

def extract_category(driver):
    """Extract business category from Google Maps"""
    try:
        category_selectors = [
            "button[jsaction*='category'] div.fontBodyMedium",
            "button.DkEaL",
            "div.LBgpqf div.fontBodyMedium"
        ]

        for selector in category_selectors:
            try:
                category_element = driver.find_element(By.CSS_SELECTOR, selector)
                category_text = category_element.text.strip()
                if category_text and len(category_text) > 2:
                    return category_text
            except:
                continue
        return "N/A"
    except Exception as e:
        print(f"Error extracting category: {e}")
        return "N/A"

def scrape_business_info(driver, business_url, search_category, search_location):
    """Main function to scrape all business information from Google Maps"""
    try:
        print(f"\n🎯 Scraping: {business_url}")

        # Add random delay before visiting business page
        delay = random.uniform(1, 2)
        print(f"⏰ Waiting {delay:.1f} seconds before visiting business page...")
        time.sleep(delay)

        driver.get(business_url)

        # Wait for page to load
        time.sleep(random.uniform(2, 4))

        # Simulate human reading behavior
        print("👁️ Simulating human reading behavior on business page...")
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(random.uniform(0.5, 1))
        driver.execute_script("window.scrollTo(0, 600);")
        time.sleep(random.uniform(0.5, 1))
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(0.3, 0.7))

        # Extract all information
        print("📊 Extracting business data...")

        business_name = extract_business_name(driver)
        print(f"  📌 Name: {business_name}")
        time.sleep(random.uniform(0.2, 0.5))

        rating = extract_rating(driver)
        print(f"  ⭐ Rating: {rating}")
        time.sleep(random.uniform(0.2, 0.5))

        review_count = extract_review_count(driver)
        print(f"  💬 Reviews: {review_count}")
        time.sleep(random.uniform(0.2, 0.5))

        address = extract_address(driver)
        print(f"  📍 Address: {address}")
        time.sleep(random.uniform(0.2, 0.5))

        phone = extract_phone_number(driver)
        print(f"  📞 Phone: {phone}")
        time.sleep(random.uniform(0.2, 0.5))

        website = extract_website(driver)
        print(f"  🌐 Website: {website}")
        time.sleep(random.uniform(0.2, 0.5))

        category = extract_category(driver)
        print(f"  🏷️ Category: {category}")
        time.sleep(random.uniform(0.2, 0.5))

        business_hours = extract_business_hours(driver)
        print(f"  🕒 Hours: {business_hours[:50]}..." if len(business_hours) > 50 else f"  🕒 Hours: {business_hours}")

        # Final scroll simulation
        print("👁️ Final page review simulation...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(random.uniform(0.5, 1))
        driver.execute_script("window.scrollTo(0, 0);")

        business_info = {
            'business_name': business_name,
            'rating': rating,
            'review_count': review_count,
            'address': address if address != "N/A" else search_location,
            'phone': phone,
            'website': website,
            'categories': category if category != "N/A" else search_category,
            'business_hours': business_hours,
            'google_maps_url': business_url
        }

        print(f"✅ Successfully scraped: {business_name}")
        return business_info

    except Exception as e:
        print(f"❌ Error scraping {business_url}: {str(e)}")
        return {
            'business_name': 'N/A',
            'rating': 'N/A',
            'review_count': 'N/A',
            'address': search_location,
            'phone': 'N/A',
            'website': 'N/A',
            'categories': search_category,
            'business_hours': 'N/A',
            'google_maps_url': business_url
        }

def scrape_multiple_locations(driver, category, locations, max_results_per_location=20):
    """Scrape businesses across multiple states/cities"""
    all_businesses = []

    print(f"\n{'='*70}")
    print(f"SCRAPING {len(locations)} LOCATIONS")
    print(f"{'='*70}")

    for idx, location in enumerate(locations, 1):
        print(f"\n[{idx}/{len(locations)}] Processing location: {location}")
        print(f"{'='*70}")

        # Search for businesses in this location
        businesses = search_google_maps_businesses(driver, category, location, max_results_per_location)

        if not businesses:
            print(f"⚠️ No businesses found in {location}")
            continue

        print(f"✅ Found {len(businesses)} businesses in {location}")

        # Scrape each business
        for i, business in enumerate(businesses, 1):
            print(f"\n  [{i}/{len(businesses)}] Processing business in {location}...")
            business_info = scrape_business_info(driver, business['url'], category, location)
            all_businesses.append(business_info)

            # Add delay between businesses
            if i < len(businesses):
                delay = random.uniform(2, 4)
                print(f"  😴 Stealth delay: {delay:.1f} seconds...")
                time.sleep(delay)

        # Longer delay between locations
        if idx < len(locations):
            delay = random.uniform(5, 8)
            print(f"\n☕ Location break: {delay:.1f} seconds before next location...")
            time.sleep(delay)

    return all_businesses

def main():
    """Main function to run the scraper"""
    print("="*70)
    print("        GOOGLE BUSINESS PROFILE SCRAPER")
    print("="*70)
    print("This tool will search Google Maps for businesses and extract their information")
    print("You can search across multiple states/cities!")
    print()

    # Get user input
    category = input("Enter business category (e.g., 'restaurants', 'dentist', 'plumber'): ").strip()
    if not category:
        print("Error: Business category is required!")
        return

    # Get locations - support multiple
    print("\nEnter locations to search (one per line).")
    print("Examples: 'New York, NY', 'Los Angeles, CA', 'Chicago, IL'")
    print("Type 'done' when finished:")

    locations = []
    while True:
        location = input(f"Location {len(locations)+1} (or 'done'): ").strip()
        if location.lower() == 'done':
            break
        if location:
            locations.append(location)

    if not locations:
        print("Error: At least one location is required!")
        return

    # Get number of results per location
    try:
        max_results = input(f"Max results per location? (default: 20, max: 50): ").strip()
        max_results = int(max_results) if max_results else 20
        max_results = min(max_results, 50)
    except ValueError:
        max_results = 20

    # Generate output filename
    safe_category = re.sub(r'[^\w\s-]', '', category).strip().replace(' ', '_')
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = f"google_{safe_category}_{timestamp}.csv"

    print(f"\n{'='*70}")
    print(f"SCRAPING CONFIGURATION")
    print(f"{'='*70}")
    print(f"📂 Category: {category}")
    print(f"📍 Locations: {len(locations)}")
    for i, loc in enumerate(locations, 1):
        print(f"   {i}. {loc}")
    print(f"📊 Max results per location: {max_results}")
    print(f"💾 Output file: {output_file}")
    print(f"{'='*70}")

    confirm = input("\nProceed with scraping? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("Scraping cancelled.")
        return

    driver = get_driver()

    try:
        # Establish session
        establish_session(driver)

        # Scrape businesses across all locations
        all_businesses = scrape_multiple_locations(driver, category, locations, max_results)

        if not all_businesses:
            print("\n❌ No businesses found for the given search criteria.")
            return

        # Save to CSV
        print(f"\n{'='*70}")
        print("SAVING RESULTS")
        print(f"{'='*70}")

        fieldnames = [
            'business_name', 'rating', 'review_count', 'address',
            'phone', 'website', 'categories',
            'business_hours', 'google_maps_url'
        ]

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_businesses)

        print(f"\n{'='*70}")
        print(f"SCRAPING COMPLETE!")
        print(f"{'='*70}")
        print(f"✅ Successfully scraped {len(all_businesses)} businesses")
        print(f"📁 Data saved to: {output_file}")
        print(f"🔍 Category: {category}")
        print(f"📍 Locations: {', '.join(locations)}")
        print(f"{'='*70}")

    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔒 Closing browser...")
        driver.quit()
        print("✅ Browser closed. Session ended.")

if __name__ == "__main__":
    # Check and install required packages
    try:
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
        print("Installing required packages...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "webdriver-manager"])
        # Import again after installation
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager

    main()
