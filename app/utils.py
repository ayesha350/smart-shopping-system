import requests
from serpapi import GoogleSearch

# SERP_API_KEY = "c940b4b25184b0761d498c855f6edda9209400df85885adc11a3a273edb57c85"

# def fetch_products(query, location="India"):
#     # Fallback data if API Key is missing or fails
#     fallback_data = [
#         {
#             "title": f"Premium {query}",
#             "source": "Amazon",
#             "price": "₹1,299",
#             "extracted_price": 1299,
#             "rating": 4.5,
#             "thumbnail": "https://via.placeholder.com/150",
#             "link": "#",
#             "delivery": "4-7 days",
#             "discount": "15%"
#         },
#         {
#             "title": f"Budget {query}",
#             "source": "Flipkart",
#             "price": "₹999",
#             "extracted_price": 999,
#             "rating": 4.2,
#             "thumbnail": "https://via.placeholder.com/150",
#             "link": "#",
#             "delivery": "2 days",
#             "discount": "25%"
#         }
#     ]

#     try:
#         search = GoogleSearch({
#             "q": query,
#             "engine": "google_shopping",
#             "location": location,
#             "api_key": SERP_API_KEY
#         })
#         results = search.get_dict()
#         shopping_results = results.get("shopping_results", [])
        
#         processed = []
#         for item in shopping_results:
#             # Simulation Logic for Delivery & Stock
#             price = item.get("extracted_price", 0)
#             rating = item.get("rating", 0)
            
#             # Smart Recommendation Logic
#             explanation = ""
#             if rating > 4.5 and price < 5000:
#                 explanation = "Highly recommended: Top-tier rating and great value."
#             elif price < 2000:
#                 explanation = "Budget pick: Lowest price in this category."
#             else:
#                 explanation = "Balanced choice based on user reviews."

#             processed.append({
#                 "title": item.get("title"),
#                 "source": item.get("source"),
#                 "price": item.get("price"),
#                 "extracted_price": price,
#                 "rating": rating,
#                 "thumbnail": item.get("thumbnail"),
#                 "link": item.get("link"),
#                 "delivery": "3-5 days", # Simulated
#                 "discount": "10% Off",  # Simulated
#                 "explanation": explanation,
#                 "best_deal": price < 1500,
#                 "fast_delivery": True
#             })
#         return processed if processed else fallback_data
#     except:
#         return fallback_data
# import os
# import requests
# from serpapi import GoogleSearch

# def fetch_products(query, location="India"):
#     # Using SerpApi for Google Shopping (Authentic Indian Results)
#     params = {
#         "engine": "google_shopping",
#         "q": query,
#         "location": location,
#         "hl": "en",
#         "gl": "in", # Forced to India
#         "curr": "INR", # Forced to Indian Rupee
#         "api_key": "c940b4b25184b0761d498c855f6edda9209400df85885adc11a3a273edb57c85" # Make sure your key is here
#     }

#     search = GoogleSearch(params)
#     results = search.get_dict()
#     shopping_results = results.get("shopping_results", [])

#     products = []
    
#     # List of authentic/trusted platforms in India
#     trusted_platforms = [
#         "Amazon.in", "Flipkart", "Myntra", "Ajio", "Nykaa", "Tata CLiQ", 
#         "Reliance Digital", "Croma", "BigBasket", "Blinkit", "Zepto"
#     ]
# import os
# import requests
# from serpapi import GoogleSearch

# def fetch_products(query, location="India"):
#     params = {
#         "engine": "google_shopping",
#         "q": query,
#         "location": location,
#         "hl": "en",
#         "gl": "in",
#         "curr": "INR",
#         "api_key": "YOUR_SERPAPI_KEY"
#     }

#     search = GoogleSearch(params)
#     results = search.get_dict()
#     shopping_results = results.get("shopping_results", [])

#     products = []
    
#     trusted_platforms = ["Amazon.in", "Flipkart", "Myntra", "Ajio", "Nykaa", "Tata CLiQ", "Reliance Digital", "Croma"]

#     for item in shopping_results:
#         # TAREKA 1: Sabse pehle direct link check karo
#         actual_link = item.get("link")
        
#         # TAREKA 2: Agar direct link nahi hai, toh SerpApi ka product_link lo
#         if not actual_link or actual_link == "None":
#             actual_link = item.get("product_link")
            
