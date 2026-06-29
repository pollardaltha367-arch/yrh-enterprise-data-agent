# Data Contract

This project is designed for retail/e-commerce style enterprise analysis.

## Minimum Required Tables

The pipeline requires at least:

```text
orders.csv
products.csv
```

## orders.csv

| Field | Meaning | Required |
| --- | --- | --- |
| order_id | Unique order id | yes |
| user_id | User id | yes |
| product_id | Product id | yes |
| order_date | Order date | yes |
| channel | Sales channel | yes |
| quantity | Purchased quantity | yes |
| unit_price | Unit selling price | yes |
| discount_rate | Discount rate | recommended |
| refund_flag | 1 if refunded, 0 otherwise | recommended |
| amount | Order amount | yes |

## products.csv

| Field | Meaning | Required |
| --- | --- | --- |
| product_id | Product id | yes |
| product_name | Product name | yes |
| category | Product category | yes |
| brand | Product brand | optional |
| cost | Unit cost | yes |
| price | Listed price | yes |

## Optional Tables

### users.csv

```text
user_id,city,age_group,register_date,source
```

### inventory.csv

```text
product_id,stock,safety_stock,warehouse
```

### marketing.csv

```text
date,channel,campaign,spend,clicks,conversions
```

### reviews.csv

```text
review_id,order_id,rating,comment,review_date
```

## If Your Dataset Is Different

Before running the pipeline, map your fields to this contract.

Example:

| Your field | Contract field |
| --- | --- |
| sku_id | product_id |
| pay_time | order_date |
| sales_amt | amount |
| platform | channel |

The first version is intentionally strict. Later versions can add automatic field mapping.

