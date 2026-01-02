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
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    """Initialize Chrome WebDriver with enhanced anti-detection settings"""
    chrome_options = Options()
    
    # Enhanced anti-detection measures

    # chrome_options.add_argument("--headless")  
    
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
    
    import random
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
            "geolocation": 2,
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
    """Establish a verified session with Yelp before starting scraping"""
    print("🔐 Establishing verified session with Yelp...")
    
    # Visit Yelp homepage first
    print("🏠 Visiting Yelp homepage...")
    driver.get("https://www.yelp.com")
    time.sleep(random.uniform(3, 5))
    
    # Check for initial bot detection
    page_source = driver.page_source.lower()
    bot_indicators = [
        'verify', 'captcha', 'robot', 'security check', 'unusual traffic',
        'blocked', 'suspicious', 'automation', 'bot', 'verify you are human',
        'prove you are not a robot', 'please verify', 'access denied',
        'rate limit', 'too many requests', 'temporarily blocked'
    ]
    
    if any(indicator in page_source for indicator in bot_indicators):
        print("\n" + "="*70)
        print("🚨 INITIAL YELP VERIFICATION REQUIRED!")
        print("="*70)
        print("❌ Yelp requires verification before we can start scraping.")
        print("🔧 This is a one-time setup step.")
        print("")
        print("📋 MANUAL STEPS REQUIRED:")
        print("1. ✅ Complete any verification (CAPTCHA, etc.) in the browser")
        print("2. ✅ Browse normally for 30-60 seconds (scroll, click around)")
        print("3. ✅ Close any popup windows or notifications")
        print("4. ✅ Navigate to any Yelp search page to confirm access")
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
    
def search_yelp_businesses(driver, category, location, max_pages=3):
    """Search Yelp for businesses based on category and location (assumes session is already established)"""
    business_urls = []
    
    try:
        # Construct search URL
        encoded_category = urllib.parse.quote_plus(category)
        encoded_location = urllib.parse.quote_plus(location)
        
        for page in range(max_pages):
            start = page * 10  # Yelp shows 10 results per page
            search_url = f"https://www.yelp.com/search?find_desc={encoded_category}&find_loc={encoded_location}&start={start}"
            
            print(f"🔍 Searching page {page + 1}: {search_url}")
            
            # Add random delay before each page
            if page > 0:
                delay = random.uniform(2, 4)  # Reduced delay as requested
                print(f"⏰ Waiting {delay:.1f} seconds before next page...")
                time.sleep(delay)
            
            driver.get(search_url)
            
            # Extended wait for page to load
            time.sleep(random.uniform(2, 4))  # Reduced delay as requested
            
            # Simulate human reading behavior
            print("👁️ Simulating human reading behavior...")
            driver.execute_script("window.scrollTo(0, 200);")
            time.sleep(random.uniform(0.5, 1))  # Reduced delay
            driver.execute_script("window.scrollTo(0, 400);")
            time.sleep(random.uniform(0.5, 1))  # Reduced delay
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(random.uniform(0.3, 0.7))  # Reduced delay
            
            # NO bot detection check here - session already established!
            
            # Try multiple selectors for business links with more patience
            business_links = []
            selectors = [
                "a[href*='/biz/']",
                "a[data-analytics-label='biz-name']", 
                "h3 a[href*='/biz/']",
                ".businessName a",
                "a[href*='/biz/'][data-testid]",
                "div[data-testid*='serp'] a[href*='/biz/']"
            ]
            
            print("🔗 Looking for business links...")
            for selector in selectors:
                try:
                    # Wait a bit before trying each selector
                    time.sleep(random.uniform(0.5, 1))
                    links = driver.find_elements(By.CSS_SELECTOR, selector)
                    if links:
                        business_links = links
                        print(f"✅ Found {len(links)} links using selector: {selector}")
                        break
                except Exception as e:
                    print(f"⚠️ Selector {selector} failed: {str(e)[:50]}")
                    continue
            
            if not business_links:
                print("🔍 No links found with standard selectors, trying alternative approach...")
                # Try to find any links that look like business pages
                try:
                    all_links = driver.find_elements(By.TAG_NAME, "a")
                    for link in all_links:
                        href = link.get_attribute('href')
                        if href and '/biz/' in href and 'yelp.com/biz/' in href:
                            business_links.append(link)
                    print(f"🔍 Found {len(business_links)} links using fallback method")
                except:
                    pass
            
            page_urls = []
            for link in business_links:
                try:
                    href = link.get_attribute('href')
                    if href and '/biz/' in href:
                        # Clean the URL to remove query parameters
                        clean_url = href.split('?')[0]
                        if clean_url not in business_urls:
                            business_urls.append(clean_url)
                            page_urls.append(clean_url)
                except:
                    continue
            
            print(f"📊 Found {len(page_urls)} new businesses on page {page + 1}")
            
            # Enhanced debugging for empty results
            if len(page_urls) == 0:
                print("⚠️ No businesses found on this page. Analyzing page content...")
                try:
                    page_title = driver.title
                    print(f"📄 Page title: {page_title}")
                    
                    # Check if we're actually on a search results page
                    if "search" not in page_title.lower() and "results" not in page_title.lower():
                        print("❌ Not on a search results page. May have been redirected.")
                        
                        # Try to navigate back to search
                        driver.get(search_url)
                        time.sleep(random.uniform(3, 5))
                        continue
                    
                    page_source = driver.page_source
                    if any(phrase in page_source.lower() for phrase in ["no businesses found", "0 results", "no results"]):
                        print("📭 Yelp returned no results for this search.")
                        break
                    else:
                        print("🤔 Page loaded but no business links detected. Continuing to next page...")
                        
                except Exception as e:
                    print(f"⚠️ Error analyzing page: {str(e)}")
            
            # More human-like behavior between pages
            if page < max_pages - 1 and page_urls:
                # Scroll around the current page like a human would
                print("👁️ Simulating human browsing behavior...")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(random.uniform(1, 2))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(1, 2))
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(random.uniform(0.5, 1))
    
    except Exception as e:
        print(f"❌ Error during search: {str(e)}")
    
    print(f"\n📈 Total businesses found: {len(business_urls)}")
    return business_urls

