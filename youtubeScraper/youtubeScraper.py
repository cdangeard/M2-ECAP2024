from playwright.sync_api import Page, expect, sync_playwright
import sys

class Youtube_scraper:
    """
    Classe qui permet de scrapper les commentaires d'une vidéo youtube
    Elle utilise un navigateur firefox pour scroller la page et récupérer les commentaires
    
    Fonctionnement : 
    - Clique sur accepter les conditions d'utilisation
    - Scrolle la page jusqu'en bas ou jusqu'a *limitScrolls*
    - Récupère les commentaires dans une liste

    Args:
        limitScrolls (int, optional): Nombre de scrolls à effectuer. Defaults to None.
    """
    def __init__(self, limitScrolls: int = None, headless: bool = False) -> None:
        self.limitScrolls = limitScrolls
        self.page = None
        self.headless = headless

    def click_consent(self, page: Page) -> None:
        """
        Fonction attend et clique sur le bouton de consentement
        """        
        consentCss = 'ytd-button-renderer.ytd-consent-bump-v2-lightbox:nth-child(2) > yt-button-shape:nth-child(1) > button:nth-child(1)'
        page.wait_for_selector(consentCss)
        page.click(consentCss)

    def scroll_down(self, page: Page) -> None:
        """
        Fonction qui permet de scroller la page jusqu'en bas
        """
        scrolls = 0
        while not self.limitScrolls or scrolls < self.limitScrolls:
            scrolls += 1
            height = page.evaluate('document.body.scrollHeight')
            page.evaluate('window.scrollBy(0, window.innerHeight)')
            new_height = page.evaluate('document.body.scrollHeight')
            if new_height == height:
                break
            page.wait_for_timeout(1000)

    def get_comments(self, url) -> list:
        """
        Récupère les commentaires d'une vidéo youtube

        Args:
            url (str): url de la vidéo youtube
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            page.goto(url)
            print('waiting for page to load')
            self.click_consent(page)
            print('Consent button clicked')
            print('Scrolling down')
            self.scroll_down(page)
            print('Done scrolling')
            comments = page.query_selector_all('#content-text > span')
            print(len(comments), ' comments found')
            return [comment.text_content() for comment in comments]
    
    def write_comments(self, comments, url):
        """
        Ecrit les commentaires dans un fichier texte
        
        Args:
            comments (list): liste des commentaires
            url (str): url de la vidéo youtube
        """
        with open(f'comments_{url.split("=")[1]}.txt', 
                  'w', encoding='utf-8') as file:
            for comment in comments:
                try:
                    file.write(comment)
                    file.write('\n\n')
                except:
                    print('Error writing comment')
                    print(comment)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        url = 'https://www.youtube.com/watch?v=8hK732DrDU8'
    else:
        url = sys.argv[1]
    tp = Youtube_scraper(limitScrolls=10, headless=False)
    comments = tp.get_comments(url)
    tp.write_comments(comments, url)