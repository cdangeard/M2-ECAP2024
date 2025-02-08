from playwright.sync_api import Page, expect, sync_playwright

url = 'https://www.youtube.com/watch?v=6cnx0xU8EtE'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    consentCss = 'ytd-button-renderer.ytd-consent-bump-v2-lightbox:nth-child(2) > yt-button-shape:nth-child(1) > button:nth-child(1)'
    page.wait_for_selector(consentCss)
    page.click(consentCss)
    height = 0
    for i in range(1000):
        page.keyboard.press('PageDown')
        page.wait_for_timeout(1000)
        new_height = page.evaluate('document.documentElement.scrollHeight')
        print(new_height)
        if new_height == height:
            break
        height = new_height
    comments = page.query_selector_all('#content-text > span')
    print(len(comments), ' comments found')
    print([comment.text_content() for comment in comments])