def extract_rating(driver):
    """Extract business rating"""
    try:
        rating_selectors = [
            "div[data-testid='rating'] span.y-css-qn4gww",
            ".y-css-qn4gww[aria-label*='star rating']",
            "span[aria-label*='star rating']",
            "div[role='img'][aria-label*='star rating']"
        ]
        
        for selector in rating_selectors:
            try:
                rating_element = driver.find_element(By.CSS_SELECTOR, selector)
                rating_text = rating_element.get_attribute('aria-label') or rating_element.text
                if rating_text:
                    # Extract number from rating text
                    rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                    if rating_match:
                        return rating_match.group(1)
            except:
                continue
        return "N/A"
    except Exception as e:
        print(f"Error extracting rating: {e}")
        return "N/A"

def extract_review_count(driver):
    """Extract number of reviews"""
    try:
        # First try the specific selector you mentioned
        try:
            review_count_element = driver.find_element(By.CSS_SELECTOR, "div[data-testid='BizHeaderReviewCount'] span a[href='#reviews']")
            review_text = review_count_element.text.strip()
            if review_text:
                # Extract number from text like "(3k reviews)" or "(1,234 reviews)"
                review_match = re.search(r'\(([0-9,k]+)\s*reviews?\)', review_text, re.IGNORECASE)
                if review_match:
                    count_str = review_match.group(1)
                    # Handle 'k' notation (e.g., "3k" = "3000")
                    if 'k' in count_str.lower():
                        return count_str.replace('k', '000').replace('K', '000')
                    else:
                        return count_str.replace(',', '')
        except:
            pass
        
        # Alternative selectors for the review count section
        review_selectors = [
            # Specific BizHeaderReviewCount area
            "div[data-testid='BizHeaderReviewCount'] a[href='#reviews']",
            "div[data-testid='BizHeaderReviewCount'] a",
            # Look for review links with parentheses
            "a[href='#reviews']",
            "a[href*='reviews']",
            # Look in the review count specific area
            "span.y-css-1q46f5r a[href='#reviews']",
            "span.y-css-1q46f5r a"
        ]
        
        for selector in review_selectors:
            try:
                review_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for review_element in review_elements:
                    review_text = review_element.text.strip()
                    if review_text and ('review' in review_text.lower() or '(' in review_text):
                        # Look for patterns like "(3k reviews)" or "(1,234 reviews)"
                        review_match = re.search(r'\(([0-9,k]+)\s*reviews?\)', review_text, re.IGNORECASE)
                        if review_match:
                            count_str = review_match.group(1)
                            # Handle 'k' notation
                            if 'k' in count_str.lower():
                                return count_str.replace('k', '000').replace('K', '000')
                            else:
                                return count_str.replace(',', '')
                        
                        # Also try to extract just numbers with 'k'
                        simple_match = re.search(r'(\d+\.?\d*k)', review_text, re.IGNORECASE)
                        if simple_match:
                            count_str = simple_match.group(1)
                            return count_str.replace('k', '000').replace('K', '000')
                        
                        # Try to extract comma-separated numbers
                        number_match = re.search(r'(\d+(?:,\d+)+)', review_text)
                        if number_match:
                            return number_match.group(1).replace(',', '')
            except:
                continue
        
        # Fallback: search page source for review count patterns
        try:
            page_source = driver.page_source
            # Look for the specific data-testid pattern
            testid_pattern = re.search(r'data-testid="BizHeaderReviewCount"[^>]*>.*?\(([0-9,k]+)\s*reviews?\)', page_source, re.IGNORECASE | re.DOTALL)
            if testid_pattern:
                count_str = testid_pattern.group(1)
                if 'k' in count_str.lower():
                    return count_str.replace('k', '000').replace('K', '000')
                else:
                    return count_str.replace(',', '')
            
            # Other fallback patterns
            review_patterns = [
                r'\(([0-9,k]+)\s*reviews?\)',
                r'(\d+\.?\d*k)\s*reviews?',
                r'(\d+(?:,\d+)+)\s*reviews?'
            ]
            
            for pattern in review_patterns:
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                if matches:
                    for match in matches:
                        if 'k' in match.lower():
                            return match.replace('k', '000').replace('K', '000')
                        elif ',' in match:
                            return match.replace(',', '')
                        elif match.isdigit():
                            return match
        except:
            pass
            
        return "N/A"
    except Exception as e:
        print(f"Error extracting review count: {e}")
        return "N/A"

