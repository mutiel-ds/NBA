from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from soup import Soup    

class Driver():
    def __init__(self, game_id, show: bool = True):
        self.show = show
        self.url = f"https://www.nba.com/game/{game_id}"
        self.driver = self.init_driver()

    def init_driver(self):
        if self.show:
            driver = Firefox()
        else:
            options = Options()
            options.add_argument("--headless")
            driver = Firefox(options=options)
        driver.get(self.url)
        return driver
    
    def close_driver(self):
        self.driver.close()
    
    def get_soup(self):
        soup = Soup(self.driver.page_source)
        return soup
    
    def get_box_score(self):
        self.driver.get(self.url+"/box-score")
        return self.get_soup()