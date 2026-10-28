def discount(price, percent):
    percent = min(percent, 100)
    return price * (1 - percent / 100)