#         # TAREKA 3: Agar dono nahi hain, toh Google Shopping ka redirected link construct karo
#         if not actual_link:
#             continue # Is case mein product skip hoga kyunki bina link ke error aayega

#         source = item.get("source", "Official Store")
        
#         # Check if authentic
#         is_authentic = any(t in source.lower() for t in trusted_platforms) or ".in" in source.lower()

    
#         if is_authentic:
#             # Price Logic (Forcing ₹ symbol and INR values)
#             raw_price = item.get("price", "₹0")
#             if "$" in raw_price:
#                 # If API still sends $, we skip or convert (but gl:in usually fixes this)
#                 continue 
            
#             # Extract numbers for sorting
#             extracted_price = item.get("extracted_price", 0)

#             # Delivery Time Logic (Based on typical platform speeds)
#             source_lower = source.lower()
#             if any(fast in source_lower for fast in ["blinkit", "zepto", "bigbasket", "swiggy"]):
#                 delivery = "15-30 Minutes"
#                 fast_delivery = True
#             elif any(mid in source_lower for mid in ["amazon", "flipkart", "nykaa"]):
#                 delivery = "2-3 Days"
#                 fast_delivery = False
#             else:
#                 delivery = "4-7 Days"
#                 fast_delivery = False

#             # Discount Logic
#             # If the API provides old_price, we calculate real discount
#             discount = "10% Off" # Default
#             if "extensions" in item:
#                 for ext in item["extensions"]:
#                     if "% off" in ext.lower():
#                         discount = ext

            # products.append({
            #     "title": item.get("title"),
            #     "link": item.get("link"),
            #     "thumbnail": item.get("thumbnail"),
            #     "price": raw_price if "₹" in raw_price else f"₹{extracted_price}",
            #     "extracted_price": extracted_price,
            #     "source": source,
            #     "rating": item.get("rating", 4.2),
            #     "delivery": delivery,
            #     "fast_delivery": fast_delivery,
            #     "best_deal": True if item.get("rating", 0) >= 4.5 else False,
            #     "discount": discount,
            #     "json_data": "" # Will be populated in views.py
            # })

#     return products  


# import os
# from serpapi import GoogleSearch

# def fetch_products(query, location="India"):
#     params = {
#         "engine": "google_shopping",
#         "q": query,
#         "location": location,
#         "hl": "en",
#         "gl": "in",
#         "curr": "INR",
#         "api_key": "c940b4b25184b0761d498c855f6edda9209400df85885adc11a3a273edb57c85" # Apni key check kar lena yahan
#     }

#     try:
#         search = GoogleSearch(params)
#         results = search.get_dict()
#         shopping_results = results.get("shopping_results", [])
#     except Exception as e:
#         print(f"Error fetching data: {e}")
#         return []

#     products = []

#     for item in shopping_results:
#         # 1. LINK FIX: Sabse pehle link check karo
#         # Agar 'link' nahi hai toh 'product_link' lo, agar wo bhi nahi toh skip.
#         actual_link = item.get("link") or item.get("product_link")
        
#         if not actual_link:
#             continue

#         # 2. SOURCE/BRAND: 
#         source = item.get("source", "Online Store")
        
#         # Filtering ko relax kar diya hai taaki "Lakme" ya koi bhi brand search ho sake
#         # Bas hum check kar rahe hain ki results empty na chale jayen
#         products.append({
#             "title": item.get("title"),
#             "link": item.get("link"),
#             "thumbnail": item.get("thumbnail"),
#             "price": raw_price if "₹" in raw_price else f"₹{extracted_price}",
#             "extracted_price": extracted_price,
#             "source": source,
#             "rating": item.get("rating", 4.2),
#             "delivery": delivery,
#             "fast_delivery": fast_delivery,
#             "best_deal": True if item.get("rating", 0) >= 4.5 else False,
#             "discount": discount,
#             "json_data": "" # Will be populated in views.py
#         })

#     return products

# import os
# import re
# from serpapi import GoogleSearch

# def fetch_products(query, location="India"):
#     params = {
#         "engine": "google_shopping",
#         "q": query,
#         "location": location,
#         "hl": "en",
#         "gl": "in",
#         "curr": "INR",
#         "api_key": "c940b4b25184b0761d498c855f6edda9209400df85885adc11a3a273edb57c85" 
#     }

