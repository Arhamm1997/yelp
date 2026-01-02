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
    chrome_options.add_argument("--start-maximized")

    # Randomize user agent from a pool of recent Chrome versions
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    ]

    selected_ua = random.choice(user_agents)
    chrome_options.add_argument(f"user-agent={selected_ua}")

    # Additional stealth measures
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Add some realistic browser preferences
    prefs = {
        "profile.default_content_setting_values": {
            "notifications": 2,
            "geolocation": 1,
        },
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    # Enhanced stealth JavaScript execution
    stealth_js = """
    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
    Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
    """

    driver.execute_script(stealth_js)
    driver.execute_script("window.scrollTo(0, 100);")
    time.sleep(random.uniform(0.5, 1.5))

    return driver

def establish_session(driver):
    """Establish a verified session with Google Maps before starting scraping"""
    print("🔐 Establishing verified session with Google Maps...")

    print("🏠 Visiting Google Maps homepage...")
    driver.get("https://www.google.com/maps")
    time.sleep(random.uniform(3, 5))

    page_source = driver.page_source.lower()
    bot_indicators = [
        'verify', 'captcha', 'robot', 'security check', 'unusual traffic',
        'blocked', 'suspicious', 'automation', 'bot'
    ]

    if any(indicator in page_source for indicator in bot_indicators):
        print("\n" + "="*70)
        print("🚨 GOOGLE VERIFICATION REQUIRED!")
        print("="*70)
        print("❌ Google requires verification before we can start scraping.")
        print("")
        print("📋 MANUAL STEPS REQUIRED:")
        print("1. ✅ Complete any verification (CAPTCHA, etc.) in the browser")
        print("2. ✅ Browse normally for 30-60 seconds")
        print("3. ✅ Press ENTER here when ready to continue...")
        print("="*70)

        input("🔑 Press ENTER after completing verification: ")
        print("✅ Session verification completed! Starting scraping...")
        time.sleep(2)
    else:
        print("✅ No initial verification required. Session established!")

    # Simulate human browsing
    print("👁️ Simulating natural browsing behavior...")
    driver.execute_script("window.scrollTo(0, 300);")
    time.sleep(random.uniform(1, 2))
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(random.uniform(1, 2))

def search_google_maps_businesses(driver, category, location, max_results=20):
    """Search Google Maps for businesses and return their URLs"""
    business_urls = []

    try:
        search_query = f"{category} in {location}"
        search_url = f"https://www.google.com/maps/search/{urllib.parse.quote(search_query)}"

        print(f"\n🔍 Searching: {search_query}")
        driver.get(search_url)
        time.sleep(random.uniform(4, 6))

        # Wait for results to load
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
            )
        except:
            print("⚠️ Results panel took longer to load, continuing anyway...")

        # Find the scrollable results panel
        print("📋 Finding results panel...")
        time.sleep(2)

        # Scroll to load more results
        print("📜 Scrolling to load more results...")
        last_height = 0
        scroll_attempts = 0
        max_scroll_attempts = 10

        while scroll_attempts < max_scroll_attempts:
            # Find results container
            try:
                results_panel = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")

                # Scroll within the panel
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_panel)
                time.sleep(random.uniform(2, 3))

                # Check if we've reached the end
                new_height = driver.execute_script("return arguments[0].scrollHeight", results_panel)
                if new_height == last_height:
                    scroll_attempts += 1
                else:
                    scroll_attempts = 0

                last_height = new_height
                print(f"  Scroll progress... (attempt {scroll_attempts + 1})")

                # Check if we have enough results
                links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/maps/place/']")
                if len(links) >= max_results:
                    print(f"  ✅ Loaded {len(links)} results, enough for our needs")
                    break

            except Exception as e:
                print(f"  ⚠️ Scroll error: {str(e)[:50]}")
                break

        # Extract business URLs
        print("🔗 Extracting business URLs...")
        links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/maps/place/']")

        seen_urls = set()
        for link in links:
            if len(business_urls) >= max_results:
                break

            try:
                href = link.get_attribute('href')
                if href and '/maps/place/' in href:
                    # Clean URL
                    clean_url = href.split('?')[0] if '?' in href else href

                    if clean_url not in seen_urls:
                        seen_urls.add(clean_url)
                        business_urls.append(clean_url)
            except:
                continue

        print(f"✅ Found {len(business_urls)} unique business URLs")

    except Exception as e:
        print(f"❌ Error during search: {str(e)}")

    return business_urls

def extract_business_name(driver):
    """Extract business name"""
    try:
        selectors = [
            "h1.DUwDvf",
            "h1.fontHeadlineLarge",
            "h1",
        ]

        for selector in selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                name = element.text.strip()
                if name and len(name) > 1:
                    return name
            except:
                continue
        return "N/A"
    except:
        return "N/A"

