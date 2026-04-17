from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse

class LocationRequiredMiddleware:
    """
    Middleware jo check karega ki user ne location set ki hai ya nahi.
    Agar nahi, toh API requests par error dega aur pages par redirect karega.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Wo paths jahan location ki zaroorat NAHI hai (Exempted paths)
        # Inhe block nahi karna warna infinite loop ho jayega
        exempt_paths = [
            reverse('set_location'), # Naya view jo hum banayenge
            '/admin/',
            '/static/',
            '/media/',
            '/login/',
            '/register/'
        ]

        # Check if current path is exempt
        if any(request.path.startswith(path) for path in exempt_paths):
            return self.get_response(request)

        # 2. Check location in session
        user_pincode = request.session.get('user_pincode')

        if not user_pincode:
            # Agar API request hai (JSON mang raha hai)
            if request.path.startswith('/api/'):
                return JsonResponse({
                    "error": "Location required",
                    "code": "LOCATION_MISSING"
                }, status=403)
            
            # Agar normal web view hai, toh use homepage ya location page par rakho
            # Note: Iska frontend logic hum modal se handle karenge
            pass 

        return self.get_response(request)