#     try:
#         search = GoogleSearch(params)
#         results = search.get_dict()
#         shopping_results = results.get("shopping_results", [])
#     except Exception as e:
#         print(f"Error fetching data: {e}")
#         return []

#     products = []

#     for item in shopping_results:
#         # 1. LINK FIX
#         actual_link = item.get("link") or item.get("product_link")
#         if not actual_link:
#             continue

#         # 2. VARIABLE EXTRACTION (Defining missing variables)
#         source = item.get("source", "Online Store")
        
#         # Price logic
#         raw_price = item.get("price", "Check Price")
#         # Extracting numeric price for 'extracted_price'
#         extracted_price = item.get("extracted_price") or 0
#         if not extracted_price and "₹" in raw_price:
#              # Fallback: extract number from string if extracted_price is missing
#              nums = re.findall(r'\d+', raw_price.replace(',', ''))
#              extracted_price = int(nums[0]) if nums else 0

#         # Delivery logic (Original fetch)
#         delivery = item.get("delivery", "Fast Shipping")
#         fast_delivery = "free" in delivery.lower() or "today" in delivery.lower() or "tomorrow" in delivery.lower()

#         # Discount logic from extensions
#         extensions = item.get("extensions", [])
#         discount = extensions[0] if extensions else "Special Price"

#         # 3. APPENDING
#         products.append({
#             "title": item.get("title"),
#             "link": actual_link, 
#             "thumbnail": item.get("thumbnail"),
#             "price": raw_price if "₹" in str(raw_price) else f"₹{raw_price}",
#             "extracted_price": extracted_price,
#             "source": source,
#             "rating": item.get("rating", 4.2),
#             "delivery": delivery,
#             "fast_delivery": fast_delivery,
#             "best_deal": True if item.get("rating", 0) >= 4.5 else False,
#             "discount": discount,
#             "json_data": "" 
#         })

#     return products


# import os
# import re
# from serpapi import GoogleSearch

# def fetch_products(query, location="India", sort_by="relevance"):
#     params = {
#         "engine": "google_shopping",
#         "q": query,
#         "location": location,
#         "hl": "en",
#         "gl": "in",
#         "curr": "INR",
#         "api_key": "c940b4b25184b0761d498c855f6edda9209400df85885adc11a3a273edb57c85" 
#     }

#     try:
#         search = GoogleSearch(params)
#         results = search.get_dict()
#         shopping_results = results.get("shopping_results", [])
#     except Exception as e:
#         return []

#     products = []
    
#     # --- [STRICT: FILTERING CONFIGURATION] ---
#     SUSPICIOUS_SUFFIXES = ['.xyz', '.pw', '.site', '.online', '.icu', '.top', '.info', '.biz']
#     UNTRUSTED_KEYWORDS = ['cheap', 'dealz', 'discount-store', 'free-offers', 'hot-price']

#     for item in shopping_results:
#         # 1. SOURCE & LINK VALIDATION
#         source = item.get("source", "").lower()
#         actual_link = (item.get("link") or item.get("product_link", "")).lower()
#         title = item.get("title", "").lower()

#         if not actual_link:
#             continue

#         # --- [STRICT: ADDING FILTERING LOGIC ONLY] ---
#         # Block suspicious domains
#         if any(actual_link.endswith(suffix) or f"{suffix}/" in actual_link for suffix in SUSPICIOUS_SUFFIXES):
#             continue
            
#         # Block untrusted keywords (unless it's a known big platform)
#         if any(word in source or word in actual_link for word in UNTRUSTED_KEYWORDS):
#             if not any(trusted in source for trusted in ['amazon', 'flipkart', 'myntra', 'nykaa', 'ajio', 'tata']):
#                 continue
        
#         # --- [TASK: CLEAN DELIVERY TIME LOGIC] ---
        
#         # 1. Start by checking if API provides a raw timing (like "Tomorrow" or "2 days")
#         api_delivery = item.get("delivery", "").lower()
        