def extract_rating(driver):
    """Extract rating"""
    try:
        # Try to find rating element
        selectors = [
            "div.F7nice span[aria-hidden='true']",
            "span.ceNzKf",
            "div.fontBodyMedium span[role='img']",
        ]

        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    # Check if it's a rating (number between 1-5)
                    if text and re.match(r'^[1-5]\.\d$', text):
                        return text
            except:
                continue

        return "N/A"
    except:
        return "N/A"

def extract_review_count(driver):
    """Extract review count"""
    try:
        selectors = [
            "div.F7nice button span",
            "button[aria-label*='reviews']",
        ]

        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    # Look for numbers in parentheses or with commas
                    match = re.search(r'[\(\s]([0-9,]+)\s*\)?', text)
                    if match:
                        return match.group(1).replace(',', '')
            except:
                continue

        return "N/A"
    except:
        return "N/A"

def extract_address(driver):
    """Extract address"""
    try:
        selectors = [
            "button[data-item-id='address'] div.fontBodyMedium",
            "button[data-tooltip='Copy address']",
            "div.Io6YTe",
        ]

        for selector in selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                address = element.text.strip()
                if address and len(address) > 5:
                    return address
            except:
                continue

        return "N/A"
    except:
        return "N/A"

def extract_phone_number(driver):
    """Extract phone number"""
    try:
        # Look for phone button
        selectors = [
            "button[data-tooltip='Copy phone number']",
            "button[data-item-id*='phone']",
            "a[href^='tel:']",
        ]

        for selector in selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                phone = element.text.strip()

                # Also try aria-label
                if not phone:
                    phone = element.get_attribute('aria-label') or ""

                # Validate phone number
                if phone and re.search(r'\d{3}[-.)]\s?\d{3}[-.)]\s?\d{4}', phone):
                    return phone
            except:
                continue

        # Try to find tel: link
        try:
            tel_link = driver.find_element(By.CSS_SELECTOR, "a[href^='tel:']")
            href = tel_link.get_attribute('href')
            if href:
                phone = href.replace('tel:', '').strip()
                return phone
        except:
            pass

        return "N/A"
    except:
        return "N/A"

def extract_website(driver):
    """Extract website URL"""
    try:
        selectors = [
            "a[data-item-id='authority']",
            "a[data-tooltip='Open website']",
        ]

        exclude_domains = [
            'google.com', 'maps.google', 'facebook.com',
            'instagram.com', 'twitter.com', 'youtube.com'
        ]

        for selector in selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                url = element.get_attribute('href')

                if url and url.startswith('http'):
                    # Check if it's not a social media or google link
                    if not any(domain in url.lower() for domain in exclude_domains):
                        return url
            except:
                continue

        return "N/A"
    except:
        return "N/A"

def extract_email(driver):
    """Extract email address if available"""
    try:
        # Email patterns to search for
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        # Check About section
        try:
            # Click on About tab if available
            about_buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-label*='About']")
            for button in about_buttons:
                try:
                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(1)
                    break
                except:
                    continue
        except:
            pass

        # Search in page source for email
        page_text = driver.page_source
        emails = re.findall(email_pattern, page_text)

        # Filter out common non-business emails
        exclude_patterns = [
            'google.com', 'example.com', 'test.com',
            'support@', 'noreply@', 'info@google'
        ]

        for email in emails:
            if not any(pattern in email.lower() for pattern in exclude_patterns):
                return email

        # Try to find in website if available
        try:
            website_link = driver.find_element(By.CSS_SELECTOR, "a[data-item-id='authority']")
            website_link.click()
            time.sleep(2)

            # Switch to new tab
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)

                # Look for contact or about page
                page_text = driver.page_source
                emails = re.findall(email_pattern, page_text)

                for email in emails:
                    if not any(pattern in email.lower() for pattern in exclude_patterns):
                        # Close tab and switch back
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        return email

                # Close tab and switch back
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        except:
            pass

        return "N/A"
    except:
        return "N/A"

