
# src/core/Application.py (نسخه تمیز شده)

from src.routing import Router
from .Request import Request
from .Response import Response

class Application:
    """
    هسته اصلی فریم‌ورک YesWeb.
    """
    def __init__(self, routes=None):
        print("YesWeb Application در حال راه‌اندازی...")
        
        # مسیریاب را با مسیرهای تعریف شده (در صورت وجود) مقداردهی اولیه می‌کنیم
        self.router = Router()
        if routes:
             # اگر مسیری از بیرون تعریف شده باشد، آن را اضافه می‌کنیم.
             for path, view_func in routes.items():
                 self.router.add_route(path, view_func)

    def __call__(self, environ, start_response):
        # ... (بقیه متد __call__ بدون تغییر باقی می‌ماند و از self.router استفاده می‌کند)
        request = Request(environ=environ)
        
        # 1. مسیریابی: View مناسب را پیدا کن
        view_func = self.router.resolve(request.path)
        
        if view_func:
            try:
                # 2. اجرای View و دریافت Response
                response = view_func(request)
            except Exception as e:
                # مدیریت خطاهای View
                content = f"<h1>خطای داخلی سرور</h1><p>یک خطا در اجرای View رخ داد: {e}</p>"
                response = Response(content=content, status=500)
        else:
            # 3. مسیر پیدا نشد (404)
            content = f"<h1>404 - یافت نشد</h1><p>مسیر {request.path} در YesWeb پیدا نشد.</p>"
            response = Response(content=content, status=404)

        # 4. اجرای پاسخ و بازگشت به سرور WSGI
        return response(start_response)