#         # 2. If API text is just an offer (contains "free", "₹", "order"), we IGNORE it
#         # and generate a clean estimate instead.
#         if not api_delivery or any(x in api_delivery for x in ["₹", "free", "order", "spend", "above"]):
#             # CATEGORY & PLATFORM BASED ESTIMATION
#             if any(q in source for q in ["zepto", "blinkit", "swiggy", "instamart", "bigbasket"]):
#                 delivery_time = "15-30 minutes"
#             elif any(cat in title for cat in ["milk", "bread", "grocery", "snack", "egg"]):
#                 delivery_time = "10-20 minutes"
#             elif any(cat in title for cat in ["shirt", "dress", "saree", "jeans", "top", "kurti"]):
#                 delivery_time = "3-7 days"
#             elif any(cat in title for cat in ["lipstick", "makeup", "cream", "serum", "shampoo"]):
#                 delivery_time = "2-5 days"
#             elif any(cat in title for cat in ["mobile", "laptop", "watch", "iphone", "electronics"]):
#                 delivery_time = "2-4 days"
#             else:
#                 delivery_time = "4-7 days"
#         else:
#             # If the API actually gave a time like "2 days", we clean the text
#             delivery_time = api_delivery.replace("delivery by", "").replace("shipping", "").strip()

#         # 3. Final Format: Always "Delivers in X"
#         final_delivery_text = f"Delivers in {delivery_time}"

#         # --- [STRICT: UPDATE ONLY THE DELIVERY FIELD] ---
# # --- [STRICT: ENSURE ALL KEYS EXIST FOR SORTING] ---
#         # Price se numbers nikalne ke liye logic (e.g., "₹1,200" -> 1200)
#         # raw_price = item.get("price", "0")
#         # extracted_price = int(re.sub(r'[^\d]', '', raw_price)) if any(char.isdigit() for char in raw_price) else 0
#         # # 1. REAL DISCOUNT CALCULATION

        
#         current_p_str = str(item.get("price", "0"))
#         current_p = float(re.sub(r'[^\d.]', '', current_p_str)) if any(c.isdigit() for c in current_p_str) else 0
        
#         original_p_raw = item.get("old_price") or item.get("mrp")
#         if original_p_raw:
#             old_p = float(re.sub(r'[^\d.]', '', str(original_p_raw)))
#             calc_disc = int(((old_p - current_p) / old_p) * 100)
#             final_discount = f"{calc_disc}% OFF" if calc_disc > 0 else "Best Price"
#         else:
#             # Extension se % uthao agar MRP nahi hai
#             final_discount = next((ext for ext in item.get("extensions", []) if "%" in ext), "0% OFF")

#         # 2. EXTRACTED PRICE FOR SORTING
#         extracted_price = current_p
#         products.append({
#             "title": item.get("title"),
#             "link": actual_link,
#             "thumbnail": item.get("thumbnail"),
#             "price": current_p_str,
#             "extracted_price": extracted_price, # <-- Sorting ke liye zaroori
#             "source": item.get("source", "Store"),
#             "rating": float(item.get("rating", 0)), # <-- Float mein convert karein
#             "delivery": final_delivery_text, 
#             "discount": final_discount,
#             "json_data": "" 
#         })
#     def get_delivery_priority(text):
#         text = text.lower()
#         # Extracts numbers for comparison
#         nums = re.findall(r'\d+', text)
#         val = int(nums[0]) if nums else 999
        
#         if 'min' in text: return val
#         if 'hour' in text: return val * 60
#         if 'day' in text: return val * 1440
#         return 9999

#     def get_discount_value(text):
#         nums = re.findall(r'\d+', text)
#         return int(nums[0]) if nums else 0

#     if sort_by == "price":
#         products.sort(key=lambda x: x['extracted_price'] if x['extracted_price'] > 0 else 999999)
    
#     elif sort_by == "discount":
#         products.sort(key=lambda x: get_discount_value(x['discount']), reverse=True)
    
#     elif sort_by == "delivery":
#         products.sort(key=lambda x: get_delivery_priority(x['delivery']))
    
#     elif sort_by == "rating":
#         products.sort(key=lambda x: x['rating'], reverse=True)
    
#     elif sort_by == "relevance":
#         # RELEVANCE LOGIC: Higher Rating (multiplied) / Price
#         # Isse high rating aur kam price wale upar aayenge
#         products.sort(key=lambda x: (float(x['rating']) * 1000) / (x['extracted_price'] if x['extracted_price'] > 0 else 1), reverse=True)

#     return products    
    


# import os
# import re
# from serpapi import GoogleSearch

# def fetch_products(query, location="India", sort_by="relevance"):
#     params = {
#         "engine": "google_shopping",
#         "q": query,
#         "location": location,
#         "hl": "en",
#         "gl": "in",
#         "curr": "INR",
#         "api_key": "c940b4b25184b0761d498c855f6edda9209400df85885adc11a3a273edb57c85" 
#     }

