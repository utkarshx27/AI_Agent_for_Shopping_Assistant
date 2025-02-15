import pandas as pd
from datetime import datetime, timedelta



inventory_info = pd.read_csv(r"C:\Users\utkar\Downloads\agentic_ai\virtual_shopping_assistant\inventory_info.csv")
shipping_info = pd.read_csv(r"C:\Users\utkar\Downloads\agentic_ai\virtual_shopping_assistant\shipping_info.csv")
competitor_prices_info = pd.read_csv(r"C:\Users\utkar\Downloads\agentic_ai\virtual_shopping_assistant\competitor_prices_info.csv")
return_policies_info = pd.read_csv(r"C:\Users\utkar\Downloads\agentic_ai\virtual_shopping_assistant\return_policies_info.csv")


def search_products(df, name=None, color=None, min_price=None, max_price=None, size=None, brand=None):
    '''Search for products in the inventory based on filters like name, color, price range, size, and brand.'''
    
    try:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input data must be a pandas DataFrame.")

        required_columns = {"name", "color", "price", "size", "brand"}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns in DataFrame: {missing_columns}")

        filtered_df = df.copy()
        
        if name:
            if not isinstance(name, str):
                raise TypeError("Name must be a string.")
            filtered_df = filtered_df[filtered_df["name"].str.contains(name, case=False, na=False)]
        
        if color:
            if not isinstance(color, str):
                raise TypeError("Color must be a string.")
            filtered_df = filtered_df[filtered_df["color"].str.lower() == color.lower()]
        
        if min_price is not None:
            if not isinstance(min_price, (int, float)) or min_price < 0:
                raise ValueError("min_price must be a non-negative number.")
            filtered_df = filtered_df[filtered_df["price"] >= min_price]
        
        if max_price is not None:
            if not isinstance(max_price, (int, float)) or max_price < 0:
                raise ValueError("max_price must be a non-negative number.")
            filtered_df = filtered_df[filtered_df["price"] <= max_price]
        
        if size:
            if not isinstance(size, str):
                raise TypeError("Size must be a string.")
            filtered_df = filtered_df[filtered_df["size"].str.lower() == size.lower()]
        
        if brand:
            if not isinstance(brand, str):
                raise TypeError("Brand must be a string.")
            filtered_df = filtered_df[filtered_df["brand"].str.lower() == brand.lower()]
        
        columns_to_drop = [
            'discount_available', 'discounted_price', 'discount_percentage', 'discounted_coupon'
        ]
        
        filtered_df_new = filtered_df.drop(columns=[col for col in columns_to_drop if col in filtered_df.columns], errors='ignore')
        
        result = filtered_df_new.to_dict(orient="records")
        
        for item in result:
            for key, value in item.items():
                if pd.api.types.is_integer_dtype(type(value)):
                    item[key] = int(value)
                elif pd.api.types.is_float_dtype(type(value)):
                    item[key] = float(value)
        
        return result
    
    except Exception as e:
        return {"error": str(e)}


# Let's assume our warehouse is in Bangalore. We will calculate the estimated delivery date based on the shipping days to the given city + doorstep delivery time.
WAREHOUSE_LOCATION = "bangalore"
DOORSTEP_DELIVERY_DAYS = 1

def estimate_shipping(df, city, desired_date):
    '''Estimate the shipping cost and delivery date for a given city.'''
    try:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input data must be a pandas DataFrame.")
        
        if "city" not in df.columns or "shipping_days" not in df.columns or "shipping_cost" not in df.columns:
            raise ValueError("DataFrame must contain 'city', 'shipping_days', and 'shipping_cost' columns.")
        
        if not isinstance(city, str):
            raise TypeError("City must be a string.")
        
        if not isinstance(desired_date, str):
            raise TypeError("Desired date must be a string in YYYY-MM-DD format.")
        
        city = city.lower()
        
        if city not in df["city"].str.lower().values:
            return {"feasible": False, "message": "Shipping not available to this location."}
        
        shipping_info = df[df["city"].str.lower() == city].iloc[0]
        
        shipping_days = int(shipping_info["shipping_days"])  # Ensure it's a pure int
        shipping_cost = float(shipping_info["shipping_cost"])  # Ensure it's a pure float

        if shipping_days < 0:
            raise ValueError("Shipping days must be a non-negative number.")
        if shipping_cost < 0:
            raise ValueError("Shipping cost must be a non-negative number.")
        
        total_days = int(shipping_info["shipping_days"]) + DOORSTEP_DELIVERY_DAYS  
        estimated_delivery_date = datetime.today() + timedelta(days=total_days)
        
        desired_date = datetime.strptime(desired_date, "%Y-%m-%d")
        feasible = estimated_delivery_date <= desired_date
        
        return {
            "feasible": feasible,
            "estimated_delivery_date": estimated_delivery_date.strftime("%Y-%m-%d"),
            "shipping_cost": float(shipping_info["shipping_cost"])
        }
    
    except Exception as e:
        return {"error": str(e)}


