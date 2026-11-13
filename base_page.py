class BasePage:
    def __init__(self, page):
        self.page = page

    def open(self, path=""):
        self.page.goto(f"{self.base_url}{path}")

    @property
    def base_url(self):
        from config import BASE_URL
        return BASE_URL