#     try:
#         search = GoogleSearch(params)
#         results = search.get_dict()
#         shopping_results = results.get("shopping_results", [])
#     except Exception as e:
#         return []

#     products = []
    
#     SUSPICIOUS_SUFFIXES = ['.xyz', '.pw', '.site', '.online', '.icu', '.top', '.info', '.biz']
#     UNTRUSTED_KEYWORDS = ['cheap', 'dealz', 'discount-store', 'free-offers', 'hot-price']

#     for item in shopping_results:
#         source = item.get("source", "").lower()
#         actual_link = (item.get("link") or item.get("product_link", "")).lower()
#         title = item.get("title", "").lower()

#         if not actual_link:
#             continue

#         if any(actual_link.endswith(suffix) or f"{suffix}/" in actual_link for suffix in SUSPICIOUS_SUFFIXES):
#             continue
            
#         if any(word in source or word in actual_link for word in UNTRUSTED_KEYWORDS):
#             if not any(trusted in source for trusted in ['amazon', 'flipkart', 'myntra', 'nykaa', 'ajio', 'tata']):
#                 continue
        
#         # --- DELIVERY TIME LOGIC ---
#         api_delivery = item.get("delivery", "").lower()
#         if not api_delivery or any(x in api_delivery for x in ["₹", "free", "order", "spend", "above"]):
#             if any(q in source for q in ["zepto", "blinkit", "swiggy", "instamart", "bigbasket"]):
#                 delivery_time = "15-30 minutes"
#             elif any(cat in title for cat in ["milk", "bread", "grocery", "snack", "egg"]):
#                 delivery_time = "10-20 minutes"
#             elif any(cat in title for cat in ["shirt", "dress", "saree", "jeans", "top", "kurti"]):
#                 delivery_time = "3-7 days"
#             elif any(cat in title for cat in ["lipstick", "makeup", "cream", "serum", "shampoo"]):
#                 delivery_time = "2-5 days"
#             elif any(cat in title for cat in ["mobile", "laptop", "watch", "iphone", "electronics"]):
#                 delivery_time = "2-4 days"
#             else:
#                 delivery_time = "4-7 days"
#         else:
#             delivery_time = api_delivery.replace("delivery by", "").replace("shipping", "").strip()

#         final_delivery_text = f"Delivers in {delivery_time}"

#         # --- PRICE LOGIC (FIXED HERE: re.sub instead of re.sum) ---
#         current_p_str = str(item.get("price", "0"))
#         # FIXED: re.sub is correct
#         current_p = float(re.sub(r'[^\d.]', '', current_p_str)) if any(c.isdigit() for c in current_p_str) else 0
        
#         original_p_raw = item.get("old_price") or item.get("mrp")
#         if original_p_raw:
#             old_p = float(re.sub(r'[^\d.]', '', str(original_p_raw)))
#             calc_disc = int(((old_p - current_p) / old_p) * 100) if old_p > 0 else 0
#             final_discount = f"{calc_disc}% OFF" if calc_disc > 0 else "Best Price"
#         else:
#             final_discount = next((ext for ext in item.get("extensions", []) if "%" in ext), "0% OFF")

#         products.append({
#             "title": item.get("title"),
#             "link": actual_link,
#             "thumbnail": item.get("thumbnail"),
#             "price": current_p_str,
#             "extracted_price": current_p,
#             "source": item.get("source", "Store"),
#             "rating": float(item.get("rating", 0)),
#             "delivery": final_delivery_text, 
#             "discount": final_discount,
#             "json_data": "" 
#         })

#     # --- SORTING LOGIC ---
#     def get_delivery_priority(text):
#         text = text.lower()
#         nums = re.findall(r'\d+', text)
#         val = int(nums[0]) if nums else 999
#         if 'min' in text: return val
#         if 'hour' in text: return val * 60
#         if 'day' in text: return val * 1440
#         return 9999

#     def get_discount_value(text):
#         nums = re.findall(r'\d+', text)
#         return int(nums[0]) if nums else 0

