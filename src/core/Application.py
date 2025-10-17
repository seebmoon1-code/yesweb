import importlib 
import sys # برای تنظیم مسیر ایمپورت در لود خودکار
import os  # برای استفاده در لود خودکار

from src.routing import Router
from src.config import Settings  
from .Request import Request
from .Response import Response
from .Template import TemplateRenderer
from .Static import StaticFileHandler, static_view 

class Application:
    """هسته اصلی فریم‌ورک YesWeb، سازگار با WSGI."""
    
    def __init__(self, settings=None): 
        print("YesWeb Application در حال راه‌اندازی...")
        
        # ۱. تنظیمات و مسیریاب
        self.settings = Settings(user_settings=settings)
        self.router = Router()
        
        # ۲. مقداردهی اولیه Template Renderer و Static/Media Handler
        self.renderer = TemplateRenderer(settings=self.settings) 
        self.static_handler = StaticFileHandler(settings=self.settings, is_media=False)
        self.media_handler = StaticFileHandler(settings=self.settings, is_media=True) 
        
        # ۳. لود کردن خودکار مسیرها از INSTALLED_APPS
        self._load_app_routes()
        
        # ۴. اضافه کردن مسیرهای Static و Media در حالت DEBUG
        if self.settings.DEBUG:
            # مسیر استاتیک: /static/<filename>
            self.router.add_route(f"{self.settings.STATIC_URL}<filename>", static_view) 
            # مسیر مدیا: /media/<filename>
            self.router.add_route(f"{self.settings.MEDIA_URL}<filename>", static_view) 
            print(f"مسیردهی Static و Media فعال شد.")

    def _load_app_routes(self):
        """مسیرهای URL_ROUTES را از تمام INSTALLED_APPS لود می‌کند."""
        print("در حال لود مسیرها از INSTALLED_APPS...")
        
        # نیاز به اضافه کردن مسیر پروژه نمونه به sys.path برای Importlib
        # (فرض می‌کنیم پوشه examples در کنار src قرار دارد)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'examples'))
        if base_dir not in sys.path:
            sys.path.append(base_dir)

        for app_name in self.settings.INSTALLED_APPS:
            # ماژول مسیردهی را از app_name.views لود می‌کنیم
            module_name = f"{app_name}.views"
            try:
                # لود داینامیک ماژول
                views_module = importlib.import_module(module_name)
                
                # بررسی URL_ROUTES در ماژول
                routes = getattr(views_module, 'URL_ROUTES', {})
                for path, view_func in routes.items():
                    self.router.add_route(path, view_func)
                print(f"  مسیرهای '{app_name}' با موفقیت لود شد.")
                
            except ImportError as e:
                # این خطا معمولاً یعنی ماژول یا app_name پیدا نشده است
                print(f"  هشدار: نتوانست ماژول مسیردهی '{module_name}' را لود کند. آیا نام اپلیکیشن یا پوشه درست است؟ خطا: {e}")
            except AttributeError:
                # این خطا یعنی ماژول views.py پیدا شده اما URL_ROUTES در آن نیست
                print(f"  هشدار: ماژول '{module_name}' شامل دیکشنری URL_ROUTES نیست.")


    def __call__(self, environ, start_response):
        """پیاده‌سازی متد WSGI."""
        request = Request(environ=environ)
        view_func, path_params = self.router.resolve(request.path)
        
        if view_func:
            try:
                kwargs = path_params
                kwargs['request'] = request
                kwargs['renderer'] = self.renderer
                
                # ارسال handler مناسب برای static_view
                if view_func == static_view:
                    # تعیین کنید که آیا درخواست Static است یا Media
                    if request.path.startswith(self.settings.STATIC_URL):
                        kwargs['handler'] = self.static_handler
                    elif request.path.startswith(self.settings.MEDIA_URL):
                        kwargs['handler'] = self.media_handler
                
                response = view_func(**kwargs) 
                
            except Exception as e:
                # مدیریت خطاهای View
                content = f"<h1>500 - خطای داخلی سرور</h1><p>یک خطا در اجرای View رخ داد: {e}</p>"
                response = Response(content=content, status=500)
        else:
            # مسیر پیدا نشد (404)
            content = f"<h1>404 - یافت نشد</h1><p>مسیر {request.path} در YesWeb پیدا نشد.</p>"
            response = Response(content=content, status=404)

        return response(start_response)
