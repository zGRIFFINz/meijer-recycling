from bs4 import BeautifulSoup

beverages = []
alcohols = []
sorted_drinks = []

with open("./meijer-all-beverage-html", "r", encoding="utf-8") as file1:
    beverage_html = file1.read()

with open("./meijer-all-alcohol-html", "r", encoding="utf-8") as file2:
    alcohol_html = file2.read()

soup1 = BeautifulSoup(beverage_html, "html.parser")
soup2 = BeautifulSoup(alcohol_html, "html.parser")


def beverage_parser():
    beverage_items = soup1.find_all("h2", class_="product-tile--line-clamp-text")
    for beverage in beverage_items:
        beverages.append(beverage.get_text())
    return beverages


def alcohol_parser():
    alcohol_items = soup2.find_all("h2", class_="product-tile--line-clamp-text")
    for alcohol in alcohol_items:
        alcohols.append(alcohol.get_text())
    return alcohols


def drink_mixer(beverages, alcohols):
    drinks = beverages
    drinks.extend(alcohols)
    sorted_drinks = sorted(drinks)
    sorted_drinks.sort(key=str.lower)
    print(sorted_drinks)
    return sorted_drinks


beverages = beverage_parser()
alcohols = alcohol_parser()
sorted_drinks = drink_mixer(beverages, alcohols)


with open("./all-drinks", "w") as file3:
    for i in sorted_drinks:
        file3.writelines(f"{i}"+"\n")
