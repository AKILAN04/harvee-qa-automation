from pages.base_page import BasePage

class CartPage(BasePage):
    item_names = ".inventory_item_name"
    checkout_button = "#checkout"

    def names(self):
        return self.page.locator(self.item_names).all_inner_texts()

    def checkout(self):
        self.page.locator(self.checkout_button).click()
