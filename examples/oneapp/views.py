
from src.core import Response # Viewها باید Response را برگردانند

def homepage_view(request):
    """View برای صفحه اصلی."""
    content = "<h1>صفحه اصلی YesWeb</h1><p>خوش آمدید! به /about بروید.</p>"
    return Response(content=content)

def about_view(request):
    """View برای صفحه درباره ما."""
    content = f"<h1>درباره ما</h1><p>این فریم‌ورک ماژولار است.</p><p>متد: {request.method}</p>"
    return Response(content=content)

# View برای مسیرهای پویا
def user_profile_view(request, user_id):
    """View برای نمایش پروفایل کاربر بر اساس شناسه پویا."""
    content = f"<h1>پروفایل کاربر</h1><p>شناسه کاربری: <b>{user_id}</b></p><p>این یک مسیر پویا است.</p>"
    return Response(content=content)

def product_detail_view(request, category, product_slug):
    """View با چندین متغیر پویا."""
    content = f"<h1>جزئیات محصول</h1><p>دسته: {category}</p><p>نام محصول: {product_slug}</p>"
    return Response(content=content)

# دیکشنری مسیرها
URL_ROUTES = {
    "/": homepage_view,
    "/about": about_view,
    "/users/<user_id>": user_profile_view, 
    "/products/<category>/<product_slug>": product_detail_view, 
}