def extract_address(driver):
    """Extract business address with enhanced selectors and promotional content filtering"""
    try:
        # Enhanced address selectors - targeting the specific Yelp address structure
        address_selectors = [
            # Target the specific address structure from the HTML you provided
            "address p span.raw__09f24__T4Ezm",  # Street address and city/state parts
            "address p[data-font-weight='semibold'] span.raw__09f24__T4Ezm",  # Street address part
            "address p[data-font-weight='bold'] span.raw__09f24__T4Ezm",    # City/state/zip part
            
            # Target the Location & Hours section structure you showed
            "section[aria-label*='Location'] p[data-font-weight='bold']",
            "section.y-css-15jz5c7 p[data-font-weight='bold']",
            "section[aria-label*='Location & Hours'] p[data-font-weight='bold']",
            
            # Modern Yelp address selectors
            "p[data-testid='address']",
            "div[data-testid='business-location'] p",
            "section[aria-label*='Location and Contact'] p",
            "section.y-css-1790tv2 p",
            
            # Alternative address patterns
            "address p",
            "p.y-css-qn4gww[data-font-weight='normal']",
            "p.y-css-160a82h[data-font-weight='bold']",  # From your HTML structure
            "p.y-css-dx7fqt[data-font-weight='semibold']",  # Street address class
            "p.y-css-69058c[data-font-weight='bold']",     # City/state class
            "*[class*='address'] p",
            "*[class*='location'] p",
            
            # Look for specific address containers
            "div[class*='businessInfoCard'] p",
            "div[class*='mapbox'] p",
            "div[class*='contact'] p",
            
            # Fallback selectors
            "section p", "aside p", "div p"
        ]
        
        # Keywords to exclude (promotional/non-address content)
        exclude_keywords = [
            'recently requested', 'quote', 'pricing', 'availability', 'response time',
            'response rate', 'locals', 'coverage', 'guaranteed', 'eligible', 'project',
            'get pricing', 'learn more', 'minutes', 'what type', 'service', 'hire through',
            'request a quote', 'get a quote', 'book now', 'contact for pricing',
            'free consultation', 'call for details', 'schedule', 'appointment'
        ]
        
        # Service area keywords (accept these as valid addresses for service businesses)
        service_area_keywords = [
            'serving', 'service area', 'coverage area', 'areas served', 'delivery area'
        ]
        
        print("    🔍 Trying enhanced address extraction with complete street address support...")
        
        # First, try to extract complete address from the address tag structure
        try:
            address_elements = driver.find_elements(By.CSS_SELECTOR, "address p span.raw__09f24__T4Ezm")
            if len(address_elements) >= 2:
                street_address = address_elements[0].text.strip()
                city_state_zip = address_elements[1].text.strip()
                if street_address and city_state_zip:
                    complete_address = f"{street_address}, {city_state_zip}"
                    print(f"    ✅ Found complete address from address tag: {complete_address}")
                    return complete_address
        except Exception as e:
            print(f"    ⚠️ Address tag extraction failed: {str(e)[:30]}")
        
        # Try alternative approach for complete address
        try:
            street_elem = driver.find_element(By.CSS_SELECTOR, "p.y-css-dx7fqt[data-font-weight='semibold'] span.raw__09f24__T4Ezm")
            city_elem = driver.find_element(By.CSS_SELECTOR, "p.y-css-69058c[data-font-weight='bold'] span.raw__09f24__T4Ezm")
            if street_elem and city_elem:
                street_address = street_elem.text.strip()
                city_state_zip = city_elem.text.strip()
                if street_address and city_state_zip:
                    complete_address = f"{street_address}, {city_state_zip}"
                    print(f"    ✅ Found complete address from specific classes: {complete_address}")
                    return complete_address
        except Exception as e:
            print(f"    ⚠️ Specific class extraction failed: {str(e)[:30]}")
        
        # Fallback to original selectors
        for selector in address_selectors:
            try:
                address_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for address_element in address_elements:
                    address_text = address_element.text.strip()
                    if address_text and len(address_text) > 5:
                        
                        # First check if this contains promotional content
                        is_promotional = any(keyword.lower() in address_text.lower() for keyword in exclude_keywords)
                        if is_promotional:
                            print(f"    ⚠️ Skipping promotional content: {address_text[:30]}...")
                            continue
                        
                        # Check if this is a service area (acceptable for service businesses)
                        is_service_area = any(keyword.lower() in address_text.lower() for keyword in service_area_keywords)
                        
                        # Validate this looks like a real address (contains numbers and street indicators)
                        has_number = any(char.isdigit() for char in address_text)
                        has_street_indicator = any(indicator in address_text.lower() for indicator in 
                            ['st ', 'ave ', 'avenue', 'blvd', 'boulevard', 'rd ', 'road', 'dr ', 'drive', 
                             'ln ', 'lane', 'ct ', 'court', 'pl ', 'place', 'way ', 'circle', 'square',
                             'street', ' st,', ' ave,', ' rd,', ' dr,', ' ln,', ' ct,', ' pl,', ' way,'])
                        
                        # Also accept if it has multiple parts (likely an address)
                        has_multiple_parts = ',' in address_text and len(address_text.split(',')) >= 2
                        
                        # Check for proper address format (number + street name)
                        address_pattern = re.match(r'^\d+\s+[A-Za-z]', address_text)
                        
                        # Accept service areas or proper addresses
                        if is_service_area or (has_number and has_street_indicator) or address_pattern or \
                           (has_multiple_parts and has_number and len(address_text.split()) >= 3):
                            # Final check - make sure it's not just a phone number formatted as address
                            digit_count = sum(1 for char in address_text if char.isdigit())
                            if is_service_area or digit_count < 8 or not address_text.replace('(', '').replace(')', '').replace('-', '').replace(' ', '').replace(',', '').isdigit():
                                print(f"    ✅ Found valid address using selector: {selector}")
                                print(f"    📍 Address: {address_text}")
                                return address_text
            except Exception as e:
                print(f"    ⚠️ Selector {selector} failed: {str(e)[:30]}")
                continue
        
        # Alternative approach: Look for address patterns in page source
        print("    🔍 Trying page source address extraction with filtering...")
        try:
            page_source = driver.page_source
            
            # Look for common address patterns in the HTML
            address_patterns = [
                r'<span class=" raw__09f24__T4Ezm">([^<]+)</span>[^<]*</p>[^<]*<p[^>]*data-font-weight="bold"[^>]*><span class=" raw__09f24__T4Ezm">([^<]+)</span>',
                r'data-testid="address"[^>]*>([^<]+)<',
                r'data-font-weight="bold"[^>]*>([^<]*(?:Serving|Service|Area|Street|Ave|Blvd|Rd|Dr)[^<]*)<',
                r'class="[^"]*address[^"]*"[^>]*>([^<]+)<',
                r'aria-label="[^"]*address[^"]*"[^>]*>([^<]+)<',
                r'>(\d+\s+[^<]*(?:St|Ave|Blvd|Rd|Dr|Ln|Court|Place|Way|Street|Avenue|Boulevard|Road|Drive|Lane)[^<]*)<',
                r'>(Serving [^<]*Area[^<]*)<'
            ]
            
            for pattern in address_patterns:
                matches = re.findall(pattern, page_source, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    if isinstance(match, tuple) and len(match) == 2:
                        # This is for the complete address pattern (street + city/state)
                        street_part = re.sub(r'<[^>]*>', '', match[0]).strip()
                        city_part = re.sub(r'<[^>]*>', '', match[1]).strip()
                        complete_address = f"{street_part}, {city_part}"
                        
                        # Filter out promotional content
                        is_promotional = any(keyword.lower() in complete_address.lower() for keyword in exclude_keywords)
                        if not is_promotional and len(complete_address) > 10:
                            print(f"    ✅ Found complete address in page source: {complete_address}")
                            return complete_address
                    else:
                        # Single match
                        clean_match = re.sub(r'<[^>]*>', '', str(match)).strip()
                        
                        # Filter out promotional content
                        is_promotional = any(keyword.lower() in clean_match.lower() for keyword in exclude_keywords)
                        if is_promotional:
                            continue
                        
                        # Check for service area or street address
                        is_service_area = any(keyword.lower() in clean_match.lower() for keyword in service_area_keywords)
                        
                        if len(clean_match) > 10:
                            if is_service_area:
                                print(f"    ✅ Found service area in page source: {clean_match[:50]}...")
                                return clean_match
                            elif any(char.isdigit() for char in clean_match):
                                has_street = any(street in clean_match.lower() for street in 
                                    ['st ', 'ave ', 'blvd', 'rd ', 'dr ', 'street', 'avenue', 'boulevard', 'road', 'drive'])
                                if has_street:
                                    print(f"    ✅ Found valid address in page source: {clean_match[:50]}...")
                                    return clean_match
        except Exception as e:
            print(f"    ⚠️ Page source extraction failed: {str(e)[:30]}")
        
        # Last resort: Look for ANY text that looks like an address or service area
        print("    🔍 Trying fallback address detection with filtering...")
        try:
            all_paragraphs = driver.find_elements(By.TAG_NAME, "p")
            for p in all_paragraphs:
                text = p.text.strip()
                if text and len(text) > 10:
                    
                    # Skip promotional content
                    is_promotional = any(keyword.lower() in text.lower() for keyword in exclude_keywords)
                    if is_promotional:
                        continue
                    
                    # Check for service area
                    is_service_area = any(keyword.lower() in text.lower() for keyword in service_area_keywords)
                    if is_service_area:
                        print(f"    ✅ Found service area using fallback: {text[:50]}...")
                        return text
                    
                    # Check if it looks like an address
                    has_number = any(char.isdigit() for char in text)
                    has_street_words = any(word in text.lower() for word in 
                        ['street', 'avenue', 'boulevard', 'road', 'drive', 'lane', 'st ', 'ave ', 'blvd', 'rd ', 'dr ', 'ln '])
                    has_comma = ',' in text
                    
                    if has_number and (has_street_words or has_comma) and len(text.split()) >= 3:
                        # Make sure it's not just a phone number or other irrelevant text
                        digit_count = sum(1 for char in text if char.isdigit())
                        if digit_count < 8 or not text.replace('(', '').replace(')', '').replace('-', '').replace(' ', '').replace(',', '').isdigit():
                            print(f"    ✅ Found address using fallback: {text[:50]}...")
                            return text
        except Exception as e:
            print(f"    ⚠️ Fallback detection failed: {str(e)[:30]}")
        
        print("    ❌ No valid address found with any method")
        return "N/A"
        
    except Exception as e:
        print(f"    ❌ Error extracting address: {e}")
        return "N/A"

def extract_phone_number(driver):
    """Extract business phone number"""
    try:
        phone_selectors = [
            "section.y-css-1790tv2 div.y-css-4cg16w:nth-of-type(2) p.y-css-qn4gww[data-font-weight='semibold']",
            "section.y-css-1790tv2 div.y-css-4cg16w:nth-of-type(1) p.y-css-qn4gww[data-font-weight='semibold']",
            "section.y-css-1790tv2 div.y-css-4cg16w:nth-of-type(3) p.y-css-qn4gww[data-font-weight='semibold']",
            "p[data-testid='phone-number']",
            "a[href^='tel:']"
        ]
        
        for selector in phone_selectors:
            try:
                phone_element = driver.find_element(By.CSS_SELECTOR, selector)
                phone_text = phone_element.text.strip()
                # Validate it's actually a phone number
                if phone_text and any(char.isdigit() for char in phone_text) and \
                   ('(' in phone_text or '-' in phone_text or len([c for c in phone_text if c.isdigit()]) >= 10):
                    return phone_text
            except:
                continue
        return "N/A"
    except Exception as e:
        print(f"Error extracting phone number: {e}")
        return "N/A"

def extract_website(driver):
    """Extract business website"""
    try:
        # Look for website link in various locations
        website_selectors = [
            # Primary website link patterns - including biz_redir
            "a[href*='biz_redir']",
            "a[href*='/biz_redir']",
            # Standard website patterns
            "a[data-testid='website-link']",
            "a[aria-label*='Business website']",
            "a[aria-label*='website']",
            "div[data-testid='business-website'] a",
            # Look in contact/info sections specifically
            "section[aria-label*='Location and Contact'] a[href^='http']:not([href*='yelp.com']):not([href*='facebook']):not([href*='instagram']):not([href*='twitter'])",
            "section.y-css-1790tv2 a[href^='http']:not([href*='yelp.com']):not([href*='facebook']):not([href*='instagram']):not([href*='twitter'])",
            # More specific business website patterns
            "a[href*='www.']:not([href*='yelp.com']):not([href*='facebook']):not([href*='instagram']):not([href*='twitter']):not([href*='linkedin'])",
            "a[href^='http']:not([href*='yelp.com']):not([href*='facebook']):not([href*='instagram']):not([href*='twitter']):not([href*='linkedin']):not([href*='maps.google']):not([href*='foursquare'])"
        ]
        
        # Expanded exclusion list for better filtering
        exclude_domains = [
            'yelp.com', 'facebook.com', 'instagram.com', 'twitter.com', 'linkedin.com',
            'maps.google.com', 'foursquare.com', 'yelp-ir.com', 'support.yelp.com',
            'biz.yelp.com', 'blog.yelp.com', 'engineeringblog.yelp.com', 'yelp-support.com',
            'onetrust.com', 'cookielaw.org', 'privacy.com', 'terms.com'
        ]
        
        for selector in website_selectors:
            try:
                website_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for website_element in website_elements:
                    website_url = website_element.get_attribute('href')
                    if website_url:
                        # Check for Yelp support URLs and other non-business URLs
                        non_business_domains = ['yelp-support.com', 'onetrust.com', 'cookielaw.org', 'privacy.com', 'terms.com']
                        if any(domain in website_url.lower() for domain in non_business_domains):
                            print(f"    ⚠️ Skipping non-business URL: {website_url}")
                            continue
                        
                        # Handle biz_redir URLs - extract the actual website URL
                        if 'biz_redir' in website_url:
                            try:
                                # Parse the biz_redir URL to extract the actual website
                                from urllib.parse import urlparse, parse_qs, unquote
                                parsed_url = urlparse(website_url)
                                
                                # Get query parameters
                                query_params = parse_qs(parsed_url.query)
                                
                                # Look for 'url' parameter which contains the actual website
                                if 'url' in query_params:
                                    actual_url = unquote(query_params['url'][0])
                                    # Validate that it's a proper website URL
                                    if actual_url.startswith(('http://', 'https://')):
                                        # Make sure it's not a Yelp or social media URL
                                        is_excluded = any(exclude in actual_url.lower() for exclude in exclude_domains)
                                        if not is_excluded:
                                            return actual_url
                                
                                # Alternative: try to find URL in the href itself
                                # Some biz_redir URLs have the format: .../biz_redir?url=ENCODED_URL&...
                                url_match = re.search(r'[?&]url=([^&]+)', website_url)
                                if url_match:
                                    encoded_url = url_match.group(1)
                                    try:
                                        actual_url = unquote(encoded_url)
                                        if actual_url.startswith(('http://', 'https://')):
                                            is_excluded = any(exclude in actual_url.lower() for exclude in exclude_domains)
                                            if not is_excluded:
                                                return actual_url
                                    except:
                                        pass
                                        
                            except Exception as e:
                                print(f"Error parsing biz_redir URL: {e}")
                                continue
                        
                        # For direct website links
                        else:
                            # More thorough filtering
                            is_excluded = any(exclude in website_url.lower() for exclude in exclude_domains)
                            if not is_excluded and website_url.startswith('http'):
                                # Additional validation - make sure it's a real business website
                                if any(tld in website_url for tld in ['.com', '.org', '.net', '.co', '.io', '.biz']):
                                    return website_url
            except:
                continue
                continue
        
        # Alternative approach: look for website text patterns
        try:
            # Look for website mentions in the contact section
            contact_sections = driver.find_elements(By.CSS_SELECTOR, "section, div[class*='contact'], div[class*='info']")
            for section in contact_sections:
                section_text = section.text.lower()
                if 'website' in section_text or 'site' in section_text:
                    # Look for links within this section
                    links = section.find_elements(By.CSS_SELECTOR, "a[href^='http']")
                    for link in links:
                        href = link.get_attribute('href')
                        if href and not any(exclude in href.lower() for exclude in exclude_domains):
                            return href
        except:
            pass
        
        # Fallback: search page source for biz_redir patterns and business website patterns
        try:
            page_source = driver.page_source
            
            # First look for biz_redir patterns
            biz_redir_pattern = r'biz_redir\?[^"\']*url=([^&"\']+)'
            matches = re.findall(biz_redir_pattern, page_source)
            for match in matches:
                try:
                    from urllib.parse import unquote
                    actual_url = unquote(match)
                    if actual_url.startswith(('http://', 'https://')):
                        is_excluded = any(exclude in actual_url.lower() for exclude in exclude_domains)
                        if not is_excluded:
                            return actual_url
                except:
                    continue
            
            # Look for specific website patterns that are likely business websites
            website_patterns = [
                r'href=["\']([^"\']*(?:restaurant|bistro|bar|cafe|dine)[^"\']*\.com[^"\']*)["\']',
                r'href=["\']([^"\']*www\.[^"\']*(?:restaurant|bistro|bar|cafe)[^"\']*)["\']',
                r'href=["\']([^"\']*\.(?:restaurant|bar|cafe|dine)[^"\']*)["\']'
            ]
            
            for pattern in website_patterns:
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                for match in matches:
                    if not any(exclude in match.lower() for exclude in exclude_domains):
                        if match.startswith('http') or match.startswith('www'):
                            return match if match.startswith('http') else f"https://{match}"
        except:
            pass
            
        return "N/A"
    except Exception as e:
        print(f"Error extracting website: {e}")
        return "N/A"

def extract_business_hours(driver):
    """Extract business hours"""
    try:
        hours_selectors = [
            # Modern Yelp hours selectors
            "div[data-testid='hours'] tbody tr",
            "table[aria-label*='hours'] tbody tr",
            "div[aria-label*='hours'] tr",
            # Alternative table selectors
            "table.hours-table tbody tr",
            "div.hours-table tbody tr",
            # More general selectors
            "*[class*='hours'] tr",
            "*[class*='Hours'] tr",
            # Single day selectors
            "div[data-testid='hours'] div",
            "*[class*='hours'] div[class*='day']"
        ]
        
        hours_data = []
        
        # Try table-based extraction first
        for selector in hours_selectors:
            try:
                hour_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if hour_elements:
                    for element in hour_elements:
                        hours_text = element.text.strip()
                        if hours_text and len(hours_text) > 3:  # Basic validation
                            # Clean up the text
                            cleaned_text = re.sub(r'\s+', ' ', hours_text)
                            if any(day in cleaned_text.lower() for day in 
                                 ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']):
                                hours_data.append(cleaned_text)
                    if hours_data:
                        return "; ".join(hours_data)
            except:
                continue
        
        # Alternative approach: look for hours patterns in the page
        try:
            # Look for hours section specifically
            hours_section_selectors = [
                "section[aria-label*='hours']",
                "div[data-testid='hours']",
                "*[class*='hours-section']",
                "*[class*='Hours']"
            ]
            
            for section_selector in hours_section_selectors:
                try:
                    section = driver.find_element(By.CSS_SELECTOR, section_selector)
                    section_text = section.text.strip()
                    if section_text and len(section_text) > 10:
                        # Split by lines and filter for actual hours
                        lines = section_text.split('\n')
                        valid_hours = []
                        for line in lines:
                            line = line.strip()
                            if any(day in line.lower() for day in 
                                 ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']) and \
                               any(time_indicator in line.lower() for time_indicator in ['am', 'pm', ':', 'closed', 'open']):
                                valid_hours.append(line)
                        if valid_hours:
                            return "; ".join(valid_hours)
                except:
                    continue
        except:
            pass
        
        # Last resort: search page source for hours pattern
        try:
            page_source = driver.page_source
            # Look for common hours patterns
            hours_pattern = re.search(r'((?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)[^<]*(?:am|pm|AM|PM|closed|Closed))', page_source)
            if hours_pattern:
                return hours_pattern.group(1).strip()
        except:
            pass
            
        return "N/A"
    except Exception as e:
        print(f"Error extracting business hours: {e}")
        return "N/A"



def scrape_business_info(driver, url, category, location):
    """Main function to scrape all business information (assumes session is established)"""
    try:
        print(f"\n🎯 Scraping: {url}")
        
        # Add random delay before visiting business page
        delay = random.uniform(1, 2)  # Reduced delay as requested
        print(f"⏰ Waiting {delay:.1f} seconds before visiting business page...")
        time.sleep(delay)
        
        driver.get(url)
        
        # Enhanced human-like behavior on business page
        print("👁️ Simulating human reading behavior on business page...")
        time.sleep(random.uniform(1, 2))  # Reduced delay as requested
        
        # Simulate reading - scroll around the page like a human
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(random.uniform(1, 2))
        driver.execute_script("window.scrollTo(0, 600);")
        time.sleep(random.uniform(1, 2))
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(0.5, 1))
        
        # Wait for page to load with multiple fallback elements
        try:
            WebDriverWait(driver, 20).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='business-name']")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".y-css-qn4gww h1"))
                )
            )
        except:
            print("⚠️ Warning: Page may not have loaded completely")
        
        # Additional wait for dynamic content
        time.sleep(random.uniform(1, 3))
        
        # Extract business name with multiple fallback selectors
        business_name = "N/A"
        name_selectors = [
            "h1",
            "[data-testid='business-name']",
            ".y-css-qn4gww h1",
            "h1.y-css-qn4gww"
        ]
        
        for selector in name_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                name = element.text.strip()
                if name and len(name) > 1:
                    business_name = name
                    break
            except:
                continue
        
        print(f"📊 Extracting data for: {business_name}")
        
        # Extract all information with progress indication and random delays
        print("  📍 Extracting address...")
        address = extract_address(driver)
        # Smart address handling - append location only if the exact location string isn't already there
        if address != "N/A":
            # Check if the word "serving" is in the address
            if "serving" in address.lower():
                address = f"{address} {location}"
            # Check if the exact user location is already at the end of the address
            elif not address.lower().endswith(location.lower()):
                address = f"{address}"
        else:
            address = location
        time.sleep(random.uniform(0.2, 0.5))
        
        print("  ⭐ Extracting rating...")
        rating = extract_rating(driver)
        time.sleep(random.uniform(0.2, 0.5))
        
        print("  💬 Extracting review count...")
        review_count = extract_review_count(driver)
        time.sleep(random.uniform(0.2, 0.5))
        
        print("  📞 Extracting phone number...")
        phone = extract_phone_number(driver)
        time.sleep(random.uniform(0.2, 0.5))
        
        print("  🌐 Extracting website...")
        website = extract_website(driver)
        time.sleep(random.uniform(0.2, 0.5))
        
        print("  🕒 Extracting business hours...")
        business_hours = extract_business_hours(driver)
        
        # Simulate human behavior - scroll around after extraction
        print("👁️ Final page review simulation...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(random.uniform(0.5, 1))
        driver.execute_script("window.scrollTo(0, 0);")
        
        business_info = {
            'business_name': business_name,
            'rating': rating,
            'review_count': review_count,
            'address': address,
            'phone': phone,
            'website': website,
            'categories': category,  # Use user input category
            'business_hours': business_hours,
            'yelp_url': url
        }
        
        # Print extracted info for verification
        print(f"✅ Business: {business_info['business_name']}")
        print(f"✅ Rating: {business_info['rating']}")
        print(f"✅ Reviews: {business_info['review_count']}")
        print(f"✅ Phone: {business_info['phone']}")
        print(f"✅ Website: {business_info['website']}")
        print(f"✅ Address: {business_info['address']}")
        print(f"✅ Category: {business_info['categories']}")
        print(f"✅ Hours: {business_info['business_hours'][:50]}..." if len(business_info['business_hours']) > 50 else f"✅ Hours: {business_info['business_hours']}")
        
        return business_info
        
    except Exception as e:
        print(f"❌ Error scraping {url}: {str(e)}")
        return {
            'business_name': 'N/A',
            'rating': 'N/A',
            'review_count': 'N/A',
            'address': location,  # Use location as fallback
            'phone': 'N/A',
            'website': 'N/A',
            'categories': category,  # Use user input category
            'business_hours': 'N/A',
            'yelp_url': url
        }

def main():
    """Main function to run the scraper"""
    print("="*60)
    print("           YELP BUSINESS SEARCH SCRAPER")
    print("="*60)
    print("This tool will search Yelp for businesses and extract their information")
    print()
    
    # Get user input
    category = input("Enter business category (e.g., 'restaurants', 'pizza', 'dentist'): ").strip()
    if not category:
        print("Error: Business category is required!")
        return
    
    location = input("Enter location (e.g., 'New York, NY', 'Los Angeles, CA'): ").strip()
    if not location:
        print("Error: Location is required!")
        return
    
    # Get number of pages to scrape
    try:
        max_pages = input("How many pages to scrape? (default: 3, max: 10): ").strip()
        max_pages = int(max_pages) if max_pages else 3
        max_pages = min(max_pages, 10)  # Limit to 10 pages
    except ValueError:
        max_pages = 3
    
    # Generate output filename
    safe_category = re.sub(r'[^\w\s-]', '', category).strip().replace(' ', '_')
    safe_location = re.sub(r'[^\w\s-]', '', location).strip().replace(' ', '_')
    output_file = f"yelp_{safe_category}_{safe_location}.csv"
    
    print(f"\nSearching for '{category}' businesses in '{location}'...")
    print(f"Will scrape up to {max_pages} pages of results")
    print(f"Results will be saved to: {output_file}")
    print("\nStarting search...")
    
    driver = get_driver()
    
    try:
        # First, establish a verified session with Yelp (one-time verification)
        establish_session(driver)
        
        # Search for businesses (session already established, no repeated verification)
        business_urls = search_yelp_businesses(driver, category, location, max_pages)
        
        if not business_urls:
            print("No businesses found for the given search criteria.")
            return
        
        print(f"\nFound {len(business_urls)} businesses. Starting detailed scraping...")
        
        # Create CSV file and write header
        fieldnames = [
            'business_name', 'rating', 'review_count', 'address', 
            'phone', 'website', 'categories', 
            'business_hours', 'yelp_url'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Scrape each business with enhanced stealth
            for i, url in enumerate(business_urls, 1):
                print(f"\n[{i}/{len(business_urls)}] Processing business...")
                business_info = scrape_business_info(driver, url, category, location)
                writer.writerow(business_info)
                
                # Extended random delay between requests for stealth
                if i < len(business_urls):
                    delay = random.uniform(2, 4)  # Reduced delay as requested
                    print(f"😴 Stealth delay: {delay:.1f} seconds before next request...")
                    time.sleep(delay)
                    
                    # Additional human simulation between businesses
                    if i % 5 == 0:  # Every 5th business instead of 3rd
                        print("🧑 Simulating brief human break...")
                        extra_delay = random.uniform(3, 6)  # Reduced break time
                        print(f"☕ Taking a {extra_delay:.1f} second break to appear more human...")
                        time.sleep(extra_delay)
        
        print(f"\n{'='*60}")
        print(f"SCRAPING COMPLETE!")
        print(f"{'='*60}")
        print(f"✅ Successfully scraped {len(business_urls)} businesses")
        print(f"📁 Data saved to: {output_file}")
        print(f"🔍 Search: {category} in {location}")
        print(f"{'='*60}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

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
