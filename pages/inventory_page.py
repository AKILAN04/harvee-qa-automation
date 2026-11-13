from pages.base_page import BasePage

class InventoryPage(BasePage):
    sort_dropdown = "[data-test='product-sort-container']"
    product_names = ".inventory_item_name"
    product_prices = ".inventory_item_price"
    cart_badge = ".shopping_cart_badge"
    cart_link = ".shopping_cart_link"

    def sort(self, option):
        self.page.locator(self.sort_dropdown).select_option(option)

    def names(self):
        return self.page.locator(self.product_names).all_inner_texts()

    def prices(self):
        return [float(x.replace("$", "")) for x in self.page.locator(self.product_prices).all_inner_texts()]

    def add_product(self, product_name):
        item = self.page.locator(".inventory_item").filter(has=self.page.get_by_text(product_name, exact=True))
        item.locator("button").click()

    def remove_product(self, product_name):
        item = self.page.locator(".inventory_item").filter(has=self.page.get_by_text(product_name, exact=True))
        item.locator("button").click()

    def badge_count(self):
        badge = self.page.locator(self.cart_badge)
        return int(badge.inner_text()) if badge.count() else 0

    def open_cart(self):
        self.page.locator(self.cart_link).click()
