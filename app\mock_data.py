from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


CATEGORIES = ["food", "daily_goods", "stationery", "small_appliance", "personal_care"]
CHANNELS = ["wechat_shop", "douyin", "taobao", "offline_store"]
CITIES = ["Guiyang", "Zunyi", "Chengdu", "Kunming", "Changsha", "Wuhan"]


def generate_mock_data(output_dir: Path, seed: int = 42) -> dict[str, Path]:
    """Generate a realistic small retail dataset for the demo workflow."""
    rng = random.Random(seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    today = date.today()
    start = today - timedelta(days=180)

    products = []
    for i in range(1, 41):
        category = rng.choice(CATEGORIES)
        cost = rng.randint(8, 160)
        price = round(cost * rng.uniform(1.25, 2.2), 2)
        products.append(
            {
                "product_id": f"P{i:03d}",
                "product_name": f"{category}_item_{i:03d}",
                "category": category,
                "brand": f"brand_{rng.randint(1, 8)}",
                "cost": cost,
                "price": price,
            }
        )
    products_df = pd.DataFrame(products)

    users = []
    for i in range(1, 601):
        register_date = start + timedelta(days=rng.randint(0, 150))
        users.append(
            {
                "user_id": f"U{i:04d}",
                "city": rng.choice(CITIES),
                "age_group": rng.choice(["18-24", "25-34", "35-44", "45+"]),
                "register_date": register_date.isoformat(),
                "source": rng.choice(CHANNELS),
            }
        )
    users_df = pd.DataFrame(users)

    orders = []
    for i in range(1, 4201):
        order_date = start + timedelta(days=rng.randint(0, 179))
        product = products_df.sample(1, random_state=rng.randint(1, 100000)).iloc[0]
        quantity = rng.choices([1, 2, 3, 4, 5], weights=[55, 24, 11, 6, 4])[0]
        discount = rng.choice([0, 0, 0, 0.05, 0.1, 0.15])
        unit_price = round(float(product["price"]) * (1 - discount), 2)
        refund_flag = rng.random() < 0.035
        orders.append(
            {
                "order_id": f"O{i:05d}",
                "user_id": f"U{rng.randint(1, 600):04d}",
                "product_id": product["product_id"],
                "order_date": order_date.isoformat(),
                "channel": rng.choice(CHANNELS),
                "quantity": quantity,
                "unit_price": unit_price,
                "discount_rate": discount,
                "refund_flag": int(refund_flag),
            }
        )
    orders_df = pd.DataFrame(orders)
    orders_df["amount"] = (orders_df["quantity"] * orders_df["unit_price"]).round(2)

    inventory = []
    for _, product in products_df.iterrows():
        inventory.append(
            {
                "product_id": product["product_id"],
                "stock": rng.randint(0, 400),
                "safety_stock": rng.randint(30, 80),
                "warehouse": rng.choice(["Guiyang_A", "Guiyang_B", "Chengdu_A"]),
            }
        )
    inventory_df = pd.DataFrame(inventory)

    marketing = []
    for day_offset in range(0, 180):
        event_date = start + timedelta(days=day_offset)
        for channel in CHANNELS:
            spend = rng.randint(80, 1600) if channel != "offline_store" else rng.randint(0, 300)
            clicks = max(1, int(spend * rng.uniform(1.5, 4.0)))
            conversions = max(0, int(clicks * rng.uniform(0.01, 0.08)))
            marketing.append(
                {
                    "date": event_date.isoformat(),
                    "channel": channel,
                    "campaign": f"{channel}_campaign_{day_offset // 30 + 1}",
                    "spend": spend,
                    "clicks": clicks,
                    "conversions": conversions,
                }
            )
    marketing_df = pd.DataFrame(marketing)

    review_templates = {
        5: ["fast delivery", "good value", "will buy again", "quality is stable"],
        4: ["overall good", "price is acceptable", "service is nice"],
        3: ["average experience", "packaging can improve", "delivery was slow"],
        2: ["not worth the price", "quality issue", "bad packaging"],
        1: ["refund requested", "very disappointed", "damaged item"],
    }
    reviews = []
    sampled_orders = orders_df.sample(1400, random_state=seed)
    for _, order in sampled_orders.iterrows():
        rating = rng.choices([1, 2, 3, 4, 5], weights=[4, 7, 15, 34, 40])[0]
        reviews.append(
            {
                "review_id": f"R{len(reviews) + 1:05d}",
                "order_id": order["order_id"],
                "rating": rating,
                "comment": rng.choice(review_templates[rating]),
                "review_date": order["order_date"],
            }
        )
    reviews_df = pd.DataFrame(reviews)

    tables = {
        "orders": orders_df,
        "users": users_df,
        "products": products_df,
        "inventory": inventory_df,
        "marketing": marketing_df,
        "reviews": reviews_df,
    }
    paths = {}
    for name, df in tables.items():
        path = output_dir / f"{name}.csv"
        df.to_csv(path, index=False, encoding="utf-8-sig")
        paths[name] = path
    return paths

