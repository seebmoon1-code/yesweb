
# src/routing/Router.py (بروزرسانی شده)

import re # ایمپورت کتابخانه عبارات با قاعده

class Router:
    """
    مدیریت مسیردهی: نگاشت URLها به توابع View، با پشتیبانی از مسیرهای پویا.
    """
    def __init__(self):
        # لیست برای ذخیره مسیرها: [(الگوی Regex, View Function)]
        self.routes = []
        
    def add_route(self, path, view_func):
        """
        یک مسیر جدید به لیست مسیرهای فریم‌ورک اضافه می‌کند.
        
        مسیرهای پویا را به الگوی Regex تبدیل می‌کند.
        مثال: /users/<id> تبدیل می‌شود به: ^/users/(?P<id>[^/]+)$
        """
        # 1. بخش‌های پویا را پیدا می‌کنیم (مثل <name> یا <id>)
        # و آنها را با یک گروه اسمی Regex (?P<name>[^/]+) جایگزین می‌کنیم.
        # [^/]+ یعنی: یک یا چند کاراکتر غیر از / (تا بخش بعدی مسیر).
        pattern = re.sub(r'<([^>]+)>', r'(?P<\1>[^/]+)', path)
        
        # 2. الگوی نهایی Regex را ایجاد می‌کنیم (شروع و پایان مسیر)
        # re.compile برای اجرای بهینه‌تر Regex است.
        compiled_regex = re.compile(f'^{pattern}$')
        
        # 3. مسیر کامپایل شده و تابع ویو را به لیست مسیرها اضافه می‌کنیم.
        self.routes.append((compiled_regex, view_func))
        print(f"مسیر اضافه شد (پویا): {path}")

    def resolve(self, path):
        """
        تابع View مناسب برای یک مسیر ورودی را پیدا می‌کند و متغیرهای پویا را برمی‌گرداند.
        خروجی: (view_func, path_params) یا (None, None)
        """
        for regex, view_func in self.routes:
            # سعی می‌کنیم Regex را با مسیر ورودی مطابقت دهیم.
            match = regex.match(path)
            if match:
                # متغیرهای مسیر (مثل id=42) را استخراج می‌کنیم.
                path_params = match.groupdict() 
                return view_func, path_params
                
        return None, None # مسیر پیدا نشد