def extract_years_in_business(driver):
    """Extract years in business / experience"""
    try:
        # Patterns to look for
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:in business|of experience|established)',
            r'(?:established|since|founded)\s*(?:in\s*)?(\d{4})',
            r'(\d+)\s*years?\s*serving',
        ]

        # Get page text
        page_text = driver.page_source.lower()

        for pattern in patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                # If it's a year (like 2010), calculate years
                if matches[0].isdigit() and len(matches[0]) == 4:
                    year = int(matches[0])
                    current_year = 2026
                    years = current_year - year
                    return f"{years} years (since {year})"
                else:
                    return f"{matches[0]} years"

        # Try to find in About section
        try:
            # Scroll down to find more info
            driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(1)

            # Look for business description or highlights
            desc_elements = driver.find_elements(By.CSS_SELECTOR, "div.fontBodyMedium, div.WeS02d")
            for element in desc_elements:
                text = element.text.lower()
                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    if matches:
                        if matches[0].isdigit() and len(matches[0]) == 4:
                            year = int(matches[0])
                            current_year = 2026
                            years = current_year - year
                            return f"{years} years (since {year})"
                        else:
                            return f"{matches[0]} years"
        except:
            pass

        return "N/A"
    except:
        return "N/A"

def extract_category(driver):
    """Extract business category"""
    try:
        selectors = [
            "button.DkEaL",
            "button[jsaction*='category']",
        ]

        for selector in selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                category = element.text.strip()
                if category and len(category) > 2:
                    return category
            except:
                continue
        return "N/A"
    except:
        return "N/A"

def extract_business_hours(driver):
    """Extract business hours"""
    try:
        # Try to expand hours if collapsed
        try:
            hours_buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-label*='hours' i]")
            for button in hours_buttons:
                try:
                    aria_expanded = button.get_attribute('aria-expanded')
                    if aria_expanded == 'false':
                        driver.execute_script("arguments[0].click();", button)
                        time.sleep(1)
                        break
                except:
                    continue
        except:
            pass

        # Extract hours from table
        hours_data = []
        try:
            rows = driver.find_elements(By.CSS_SELECTOR, "table.eK4R0e tr, div[aria-label*='Hours'] table tr")
            for row in rows:
                text = row.text.strip()
                if text and any(day in text for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
                    hours_data.append(text.replace('\n', ' '))
        except:
            pass

        if hours_data:
            return "; ".join(hours_data)

        # Try to get current open/closed status
        try:
            status_elements = driver.find_elements(By.CSS_SELECTOR, "span.ZDu9vd span, div[class*='open']")
            for element in status_elements:
                text = element.text.strip()
                if text and ('open' in text.lower() or 'closed' in text.lower() or 'closes' in text.lower()):
                    return text
        except:
            pass

        return "N/A"
    except:
        return "N/A"

def scrape_business_info(driver, business_url, search_category, search_location):
    """Scrape all information from a single business"""
    try:
        print(f"\n🎯 Opening business page...")

        # Navigate to business page
        driver.get(business_url)
        time.sleep(random.uniform(3, 5))

        # Wait for page to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
            )
        except:
            print("⚠️ Page load timeout, continuing anyway...")

        # Additional wait for dynamic content
        time.sleep(2)

        # Simulate human behavior - scroll
        print("👁️ Simulating reading behavior...")
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(random.uniform(0.5, 1))
        driver.execute_script("window.scrollTo(0, 600);")
        time.sleep(random.uniform(0.5, 1))
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(0.5, 1))

        # Extract all data
        print("📊 Extracting business data...")

        business_name = extract_business_name(driver)
        print(f"  📌 Name: {business_name}")

        rating = extract_rating(driver)
        print(f"  ⭐ Rating: {rating}")

        review_count = extract_review_count(driver)
        print(f"  💬 Reviews: {review_count}")

        address = extract_address(driver)
        print(f"  📍 Address: {address}")

        phone = extract_phone_number(driver)
        print(f"  📞 Phone: {phone}")

        website = extract_website(driver)
        print(f"  🌐 Website: {website}")

        category = extract_category(driver)
        print(f"  🏷️ Category: {category}")

        print("  📧 Extracting email (this may take a moment)...")
        email = extract_email(driver)
        print(f"  📧 Email: {email}")

        print("  📅 Checking years in business...")
        years_experience = extract_years_in_business(driver)
        print(f"  📅 Experience: {years_experience}")

        business_hours = extract_business_hours(driver)
        hours_preview = business_hours[:50] + "..." if len(business_hours) > 50 else business_hours
        print(f"  🕒 Hours: {hours_preview}")

        business_info = {
            'business_name': business_name,
            'rating': rating,
            'review_count': review_count,
            'address': address if address != "N/A" else search_location,
            'phone': phone,
            'email': email,
            'website': website,
            'categories': category if category != "N/A" else search_category,
            'years_in_business': years_experience,
            'business_hours': business_hours,
            'google_maps_url': business_url
        }

        print(f"✅ Successfully scraped: {business_name}")
        return business_info

    except Exception as e:
        print(f"❌ Error scraping business: {str(e)}")
        return {
            'business_name': 'N/A',
            'rating': 'N/A',
            'review_count': 'N/A',
            'address': search_location,
            'phone': 'N/A',
            'email': 'N/A',
            'website': 'N/A',
            'categories': search_category,
            'years_in_business': 'N/A',
            'business_hours': 'N/A',
            'google_maps_url': business_url
        }

