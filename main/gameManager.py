
class GameManager:
    def __init__(self):
        self.current_page = None

    def change_page(self, page):
        self.current_page = page

    def direct_page(self, page):
        self.change_page(page)
        self.current_page.start()
