from __future__ import annotations

import pandas as pd


def analyze_retail_business(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame | dict]:
    orders = tables["orders"].copy()
    products = tables["products"].copy()
    users = tables.get("users", pd.DataFrame()).copy()
    inventory = tables.get("inventory", pd.DataFrame()).copy()
    marketing = tables.get("marketing", pd.DataFrame()).copy()
    reviews = tables.get("reviews", pd.DataFrame()).copy()

    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    orders["net_amount"] = orders["amount"] * (1 - orders.get("refund_flag", 0))
    order_product = orders.merge(products, on="product_id", how="left")
    order_product["gross_profit"] = (order_product["unit_price"] - order_product["cost"]) * order_product["quantity"]
    order_product["month"] = order_product["order_date"].dt.to_period("M").astype(str)

    total_gmv = float(order_product["amount"].sum())
    total_net_sales = float(order_product["net_amount"].sum())
    total_orders = int(order_product["order_id"].nunique())
    total_users = int(order_product["user_id"].nunique())
    refund_rate = float(order_product["refund_flag"].mean()) if "refund_flag" in order_product else 0.0
    avg_order_value = total_net_sales / total_orders if total_orders else 0.0
    gross_margin = float(order_product["gross_profit"].sum() / total_net_sales) if total_net_sales else 0.0

    kpis = {
        "gmv": round(total_gmv, 2),
        "net_sales": round(total_net_sales, 2),
        "orders": total_orders,
        "active_users": total_users,
        "avg_order_value": round(avg_order_value, 2),
        "refund_rate": round(refund_rate, 4),
        "gross_margin": round(gross_margin, 4),
    }

    monthly = (
        order_product.groupby("month", as_index=False)
        .agg(net_sales=("net_amount", "sum"), orders=("order_id", "nunique"), gross_profit=("gross_profit", "sum"))
        .sort_values("month")
    )
    monthly["avg_order_value"] = (monthly["net_sales"] / monthly["orders"]).round(2)

    category = (
        order_product.groupby("category", as_index=False)
        .agg(net_sales=("net_amount", "sum"), orders=("order_id", "nunique"), gross_profit=("gross_profit", "sum"))
        .sort_values("net_sales", ascending=False)
    )
    category["gross_margin"] = (category["gross_profit"] / category["net_sales"]).round(4)

    channel = (
        order_product.groupby("channel", as_index=False)
        .agg(net_sales=("net_amount", "sum"), orders=("order_id", "nunique"), users=("user_id", "nunique"))
        .sort_values("net_sales", ascending=False)
    )

    if not marketing.empty:
        marketing_sales = (
            marketing.groupby("channel", as_index=False)
            .agg(spend=("spend", "sum"), clicks=("clicks", "sum"), conversions=("conversions", "sum"))
        )
        channel = channel.merge(marketing_sales, on="channel", how="left")
        channel["roi"] = (channel["net_sales"] / channel["spend"].replace(0, pd.NA)).round(2)
        channel["conversion_rate"] = (channel["conversions"] / channel["clicks"].replace(0, pd.NA)).round(4)

    user_value = (
        order_product.groupby("user_id", as_index=False)
        .agg(net_sales=("net_amount", "sum"), orders=("order_id", "nunique"), last_order=("order_date", "max"))
    )
    user_value["avg_order_value"] = (user_value["net_sales"] / user_value["orders"]).round(2)
    user_value["segment"] = pd.cut(
        user_value["net_sales"],
        bins=[-0.01, user_value["net_sales"].quantile(0.5), user_value["net_sales"].quantile(0.85), float("inf")],
        labels=["normal", "valuable", "core"],
        duplicates="drop",
    )
    segment = (
        user_value.groupby("segment", observed=True, as_index=False)
        .agg(users=("user_id", "nunique"), net_sales=("net_sales", "sum"), avg_orders=("orders", "mean"))
    )

    inventory_risk = pd.DataFrame()
    if not inventory.empty:
        product_sales = order_product.groupby("product_id", as_index=False).agg(sold_qty=("quantity", "sum"))
        inventory_risk = inventory.merge(products[["product_id", "product_name", "category"]], on="product_id", how="left")
        inventory_risk = inventory_risk.merge(product_sales, on="product_id", how="left")
        inventory_risk["sold_qty"] = inventory_risk["sold_qty"].fillna(0)
        inventory_risk["stock_status"] = "normal"
        inventory_risk.loc[inventory_risk["stock"] < inventory_risk["safety_stock"], "stock_status"] = "shortage"
        inventory_risk.loc[(inventory_risk["stock"] > inventory_risk["sold_qty"] * 2) & (inventory_risk["stock"] > 120), "stock_status"] = "overstock"

    review_summary = pd.DataFrame()
    if not reviews.empty:
        review_summary = (
            reviews.groupby("rating", as_index=False)
            .agg(reviews=("review_id", "count"))
            .sort_values("rating")
        )

    return {
        "kpis": kpis,
        "monthly": monthly,
        "category": category,
        "channel": channel,
        "user_segment": segment,
        "top_users": user_value.sort_values("net_sales", ascending=False).head(20),
        "inventory_risk": inventory_risk,
        "review_summary": review_summary,
    }


def generate_insights(results: dict[str, pd.DataFrame | dict]) -> list[str]:
    kpis = results["kpis"]
    category = results["category"]
    channel = results["channel"]
    insights = []

    if isinstance(kpis, dict):
        insights.append(
            f"Net sales reached {kpis['net_sales']}, with {kpis['orders']} orders and "
            f"an average order value of {kpis['avg_order_value']}."
        )
        insights.append(
            f"Refund rate is {kpis['refund_rate']:.2%}; gross margin is {kpis['gross_margin']:.2%}."
        )

    if isinstance(category, pd.DataFrame) and not category.empty:
        top = category.iloc[0]
        insights.append(
            f"Top category by net sales is {top['category']}, contributing {round(float(top['net_sales']), 2)}."
        )

    if isinstance(channel, pd.DataFrame) and not channel.empty:
        top_channel = channel.iloc[0]
        insights.append(
            f"Best channel by net sales is {top_channel['channel']}, with {round(float(top_channel['net_sales']), 2)}."
        )

    return insights