def scrape_multiple_locations(driver, category, locations, max_results_per_location=20):
    """Scrape businesses across multiple locations"""
    all_businesses = []

    print(f"\n{'='*70}")
    print(f"SCRAPING {len(locations)} LOCATION(S)")
    print(f"{'='*70}")

    for idx, location in enumerate(locations, 1):
        print(f"\n[{idx}/{len(locations)}] Processing location: {location}")
        print(f"{'='*70}")

        # Search for businesses
        business_urls = search_google_maps_businesses(driver, category, location, max_results_per_location)

        if not business_urls:
            print(f"⚠️ No businesses found in {location}")
            continue

        print(f"✅ Found {len(business_urls)} businesses in {location}")
        print(f"Starting detailed scraping...")

        # Scrape each business
        for i, url in enumerate(business_urls, 1):
            print(f"\n  [{i}/{len(business_urls)}] Business {i} in {location}")
            print(f"  {'-'*66}")

            business_info = scrape_business_info(driver, url, category, location)
            all_businesses.append(business_info)

            # Delay between businesses
            if i < len(business_urls):
                delay = random.uniform(2, 4)
                print(f"\n  😴 Delay: {delay:.1f}s before next business...")
                time.sleep(delay)

        # Longer delay between locations
        if idx < len(locations):
            delay = random.uniform(5, 8)
            print(f"\n☕ Location break: {delay:.1f}s before next location...")
            time.sleep(delay)

    return all_businesses

def main():
    """Main function"""
    print("="*70)
    print("     GOOGLE BUSINESS PROFILE SCRAPER v2.0")
    print("     With Email & Years of Experience Extraction")
    print("="*70)
    print()

    # Get category
    category = input("Enter business category (e.g., 'restaurants', 'dentist'): ").strip()
    if not category:
        print("❌ Error: Category is required!")
        return

    # Get locations
    print("\nEnter locations to search (one per line).")
    print("Examples: 'New York, NY', 'Los Angeles, CA'")
    print("Type 'done' when finished:\n")

    locations = []
    while True:
        location = input(f"Location {len(locations)+1} (or 'done'): ").strip()
        if location.lower() == 'done':
            break
        if location:
            locations.append(location)

    if not locations:
        print("❌ Error: At least one location is required!")
        return

    # Get max results
    try:
        max_results = input(f"\nMax results per location (default: 20): ").strip()
        max_results = int(max_results) if max_results else 20
        max_results = min(max_results, 100)
    except ValueError:
        max_results = 20

    # Generate filename
    safe_category = re.sub(r'[^\w\s-]', '', category).strip().replace(' ', '_')
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = f"google_{safe_category}_{timestamp}.csv"

    print(f"\n{'='*70}")
    print(f"CONFIGURATION")
    print(f"{'='*70}")
    print(f"📂 Category: {category}")
    print(f"📍 Locations: {len(locations)}")
    for i, loc in enumerate(locations, 1):
        print(f"   {i}. {loc}")
    print(f"📊 Max per location: {max_results}")
    print(f"💾 Output: {output_file}")
    print(f"{'='*70}")

    confirm = input("\nStart scraping? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("Cancelled.")
        return

    driver = get_driver()

    try:
        # Establish session
        establish_session(driver)

        # Scrape all locations
        all_businesses = scrape_multiple_locations(driver, category, locations, max_results)

        if not all_businesses:
            print("\n❌ No businesses found.")
            return

        # Save to CSV
        print(f"\n{'='*70}")
        print("SAVING RESULTS")
        print(f"{'='*70}")

        fieldnames = [
            'business_name', 'rating', 'review_count', 'address',
            'phone', 'email', 'website', 'categories', 'years_in_business',
            'business_hours', 'google_maps_url'
        ]

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_businesses)

        print(f"\n{'='*70}")
        print(f"✅ SCRAPING COMPLETE!")
        print(f"{'='*70}")
        print(f"📊 Total businesses: {len(all_businesses)}")
        print(f"💾 Saved to: {output_file}")
        print(f"📧 Email addresses found: {sum(1 for b in all_businesses if b['email'] != 'N/A')}")
        print(f"📅 Years in business found: {sum(1 for b in all_businesses if b['years_in_business'] != 'N/A')}")
        print(f"{'='*70}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔒 Closing browser...")
        driver.quit()

if __name__ == "__main__":
    try:
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
        print("Installing required packages...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "webdriver-manager"])
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager

    main()
