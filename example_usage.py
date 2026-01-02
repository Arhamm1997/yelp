"""
Example usage of the Google Business Profile Scraper
This script demonstrates how to use the scraper programmatically
"""

import csv
from google_business_scraper import (
    get_driver,
    establish_session,
    search_google_maps_businesses,
    scrape_business_info
)

def example_single_location():
    """Example: Scrape restaurants in a single city"""
    print("="*70)
    print("EXAMPLE 1: Single Location Scraping")
    print("="*70)

    category = "Italian restaurants"
    location = "New York, NY"
    max_results = 10

    driver = get_driver()

    try:
        # Establish session
        establish_session(driver)

        # Search for businesses
        businesses = search_google_maps_businesses(driver, category, location, max_results)

        # Scrape each business
        results = []
        for i, business in enumerate(businesses, 1):
            print(f"\nScraping {i}/{len(businesses)}...")
            info = scrape_business_info(driver, business['url'], category, location)
            results.append(info)

        # Save to CSV
        with open('example_single_location.csv', 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['business_name', 'rating', 'review_count', 'address',
                         'phone', 'website', 'categories', 'business_hours', 'google_maps_url']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"\n✅ Saved {len(results)} businesses to example_single_location.csv")

    finally:
        driver.quit()

def example_multiple_locations():
    """Example: Scrape dentists across multiple cities"""
    print("="*70)
    print("EXAMPLE 2: Multiple Location Scraping")
    print("="*70)

    category = "Dentist"
    locations = [
        "Miami, FL",
        "Orlando, FL",
        "Tampa, FL"
    ]
    max_results_per_location = 5

    driver = get_driver()
    all_results = []

    try:
        # Establish session once
        establish_session(driver)

        # Scrape each location
        for location in locations:
            print(f"\n{'='*70}")
            print(f"Processing: {location}")
            print(f"{'='*70}")

            businesses = search_google_maps_businesses(driver, category, location, max_results_per_location)

            for i, business in enumerate(businesses, 1):
                print(f"\nScraping {i}/{len(businesses)} in {location}...")
                info = scrape_business_info(driver, business['url'], category, location)
                all_results.append(info)

        # Save all results
        with open('example_multiple_locations.csv', 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['business_name', 'rating', 'review_count', 'address',
                         'phone', 'website', 'categories', 'business_hours', 'google_maps_url']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_results)

        print(f"\n✅ Saved {len(all_results)} businesses from {len(locations)} locations to example_multiple_locations.csv")

    finally:
        driver.quit()

def example_custom_processing():
    """Example: Custom data processing after scraping"""
    print("="*70)
    print("EXAMPLE 3: Custom Data Processing")
    print("="*70)

    category = "Coffee shop"
    location = "Seattle, WA"
    max_results = 10

    driver = get_driver()

    try:
        establish_session(driver)
        businesses = search_google_maps_businesses(driver, category, location, max_results)

        results = []
        for business in businesses:
            info = scrape_business_info(driver, business['url'], category, location)
            results.append(info)

        # Custom processing: Filter by rating
        high_rated = [b for b in results if b['rating'] != 'N/A' and float(b['rating']) >= 4.5]

        print(f"\n📊 Analysis Results:")
        print(f"Total businesses scraped: {len(results)}")
        print(f"Businesses with rating ≥ 4.5: {len(high_rated)}")

        # Save filtered results
        with open('example_high_rated.csv', 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['business_name', 'rating', 'review_count', 'address',
                         'phone', 'website', 'categories', 'business_hours', 'google_maps_url']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(high_rated)

        print(f"✅ Saved {len(high_rated)} high-rated businesses to example_high_rated.csv")

        # Print top 3
        print("\n🏆 Top 3 Highest Rated:")
        sorted_results = sorted(
            [b for b in results if b['rating'] != 'N/A'],
            key=lambda x: float(x['rating']),
            reverse=True
        )[:3]

        for i, business in enumerate(sorted_results, 1):
            print(f"{i}. {business['business_name']} - {business['rating']} stars ({business['review_count']} reviews)")

    finally:
        driver.quit()

if __name__ == "__main__":
    print("\nGoogle Business Scraper - Example Usage\n")
    print("Choose an example to run:")
    print("1. Single location scraping")
    print("2. Multiple locations scraping")
    print("3. Custom data processing")
    print("4. Run all examples")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        example_single_location()
    elif choice == "2":
        example_multiple_locations()
    elif choice == "3":
        example_custom_processing()
    elif choice == "4":
        example_single_location()
        print("\n" + "="*70 + "\n")
        example_multiple_locations()
        print("\n" + "="*70 + "\n")
        example_custom_processing()
    else:
        print("Invalid choice!")
