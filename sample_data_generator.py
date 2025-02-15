import pandas as pd

shipping_data = {
    'city': ['lucknow', 'delhi', 'mumbai'],
    'shipping_days': [4, 3, 2],
    'shipping_cost': [1.99, 1.49, 1.29],
}

shipping_info = pd.DataFrame(shipping_data)
shipping_info.to_csv('shipping_info.csv', index=False)

inventry_data = {
    'product_id': [0, 1, 2, 3, 4],
    'name': ['floral skirt', 'socks', 'sneakers', 'casual denim jacket', 'cocktail dress'],
    'color': ['orange', 'white', 'white', 'navy blue', 'red'],
    'price': [30, 4.99, 60, 80, 50],
    'size': ['s', 'm', 'Size 8', 'l', 'm'],
    'type': ['skirt', 'accessories', 'shoes', 'jacket', 'cocktail dress'],
    'brand': ['acb', 'xyz', 'Nike', 'Roadster', 'xyz'],
    'discount_available': ['yes', 'no', 'no', 'no', 'no'],
    'discounted_price': [27, 0, 0, 0, 0],
    'discount_percentage': [10, 0, 0, 0, 0],
    'discounted_coupon': ['SAVE10', 'null', 'null', 'null', 'null'],
    'store': ['SiteA', 'SiteA', 'SiteB', 'SiteB', 'SiteB']
    
 }

inventory_info = pd.DataFrame(inventry_data)
inventory_info.to_csv('inventory_info.csv', index=False)

competitor_prices_info = pd.DataFrame({
    "product_id": [0, 0, 1, 1, 3, 3, 3],
    "product_name": ["floral skirt", "floral skirt", "socks", "socks", "casual denim jacket", "casual denim jacket", "casual denim jacket"],
    "store": ["Amazon", "Flipkart", "Amazon", "Myntra", "aJio", "TheSouledStore", "Myntra"],
    "price": [38.99, 20, 3.10, 2.80, 60, 80, 65],
    "discount_available": ["yes", "yes", "no", "yes", "no", "yes", "yes"],
    'discount_percentage': [5, 5, 0, 50, 0, 10, 20],
    "discounted_price": [35.99, 18.99, 3.10, 1.40, 60, 72, 52]
})
competitor_prices_info.to_csv('competitor_prices_info.csv', index=False)

return_policies_info = pd.DataFrame({
    "store": ["Amazon", "Flipkart", "Myntra", "SiteA", "SiteB", "aJio"],
    "return_period": ["30 days", "10 days", "15 days",  "10 days",  "10 days",  "5 days"],
    "return_conditions": [
        "Items must be in original condition with tags.",
        "Only defective/damaged products are returnable",
        "No returns on discounted items",
        "Items must be in original condition with tags",
        "Only defective/damaged products are returnable",
        "No returns on discounted items"
    ],
    "refund_method": ["Original payment method", "Store credit or refund", "Store credit only", "Original payment method", "Store credit or refund", "Store credit only"]
})

return_policies_info.to_csv('return_policies_info.csv', index=False)