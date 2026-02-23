import sys
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def scrape_website(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=60000)
        except Exception as e:
            print("Error loading page:", e)
            browser.close()
            return
        html = page.content()
        browser.close()
    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Print title
    if soup.title:
        print("Title:", soup.title.get_text(strip=True))
    else:
        print("No title found")

    # Print page text
    if soup.body:
        print("\nPage Text:\n")
        print(soup.body.get_text(strip=True,separator='\n'))

    # Print links
    print("\nLinks:\n")
    links = set()
    for a in soup.find_all("a", href=True):
        full_link = urljoin(url, a["href"])
        links.add(full_link)
    for link in links:
        print(link)

def main():
    if len(sys.argv) != 2:
        sys.exit()

    url = sys.argv[1]
    scrape_website(url)

if __name__ == "__main__":
    main()