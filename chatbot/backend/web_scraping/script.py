from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from chromedriver_py import binary_path
import time
from urllib.parse import urljoin

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service(executable_path=binary_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
visited_urls = set()


def is_social_media_link(link):
    social_media_domains = ['facebook.com', 'twitter.com',
                            'linkedin.com', 'instagram.com', 'youtube.com']
    for domain in social_media_domains:
        if domain in link:
            return True
    return False


def extract_links(url):
    driver.get(url)
    time.sleep(5)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    links = set()
    for a_tag in soup.find_all('a', href=True):
        link = urljoin(url, a_tag['href'])
        if not is_social_media_link(link):
            links.add(link)

    return links


def scrape_dynamic_page(url):
    driver.get(url)
    time.sleep(5)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    for element in soup.find_all(['header', 'footer', 'nav']):
        element.decompose()

    main_content = (soup.find('main') or
                    soup.find('article') or soup.find('body'))
    if not main_content:
        raise ValueError("Main content not found on the page.")

    text = main_content.get_text(separator=' ', strip=True)
    return text


def scrape_nested_links(start_url, depth=2):
    if depth == 0 or start_url in visited_urls:
        return

    print(f"Scraping: {start_url}")
    visited_urls.add(start_url)

    try:
        scraped_text = scrape_dynamic_page(start_url)
        print("Scraped Content:")
        print(scraped_text)

        links = extract_links(start_url)

        for link in links:
            scrape_nested_links(link, depth - 1)
    except Exception as e:
        print(f"Error scraping {start_url}: {e}")
