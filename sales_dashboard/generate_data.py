import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

products = {
    "Laptop Pro 15": "Electronics",
    "Wireless Mouse": "Electronics",
    "Office Chair": "Furniture",
    "Standing Desk": "Furniture",
    "Bluetooth Speaker": "Electronics",
    "Yoga Mat": "Fitness",
    "Running Shoes": "Fitness",
    "Coffee Maker": "Home Appliances",
    "Air Fryer": "Home Appliances",
    "Backpack": "Accessories",
    "Smart Watch": "Electronics",
    "Desk Lamp": "Furniture",
}

regions = ["North", "South", "East", "West", "Central"]
salespeople = ["Aarav Sharma", "Priya Patel", "Rohan Mehta", "Sneha Gupta", "Vikram Singh", "Anita Rao"]

positive_reviews = [
    "Absolutely love this product, exceeded my expectations!",
    "Great quality and fast delivery, highly recommend.",
    "Best purchase I've made this year, works perfectly.",
    "Excellent value for money, very satisfied.",
    "Amazing product, will definitely buy again.",
    "Super happy with this purchase, five stars!",
    "Works exactly as described, very impressed.",
    "Outstanding quality, customer service was helpful too.",
]

neutral_reviews = [
    "It's okay, does the job but nothing special.",
    "Average product, met basic expectations.",
    "Decent for the price, could be better.",
    "It's fine, not amazing but not bad either.",
    "Works as expected, no complaints so far.",
]

negative_reviews = [
    "Very disappointed, product broke after a week.",
    "Poor quality, would not recommend this at all.",
    "Terrible experience, delivery was late and item was damaged.",
    "Not worth the money, quite frustrated with this purchase.",
    "Product stopped working within days, very unhappy.",
    "Bad quality material, feels cheap and flimsy.",
]

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 6, 30)

rows = []
for i in range(400):
    product = random.choice(list(products.keys()))
    category = products[product]
    region = random.choice(regions)
    salesperson = random.choice(salespeople)
    date = random_date(start_date, end_date)
    units = random.randint(1, 25)
    base_price = {
        "Laptop Pro 15": 78000, "Wireless Mouse": 899, "Office Chair": 6500,
        "Standing Desk": 15500, "Bluetooth Speaker": 2499, "Yoga Mat": 799,
        "Running Shoes": 3499, "Coffee Maker": 4200, "Air Fryer": 5800,
        "Backpack": 1899, "Smart Watch": 12500, "Desk Lamp": 1299
    }[product]
    unit_price = round(base_price * random.uniform(0.9, 1.1), 2)
    revenue = round(units * unit_price, 2)

    sentiment_type = random.choices(["pos", "neu", "neg"], weights=[0.55, 0.25, 0.20])[0]
    if sentiment_type == "pos":
        review = random.choice(positive_reviews)
    elif sentiment_type == "neu":
        review = random.choice(neutral_reviews)
    else:
        review = random.choice(negative_reviews)

    rows.append({
        "Date": date.strftime("%Y-%m-%d"),
        "Product": product,
        "Category": category,
        "Region": region,
        "Salesperson": salesperson,
        "Units Sold": units,
        "Unit Price": unit_price,
        "Revenue": revenue,
        "Customer Review": review
    })

df = pd.DataFrame(rows).sort_values("Date").reset_index(drop=True)
df.to_csv("data/sales_data.csv", index=False)
print(df.shape)
print(df.head())