#     if sort_by == "price":
#         products.sort(key=lambda x: x['extracted_price'] if x['extracted_price'] > 0 else 999999)
#     elif sort_by == "discount":
#         products.sort(key=lambda x: get_discount_value(x['discount']), reverse=True)
#     elif sort_by == "delivery":
#         products.sort(key=lambda x: get_delivery_priority(x['delivery']))
#     elif sort_by == "rating":
#         products.sort(key=lambda x: x['rating'], reverse=True)
#     elif sort_by == "relevance":
#         products.sort(key=lambda x: (float(x['rating']) * 1000) / (x['extracted_price'] if x['extracted_price'] > 0 else 1), reverse=True)

#     return products 

# # SAFELY ADDED AT THE END - No effect on fetch_products
# def optimize_cart(cart_items):
#     optimized_items = []
#     total_original = 0
#     total_optimized = 0

#     for item in cart_items:
#         title = item.product_data.get('title', '')
#         price_str = str(item.product_data.get('price', '0'))
#         price = float(re.sub(r'[^\d.]', '', price_str)) if any(c.isdigit() for c in price_str) else 0
#         source = item.product_data.get('source', 'Unknown')

#         optimized_items.append({
#             'product_name': title,
#             'best_platform': source,
#             'price': price
#         })
#         total_original += price
#         total_optimized += price

#     return {
#         'optimized_items': optimized_items,
#         'optimized_total': f"{total_optimized:,.2f}",
#         'total_savings': 0,
#         'is_optimized': False,
#         'opt_label': "Standard Order"
#     }


import os
import re
from serpapi import GoogleSearch

