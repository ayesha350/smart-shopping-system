from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import fetch_products
from .models import PriceAlert
import json
from .utils import optimize_cart
from .models import PriceAlert, Wishlist
from .models import CartItem
import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem
import re
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CartItem
# Purane imports ke saath naya function add karein
from .utils import fetch_products, optimize_cart, get_optimized_cart_v2

# HOME 
def home(request):
    categories = ['Food', 'Medicine', 'Clothes', 'Beauty', 'Shoes', 'Jwellery', 'Grocery', 'Electronics', 'General Products']
    location = request.session.get('location', 'India')
    
    # Fetching real products with INR focus
    all_deals = fetch_products("top deals", location=location)
    
    for item in all_deals:
        # Serializing the clean data for Wishlist/Cart
        item['json_data'] = json.dumps(item)
        
    # Showing high-rated authentic deals
    best_deals = [item for item in all_deals if item.get('rating', 0) >= 4.2][:6]
    
    return render(request, 'index.html', {
        'categories': categories, 
        'best_deals': best_deals,
        'location': location,
        'recent': request.session.get('recent_searches', [])
    })


def home(request):
    categories = ['Food', 'Medicine', 'Clothes', 'Beauty', 'Shoes', 'Jwellery', 'Grocery', 'Electronics', 'General Products']
    location = request.session.get('location', 'India')
    
    # Fetching real products with INR focus
    all_deals = fetch_products("top deals", location=location)
    
    # --- 🚀 NEW: ALTERNATIVES LOGIC START ---
    # Har deal ke liye uske saste aur behtar options dhoondhein
    if all_deals:
        for item in all_deals:
            # Hum 'all_deals' ko hi as a database use kar rahe hain comparison ke liye
            item['alternatives'] = get_alternative_products(item, all_deals)
    # --- NEW: ALTERNATIVES LOGIC END ---

    for item in all_deals:
        # Serializing the clean data for Wishlist/Cart
        # Isme ab 'alternatives' bhi include ho chuka hai
        item['json_data'] = json.dumps(item)
        
    # Showing high-rated authentic deals
    best_deals = [item for item in all_deals if item.get('rating', 0) >= 4.2][:6]
    
    return render(request, 'index.html', {
        'categories': categories, 
        'best_deals': best_deals,
        'location': location,
        'recent': request.session.get('recent_searches', [])
    })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def set_location(request):
    """
    User ki location (pincode ya coordinates) ko session mein save karne ke liye.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pincode = data.get('pincode')
            lat = data.get('lat')
            lng = data.get('lng')

            # 1. Agar Pincode manually dala gaya hai
            if pincode:
                request.session['user_pincode'] = pincode
                request.session['location_method'] = 'manual'
                return JsonResponse({"status": "success", "message": f"Location set to {pincode}"})

            # 2. Agar Geolocation use ki gayi hai
            elif lat and lng:
                # Yahan aap koi Reverse Geocoding API call kar sakte hain.
                # Abhi ke liye hum coordinates save kar rahe hain aur dummy pincode de rahe hain.
                request.session['user_pincode'] = "Detected" 
                request.session['user_lat'] = lat
                request.session['user_lng'] = lng
                request.session['location_method'] = 'gps'
                return JsonResponse({"status": "success", "message": "GPS Location saved"})

            return JsonResponse({"status": "error", "message": "Invalid data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)



def add_to_cart(request):
    if request.method == "POST":
        product_json = request.POST.get('product_data')
        product_data = json.loads(product_json)
        
        cart = request.session.get('cart', [])
        cart.append(product_data)
        request.session['cart'] = cart
        messages.success(request, "Product added to comparison cart!")
    return redirect('cart')

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    if request.method == "POST":
        # Database se wahi item dhoondo jo us user ka ho aur jiski ID match kare
        item = get_object_or_404(CartItem, id=item_id, user=request.user)
        item.delete()
    return redirect('cart')

     


  

@login_required(login_url='login')
def view_cart(request):
    # --- 1. EXISTING LOGIC: Database & Session Fetching ---
    cart_items = CartItem.objects.filter(user=request.user).order_by('-added_at')
    session_cart = request.session.get('cart', [])
    
    comparison = ""
    total_price = 0

    def clean_price(price_str):
        try:
            return float(re.sub(r'[^\d.]', '', str(price_str)))
        except: return 0.0

    # --- 2. EXISTING LOGIC: Total Price Calculation ---
    if cart_items.exists():
        for item in cart_items:
            price = clean_price(item.product_data.get('price', 0))
            total_price += (price * item.quantity)

        # --- 3. EXISTING LOGIC: Comparison Logic (Database Items) ---
        if cart_items.count() >= 2:
            item_list = []
            for item in cart_items:
                p_val = clean_price(item.product_data.get('price', 0))
                item_list.append({
                    'title': item.product_data.get('title', 'Product'),
                    'price': p_val,
                    'source': item.product_data.get('source', 'Unknown')
                })
            
            sorted_items = sorted(item_list, key=lambda x: x['price'])
            cheapest, next_best = sorted_items[0], sorted_items[1]
            diff = next_best['price'] - cheapest['price']
            
            if diff > 0:
                comparison = f"Decision Made: '{cheapest['title'][:30]}...' is the winner! It's ₹{int(diff)} cheaper. We recommend {cheapest['source']}."
            else:
                comparison = "Multiple products have the same lowest price."

    # --- 4. EXISTING FEATURE: Multi-App Cart Optimization (Manual Logic) ---
    optimized_total_manual = 0
    recommendations_manual = []
    
    for item in cart_items:
        price = clean_price(item.product_data.get('price', 0))
        best_price = price 
        optimized_total_manual += best_price
        recommendations_manual.append({
            'title': item.product_data.get('title'),
            'platform': item.product_data.get('source'),
            'price': best_price
        })

    total_savings_manual = total_price - optimized_total_manual

    # --- 🚀 NEW INTEGRATION: Advanced Multi-App Optimization ---
    # Purane logic ko bina disturb kiye naye logic call yahan hain
    optimization_data = optimize_cart(cart_items)
    smart_logic = get_optimized_cart_v2(cart_items) 

    # --- 5. RENDER CONTEXT (Combining All Features & New Integration) ---
    context = {
        'cart_items': cart_items,
        'cart': session_cart,
        'total_price': f"{total_price:,.2f}",
        'comparison': comparison,
        
        'optimized_recommendations': recommendations_manual,
        'optimized_total_manual': f"{optimized_total_manual:,.2f}",
        'total_savings_manual': int(total_savings_manual),

        'optimized_items': optimization_data['optimized_items'],
        'optimized_total': optimization_data['optimized_total'],
        'total_savings': optimization_data['savings'],
        'is_optimized': optimization_data['optimized'],
        'opt_label': optimization_data['label'],

        # Smart Logic Data (Safe Integration)
        'smart_optimized_items': smart_logic['optimized_items'],
        'smart_optimized_total': smart_logic['optimized_total'],
        'smart_savings': smart_logic['savings'],
        'smart_is_optimized': smart_logic['optimized'],
    }
    
    return render(request, 'cart.html', context)




# --- Keep existing cart_compare for safety if called directly ---
def cart_compare(request):
    cart = request.session.get('cart', [])
    comparison = ""
    if len(cart) >= 2:
        sorted_cart = sorted(cart, key=lambda x: x.get('extracted_price', 0))
        cheapest, others = sorted_cart[0], sorted_cart[1]
        diff = others.get('extracted_price', 0) - cheapest.get('extracted_price', 0)
        if diff > 0:
            comparison = f"Decision Made: '{cheapest['title'][:30]}...' is the winner! It's ₹{diff} cheaper. We recommend {cheapest['source']}."
        else:
            comparison = "Both products have similar pricing."
    return render(request, 'cart.html', {'cart': cart, 'comparison': comparison})

# --- AUTH VIEWS ---
def signup_user(request):
    if request.method == "POST":
        u = request.POST.get('username'); p = request.POST.get('password')
        if User.objects.filter(username=u).exists(): messages.error(request, "Username taken")
        else:
            user = User.objects.create_user(username=u, password=p)
            login(request, user); return redirect('home')
    return render(request, 'login.html')

def login_user(request):
    if request.method == "POST":
        u = request.POST.get('username'); p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user: login(request, user); return redirect('home')
        else: messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

def logout_user(request):
    logout(request); return redirect('home')
# --- WISHLIST LOGIC ---
@login_required(login_url='login')
def view_wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': items})


@login_required(login_url='login')
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    item.delete()
    return redirect('view_wishlist')



@login_required(login_url='login')
def add_to_wishlist(request):
    if request.method == "POST":
        p_data = request.POST.get('product_data')
        if p_data:
            # 1. Pehle data ko load karein
            final_data = json.loads(p_data)
            
            # 2. DISCOUNT FIX: Agar discount 0% hai, toh usey 'HOT DEAL' kar dein
            disc = str(final_data.get('discount', '')).strip()
            if disc in ["0% OFF", "0%", "0", "None", ""]:
                final_data['discount'] = "HOT DEAL"

            # 3. Data save karein (Apne Model ke hisaab se line check karein)
            Wishlist.objects.create(user=request.user, product_data=final_data)
            
            messages.success(request, "Added to wishlist!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))
       


# --- ALERT SYSTEM ---
@login_required(login_url='login')
def price_alerts(request):
    alerts = PriceAlert.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'alerts.html', {'alerts': alerts})



@login_required(login_url='login')
def set_price_alert(request):
    if request.method == "POST":
        PriceAlert.objects.create(
            user=request.user, 
            product_name=request.POST.get('product_name'), 
            target_price=request.POST.get('target_price')
        )
        messages.success(request, "Price alert set in INR!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required(login_url='login')
def delete_alert(request, alert_id):
    alert = PriceAlert.objects.get(id=alert_id, user=request.user)
    alert.delete()
    return redirect('price_alerts')




from .utils import get_alternative_products


def search_results(request):
    # SEARCH logic: query, sort aur location parameters le rahe hain
    query = request.GET.get('q', '')
    sort_option = request.GET.get('sort', 'relevance') # Default relevance
    location = request.session.get('location', 'India')
    
    # Passing sort_by directly to your updated utility function
    products = fetch_products(query, location=location, sort_by=sort_option)
    
    # Logic for Recommendation
    if products:
        # Relevance ke basis par sort karke pehle wale ko recommend mark karo
        if sort_option == 'relevance':
            products.sort(key=lambda x: (float(x.get('rating', 0)) * 10) - (float(x.get('extracted_price', 0)) / 1000), reverse=True)
        products[0]['recommended'] = True

    # --- 🚀 NEW: ALTERNATIVE PRODUCTS LOGIC START ---
    # Har product ke liye baaki results mein se alternatives dhoondhein
    for item in products:
        # Hum 'products' (poori list) ko as a database bhej rahe hain
        item['alternatives'] = get_alternative_products(item, products)
    # --- NEW: ALTERNATIVE PRODUCTS LOGIC END ---

    for item in products:
        # Data serialization taaki Wishlist/Cart functionality na tute
        item['json_data'] = json.dumps(item)

    # Recent Searches Update logic (Strictly Keeping Existing Code)
    if query:
        recent = request.session.get('recent_searches', [])
        if query not in recent:
            recent.insert(0, query)
            request.session['recent_searches'] = recent[:5]
    
    context = {
        'products': products, 
        'query': query, 
        'sort': sort_option, 
        'location': location
    }
    
    # Purane template name 'search.html' ko hi return kar raha hoon
    return render(request, 'search.html', context)

# Category clicks ko manage karne ke liye (behaving exactly like search)
def category_view(request, category_name):
    # Category clicks ko query ki tarah treat karenge
    sort_option = request.GET.get('sort', 'relevance')
    location = request.session.get('location', 'India')
    
    # Category name ko hi query bana kar fetch kar rahe hain
    products = fetch_products(category_name, location=location, sort_by=sort_option)
    # 1. Sabse pehle relevance ke basis par sort karo (agar selected hai)
    # Logic for Recommendation
    if products:
        # Relevance ke basis par sort karke pehle wale ko recommend mark karo
        if sort_option == 'relevance':
            products.sort(key=lambda x: (float(x.get('rating', 0)) * 10) - (float(x.get('extracted_price', 0)) / 1000), reverse=True)
        products[0]['recommended'] = True
    

    # 3. Phir baaki ka loop chalne do (json_data wala)
    for item in products:
        item['json_data'] = json.dumps(item)

    
    context = {
        'products': products,
        'query': category_name, # Category name search query ki tarah display hoga
        'sort': sort_option,
        'location': location
    }
    
    # Same search template use kar rahe hain consistent results ke liye
    return render(request, 'search.html', context)


# --- CART & UTILS ---
@login_required(login_url='login')
def add_to_cart(request):
    if request.method == "POST":
        p_data = request.POST.get('product_data')
        if p_data:
            data = json.loads(p_data)
            # Check if item exists to increment quantity
            item, created = CartItem.objects.get_or_create(
                user=request.user, 
                product_data=data
            )
            if not created:
                item.quantity += 1
                item.save()
            messages.success(request, "Added to Cart! 🛒")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required(login_url='login')
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user).order_by('-added_at')
    total_price = sum(float(re.sub(r'[^\d.]', '', str(item.product_data.get('price', 0)))) * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})





def set_location(request):
    if request.method == "POST":
        loc = request.POST.get('location')
        request.session['location'] = loc
        return redirect('home')
    
def get_optimized_cart_v2(cart_items):
    import re
    grouped_data = {}
    original_total = 0

    if not cart_items:
        return {"optimized": False, "optimized_items": [], "optimized_total": "0.00", "savings": 0}

    for item in cart_items:
        data = item.product_data
        p_str = str(data.get('price', '0'))
        price = float(re.sub(r'[^\d.]', '', p_str)) if any(c.isdigit() for c in p_str) else 0.0
        
        # KEYWORD MATCHING: Pehle 7-8 letters se match karein (e.g., "Peanut")
        full_name = data.get('title', 'Unknown Product').strip()
        match_key = full_name.lower()[:8] 
        
        source = data.get('source', 'Unknown')
        qty = item.quantity
        original_total += (price * qty)

        if match_key not in grouped_data:
            grouped_data[match_key] = {
                'display_name': full_name,
                'best_platform': source,
                'price': price,
                'qty': qty
            }
        else:
            # Agar wahi product dusri jagah sasta hai, toh update karein
            if price < grouped_data[match_key]['price']:
                grouped_data[match_key]['price'] = price
                grouped_data[match_key]['best_platform'] = source

    optimized_items = list(grouped_data.values())
    optimized_total_val = sum(i['price'] * i['qty'] for i in optimized_items)
    savings = original_total - optimized_total_val

    return {
        "optimized": savings > 0.5, # Thoda bhi bacha toh dikhao
        "optimized_items": optimized_items,
        "optimized_total": f"{optimized_total_val:,.2f}",
        "savings": int(savings)
    }


from .utils import get_alternative_products
import json

def search_results(request):
    query = request.GET.get('q', '')
    sort_option = request.GET.get('sort', 'relevance')
    location = request.session.get('location', 'India')
    
    # Products fetch karo
    products = fetch_products(query, location=location, sort_by=sort_option)
    
    if products:
        # Step A: Pehle Alternatives nikalein
        for item in products:
            item['alternatives'] = get_alternative_products(item, products)
            
        # Step B: Phir JSON data banayein (taaki alternatives bhi JS mein chale jayein)
        for item in products:
            item['json_data'] = json.dumps(item)

        # Step C: Recommendation mark karein
        if sort_option == 'relevance':
            products.sort(key=lambda x: (float(x.get('rating', 0)) * 10) - (float(x.get('extracted_price', 0)) / 1000), reverse=True)
        products[0]['recommended'] = True

    context = {'products': products, 'query': query, 'sort': sort_option, 'location': location}
    print(products[0].get('alternatives'))

    return render(request, 'search.html', context)