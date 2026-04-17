import requests
from serpapi import GoogleSearch
import os
import re


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

import re

def get_alternative_products(original_product, all_products):
    alternatives = []
    
    def clean_price(p_str):
        try: return float(re.sub(r'[^\d.]', '', str(p_str)))
        except: return 0.0

    orig_name = original_product.get('title', '').lower()
    orig_price = clean_price(original_product.get('price', 0))
    orig_rating = float(original_product.get('rating', 0) or 0)
    
    # Keyword extraction (First 2 words)
    keywords = orig_name.split()[:2] 

    for prod in all_products:
        if prod.get('product_id') == original_product.get('product_id'):
            continue

        p_name = prod.get('title', '').lower()
        p_price = clean_price(prod.get('price', 0))
        p_rating = float(prod.get('rating', 0) or 0)

        # Matching Logic: ±50% range rakhte hain testing ke liye
        is_match = any(word in p_name for word in keywords)
        within_range = (orig_price * 0.5) <= p_price <= (orig_price * 1.5)

        if is_match and within_range:
            tag, reason = "Similar Option", "Matching category"
            if p_price < orig_price:
                tag, reason = "Better Price", f"Sasta hai ₹{int(orig_price - p_price)}"
            elif p_rating > orig_rating:
                tag, reason = "Top Rated", "Better Rating"

            alternatives.append({
                "product_name": prod.get('title'),
                "price": p_price,
                "platform": prod.get('source'),
                "rating": p_rating,
                "tag": tag,
                "reason": reason
            })

    return sorted(alternatives, key=lambda x: x['price'])[:3]

def get_alternative_products(original_product, all_products):
    # Testing ke liye: Bas koi bhi 2 dusre products utha lo
    alts = [p for p in all_products if p.get('product_id') != original_product.get('product_id')]
    
    # Inhe "Better Option" ka tag de do
    results = []
    for a in alts[:2]:
        results.append({
            "tag": "Loot Deal",
            "product_name": a.get('title'),
            "price": a.get('price'),
            "platform": a.get('source'),
            "reason": "Sasta mil raha h!"
        })
    return results