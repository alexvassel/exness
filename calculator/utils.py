def get_discount_by_price(price: float) -> int:
    if type(price) is not float or price <= 0 or price < 1000:
        return 0
    if price in range(1000, 5000):
        return 3
    if price in range(5000, 7000):
        return 5
    if price in range(7000, 10000):
        return 7
    if price in range(10000, 50000):
        return 10
    if price >= 50000:
        return 15
    return 0


def get_price_with_tax(price: float, tax: float) -> float:
    if type(price) is not float or price <= 0:
        return price
    if type(tax) is not float or tax <= 0:
        return price
    return float(price + price * tax / 100)


def get_price_with_discount(price: float, discount: int) -> float:
    if type(price) is not float or price <= 0:
        return price
    if type(discount) is not int or discount <= 0:
        return price
    return float(price - price * discount / 100)