def discount_checker(df, product_id):
    try:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input data must be a pandas DataFrame.")
        
        required_columns = {"product_id", "discount_available", "discounted_price", "discount_percentage", "discounted_coupon"}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns in DataFrame: {missing_columns}")
        
        if not isinstance(product_id, (int, str)):
            raise TypeError("Product ID must be an integer or string.")
        
        product_info = df[df["product_id"] == product_id]
        
        if product_info.empty:
            return {"error": "Product not found"}
        
        product_info = product_info.iloc[0]
        
        if not isinstance(product_info["discount_available"], str):
            raise ValueError("discount_available must be a string.")
        
        if product_info["discount_available"].lower() == "yes":
            return {
                "discount_status": True,
                "discounted_price": float(product_info["discounted_price"]),
                "discount_percentage": float(product_info["discount_percentage"]),
                "discounted_coupon": product_info["discounted_coupon"],
            }
        else:
            return {"discount_status": False}
    
    except Exception as e:
        return {"error": str(e)}
    

def price_comparison(df, product_name):
    try:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input data must be a pandas DataFrame.")
        
        required_columns = {"product_name", "store", "price", "discount_available", "discounted_price"}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns in DataFrame: {missing_columns}")
        
        if not isinstance(product_name, str):
            raise TypeError("Product name must be a string.")
        
        product_prices = df[df["product_name"].str.lower() == product_name.lower()]
        
        if product_prices.empty:
            return {"error": "Product not found in competitor stores"}
        
        return product_prices[["store", "price", "discount_available", "discounted_price"]].to_dict(orient="records")
    
    except Exception as e:
        return {"error": str(e)}


def return_policy_checker(df, store_name):
    policy_info = df[df["store"].str.lower() == store_name.lower()]
    
    if policy_info.empty:
        return {"error": "Return policy not found for this store"}

    policy_info = policy_info.iloc[0] 

    return {
        "store": policy_info["store"],
        "return_period": policy_info["return_period"],
        "return_conditions": policy_info["return_conditions"],
        "refund_method": policy_info["refund_method"]
    }


def discount_checker(df, product_id):
    try:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input data must be a pandas DataFrame.")
        
        required_columns = {"product_id", "discount_available", "discounted_price", "discount_percentage", "discounted_coupon"}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns in DataFrame: {missing_columns}")
        
        if not isinstance(product_id, (int, str)):
            raise TypeError("Product ID must be an integer or string.")
        
        product_info = df[df["product_id"] == product_id]
        
        if product_info.empty:
            return {"error": "Product not found"}
        
        product_info = product_info.iloc[0]  # Extract row as a Series
        
        if not isinstance(product_info["discount_available"], str):
            raise ValueError("discount_available must be a string.")
        
        if product_info["discount_available"].lower() == "yes":
            return {
                "discount_status": True,
                "discounted_price": float(product_info["discounted_price"]),
                "discount_percentage": float(product_info["discount_percentage"]),
                "discounted_coupon": product_info["discounted_coupon"],
            }
        else:
            return {"discount_status": False}
    
    except Exception as e:
        return {"error": str(e)}


def price_comparison(df, product_name):
    try:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input data must be a pandas DataFrame.")
        
        required_columns = {"product_name", "store", "price", "discount_available", "discounted_price"}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns in DataFrame: {missing_columns}")
        
        if not isinstance(product_name, str):
            raise TypeError("Product name must be a string.")
        
        product_prices = df[df["product_name"].str.lower() == product_name.lower()]
        
        if product_prices.empty:
            return {"error": "Product not found in competitor stores"}
        
        return product_prices[["store", "price", "discount_available", "discounted_price"]].to_dict(orient="records")
    
    except Exception as e:
        return {"error": str(e)}


def return_policy_checker(df, store_name):
    try:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input data must be a pandas DataFrame.")
        
        required_columns = {"store", "return_period", "return_conditions", "refund_method"}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns in DataFrame: {missing_columns}")
        
        if not isinstance(store_name, str):
            raise TypeError("Store name must be a string.")
        
        policy_info = df[df["store"].str.lower() == store_name.lower()]
        
        if policy_info.empty:
            return {"error": "Return policy not found for this store"}
        
        policy_info = policy_info.iloc[0]
        
        return {
            "store": policy_info["store"],
            "return_period": policy_info["return_period"],
            "return_conditions": policy_info["return_conditions"],
            "refund_method": policy_info["refund_method"]
        }
    
    except Exception as e:
        return {"error": str(e)}
