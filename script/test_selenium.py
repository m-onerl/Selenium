import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Ścieżka do pliku przechowującego ceny
prices_file = 'prices.json'

# Funkcja do odczytu cen z pliku
def read_prices():
    if os.path.exists(prices_file):
        with open(prices_file, 'r') as file:
            return json.load(file)
    return {}

# Funkcja do zapisu cen do pliku
def write_prices(prices):
    with open(prices_file, 'w') as file:
        json.dump(prices, file, indent=4)

# Użycie WebDriver Manager do zainstalowania odpowiedniej wersji ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(10)
driver.maximize_window()

# Nawigacja do aplikacji
driver.get('http://magento.softwaretestingboard.com/')
search_field = driver.find_element(By.NAME, 'q')
search_field.clear()
search_field.send_keys('t-shirt')
search_field.submit()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='product-item-info']"))
)

# Odczyt starych cen z pliku
old_prices = read_prices()
new_prices = {}

products = driver.find_elements(By.XPATH, "//div[@class='product-item-info']")
for product in products:
    name = product.find_element(By.XPATH, ".//a[@class='product-item-link']").text
    price = product.find_element(By.XPATH, ".//span[@class='price']").text
    new_prices[name] = price
    
    old_price = old_prices.get(name, 'Brak danych')
    change = 'Brak zmian'
    
    if old_price != 'Brak danych':
        old_price_value = float(old_price.strip('$'))
        new_price_value = float(price.strip('$'))
        change_value = new_price_value - old_price_value
        change = f"{change_value:+.2f} USD"
    
    print(f"Produkt: {name}, Stara cena: {old_price}, Nowa cena: {price}, Zmiana: {change}")

# Zapis nowych cen do pliku
write_prices(new_prices)

driver.quit()
