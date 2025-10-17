
# examples/views.py

from src.core import Response # Viewها باید Response را برگردانند

def homepage_view(request):
    """View برای صفحه اصلی."""
    content = "<h1>صفحه اصلی YesWeb</h1><p>خوش آمدید! به /about بروید. (مسیردهی تمیز شد)</p>"
    return Response(content=content)

def about_view(request):
    """View برای صفحه درباره ما."""
    # می‌توانیم از اطلاعات Request استفاده کنیم
    content = f"<h1>درباره ما</h1><p>این فریم‌ورک ماژولار است.</p><p>متد: {request.method}</p>"
    return Response(content=content)

def goodbye_view(request):
    """View جدید."""
    return Response(content="<h1>خداحافظ</h1><p>تا دیداری دیگر.</p>")
    
# دیکشنری مسیرها
URL_ROUTES = {
    "/": homepage_view,
    "/about": about_view,
    "/bye": goodbye_view,
}
