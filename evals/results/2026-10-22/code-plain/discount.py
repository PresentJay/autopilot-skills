def discount(price, percent):
    return price * (1 - min(percent, 100) / 100)
