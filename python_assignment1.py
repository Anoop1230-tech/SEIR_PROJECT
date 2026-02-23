import sys
import re
from collections import Counter
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

P = 53
MOD = 2**64
HASH_BITS = 64

# Fetch body text using Playwright
def fetch_text(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=60000)
        except Exception as e:
            print("Error loading:", url)
            print(e)
            browser.close()
            return ""
        html = page.content()
        browser.close()
    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    if soup.body:
        return soup.body.get_text(separator=" ", strip=True)
    return ""

# Count word frequency
def word_frequency(text):
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return Counter(words)

# 64-bit Polynomial Rolling Hash
def word_hash(word):
    h = 0
    power = 1
    for ch in word:
        h = (h + ord(ch) * power) % MOD
        power = (power * P) % MOD
    return h

# Compute SimHash
def compute_simhash(freq_map):
    vector = [0] * HASH_BITS
    for word, count in freq_map.items():
        h = word_hash(word)
        for i in range(HASH_BITS):
            bit = (h >> i) & 1
            if bit == 1:
                vector[i] += count
            else:
                vector[i] -= count
    simhash = 0
    for i in range(HASH_BITS):
        if vector[i] > 0:
            simhash |= (1 << i)
    return simhash

# Count common bits between hashes
def common_bits(hash1, hash2):
    xor = hash1 ^ hash2
    different_bits = bin(xor).count("1")
    return HASH_BITS - different_bits

def main():
    if len(sys.argv) != 3:
        sys.exit()

    url1 = sys.argv[1]
    url2 = sys.argv[2]

    # Processing first URL
    text1 = fetch_text(url1)
    freq1 = word_frequency(text1)
    simhash1 = compute_simhash(freq1)

    # Processing second URL
    text2 = fetch_text(url2)
    freq2 = word_frequency(text2)
    simhash2 = compute_simhash(freq2)

    common = common_bits(simhash1, simhash2)

    print("\nResult:")
    # print("freq1:",freq1)
    # print("freq2:",freq2)
    print("Common bits in SimHash:", common, "out of 64")

if __name__ == "__main__":
    main()