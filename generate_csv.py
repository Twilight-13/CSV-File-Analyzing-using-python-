import csv
import random
import datetime
import names

countries = ["United States", "Canada", "United Kingdom", "Germany", "Australia", "France", "Japan", "Brazil", "India", "China", "Italy", "Spain", "Netherlands", "Sweden", "Mexico", "South Korea", "Russia", "Argentina", "Turkey", "South Africa"]
product_categories = ["Electronics", "Clothing", "Home Goods", "Books"]

def generate_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates + 1) # +1 to include the end date
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date.strftime("%Y-%m-%d")

with open("sales_data_500.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["SL_No", "Country", "Customer_Name", "Amount", "Order_Date", "Ship_Date", "Product_Category"])

    for i in range(1, 501):
        country = random.choice(countries)
        customer_name = names.get_full_name()
        amount = random.randint(50, 300) * 1000 + random.randint(0, 999)
        order_date = generate_random_date(datetime.date(2023, 10, 26), datetime.date(2024, 9, 30))
        order_datetime = datetime.datetime.strptime(order_date, "%Y-%m-%d").date()
        ship_date = (order_datetime + datetime.timedelta(days=random.randint(1, min(20,(datetime.date(2024, 10, 5) - order_datetime).days)))).strftime("%Y-%m-%d") #ship date within 20 days of order date
        product_category = random.choice(product_categories)
        writer.writerow([i, country, customer_name, amount, order_date, ship_date, product_category])

print("CSV file 'sales_data_500.csv' generated successfully.")