def fetch_products(query, location="India", sort_by="relevance"):
    params = {
        "engine": "google_shopping",
        "q": query,
        "location": location,
        "hl": "en",
        "gl": "in",
        "curr": "INR",
        "api_key": "c940b4b25184b0761d498c855f6edda9209400df85885adc11a3a273edb57c85" 
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        shopping_results = results.get("shopping_results", [])
    except Exception as e:
        return []

    products = []
    
    SUSPICIOUS_SUFFIXES = ['.xyz', '.pw', '.site', '.online', '.icu', '.top', '.info', '.biz']
    UNTRUSTED_KEYWORDS = ['cheap', 'dealz', 'discount-store', 'free-offers', 'hot-price']

    for item in shopping_results:
        source = item.get("source", "").lower()
        actual_link = (item.get("link") or item.get("product_link", "")).lower()
        title = item.get("title", "").lower()

        if not actual_link:
            continue

        if any(actual_link.endswith(suffix) or f"{suffix}/" in actual_link for suffix in SUSPICIOUS_SUFFIXES):
            continue
            
        if any(word in source or word in actual_link for word in UNTRUSTED_KEYWORDS):
            if not any(trusted in source for trusted in ['amazon', 'flipkart', 'myntra', 'nykaa', 'ajio', 'tata']):
                continue
        
        # --- DELIVERY TIME LOGIC ---
        api_delivery = item.get("delivery", "").lower()
        if not api_delivery or any(x in api_delivery for x in ["₹", "free", "order", "spend", "above"]):
            if any(q in source for q in ["zepto", "blinkit", "swiggy", "instamart", "bigbasket"]):
                delivery_time = "15-30 minutes"
            elif any(cat in title for cat in ["milk", "bread", "grocery", "snack", "egg"]):
                delivery_time = "10-20 minutes"
            elif any(cat in title for cat in ["shirt", "dress", "saree", "jeans", "top", "kurti"]):
                delivery_time = "3-7 days"
            elif any(cat in title for cat in ["lipstick", "makeup", "cream", "serum", "shampoo"]):
                delivery_time = "2-5 days"
            elif any(cat in title for cat in ["mobile", "laptop", "watch", "iphone", "electronics"]):
                delivery_time = "2-4 days"
            else:
                delivery_time = "4-7 days"
        else:
            delivery_time = api_delivery.replace("delivery by", "").replace("shipping", "").strip()

        final_delivery_text = f"Delivers in {delivery_time}"

        # --- PRICE LOGIC ---
        current_p_str = str(item.get("price", "0"))
        current_p = float(re.sub(r'[^\d.]', '', current_p_str)) if any(c.isdigit() for c in current_p_str) else 0
        
        original_p_raw = item.get("old_price") or item.get("mrp")
        if original_p_raw:
            old_p = float(re.sub(r'[^\d.]', '', str(original_p_raw)))
            calc_disc = int(((old_p - current_p) / old_p) * 100) if old_p > 0 else 0
            final_discount = f"{calc_disc}% OFF" if calc_disc > 0 else "Best Price"
        else:
            final_discount = next((ext for ext in item.get("extensions", []) if "%" in ext), "0% OFF")

        products.append({
            "title": item.get("title"),
            "link": actual_link,
            "thumbnail": item.get("thumbnail"),
            "price": current_p_str,
            "extracted_price": current_p,
            "source": item.get("source", "Store"),
            "rating": float(item.get("rating", 0)),
            "delivery": final_delivery_text, 
            "discount": final_discount,
            "json_data": "" 
        })

    # --- SORTING LOGIC ---
    def get_delivery_priority(text):
        text = text.lower()
        nums = re.findall(r'\d+', text)
        val = int(nums[0]) if nums else 999
        if 'min' in text: return val
        if 'hour' in text: return val * 60
        if 'day' in text: return val * 1440
        return 9999

    def get_discount_value(text):
        nums = re.findall(r'\d+', text)
        return int(nums[0]) if nums else 0

    if sort_by == "price":
        products.sort(key=lambda x: x['extracted_price'] if x['extracted_price'] > 0 else 999999)
    elif sort_by == "discount":
        products.sort(key=lambda x: get_discount_value(x['discount']), reverse=True)
    elif sort_by == "delivery":
        products.sort(key=lambda x: get_delivery_priority(x['delivery']))
    elif sort_by == "rating":
        products.sort(key=lambda x: x['rating'], reverse=True)
    elif sort_by == "relevance":
        products.sort(key=lambda x: (float(x['rating']) * 1000) / (x['extracted_price'] if x['extracted_price'] > 0 else 1), reverse=True)

    return products 

# --- KEEPING ORIGINAL optimize_cart EXACTLY AS IT WAS ---
def optimize_cart(cart_items):
    optimized_items = []
    total_original = 0
    total_optimized = 0

    for item in cart_items:
        title = item.product_data.get('title', '')
        price_str = str(item.product_data.get('price', '0'))
        price = float(re.sub(r'[^\d.]', '', price_str)) if any(c.isdigit() for c in price_str) else 0
        source = item.product_data.get('source', 'Unknown')

        optimized_items.append({
            'product_name': title,
            'best_platform': source,
            'price': price
        })
        total_original += price
        total_optimized += price

    return {
        'optimized_items': optimized_items,
        'optimized_total': f"{total_optimized:,.2f}",
        'total_savings': 0,
        'is_optimized': False,
        'opt_label': "Standard Order"
    }

# --- 🚀 NEW SAFE EXTENSION: get_optimized_cart_v2 ---
def get_optimized_cart_v2(cart_items):
    import re
    grouped_data = {}
    original_total = 0

    for item in cart_items:
        data = item.product_data
        p_str = str(data.get('price', '0'))
        price = float(re.sub(r'[^\d.]', '', p_str)) if any(c.isdigit() for c in p_str) else 0.0
        
        # --- SMART LOGIC: Sirf pehle 15 letters match karo (Peanuts etc.) ---
        full_name = data.get('title', 'Unknown Product').strip()
        match_name = full_name.lower()[:15] 
        
        source = data.get('source', 'Unknown')
        qty = getattr(item, 'quantity', 1)
        original_total += (price * qty)

        # Agar match_name (shuruat ka naam) milta hai, toh sasta wala rakho
        if match_name not in grouped_data:
            grouped_data[match_name] = {
                'display_name': full_name, # Original naam dikhane ke liye
                'best_platform': source,
                'price': price,
                'qty': qty
            }
        else:
            if price < grouped_data[match_name]['price']:
                grouped_data[match_name]['price'] = price
                grouped_data[match_name]['best_platform'] = source

    optimized_items = []
    for m_name, info in grouped_data.items():
        optimized_items.append({
            'product_name': info['display_name'],
            'best_platform': info['best_platform'],
            'price': info['price'],
            'qty': info['qty']
        })

    optimized_total_val = sum(i['price'] * i['qty'] for i in optimized_items)
    savings = original_total - optimized_total_val

    return {
        "optimized": savings > 1, # ₹1 se zyada bachat ho tabhi dikhao
        "optimized_items": optimized_items,
        "optimized_total": f"{optimized_total_val:,.2f}",
        "savings": int(savings)
    }