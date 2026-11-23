def discount(price, percent):
    if percent > 100:
        percent = 100
    return price * (1 - percent / 100)
