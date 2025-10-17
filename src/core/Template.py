# src/core/Template.py (بروزرسانی شده)

import os
from jinja2 import Environment, FileSystemLoader

class TemplateRenderer:
    """
    مدیریت رندرینگ قالب‌ها با استفاده از Jinja2.
    """
    def __init__(self, settings):
        self.settings = settings
        self.template_dirs = self._get_template_dirs()
        
        # راه‌اندازی Jinja2 Environment
        self.env = Environment(
            loader=FileSystemLoader(self.template_dirs),
            autoescape=True
        )
        
        # اضافه کردن توابع کمکی static و media به عنوان توابع جهانی
        self.env.globals['static'] = self.static_url 
        self.env.globals['media'] = self.media_url
        
        print(f"Template Renderer راه‌اندازی شد. مسیرها: {self.template_dirs}")

    def _get_template_dirs(self):
        """مسیرهای پوشه templates را از اپلیکیشن‌های نصب شده جمع‌آوری می‌کند."""
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'examples')) 
        template_paths = []
        
        for app_name in self.settings.INSTALLED_APPS:
            app_path = os.path.join(base_dir, app_name, 'templates') 
            if os.path.isdir(app_path):
                template_paths.append(app_path)
        
        return template_paths

    def static_url(self, path):
        """آدرس URL کامل برای فایل‌های استاتیک را برمی‌گرداند."""
        return f"{self.settings.STATIC_URL}{path}"
        
    def media_url(self, path):
        """آدرس URL کامل برای فایل‌های Media را برمی‌گرداند."""
        return f"{self.settings.MEDIA_URL}{path}"

    def render(self, template_name, context=None):
        """فایل قالب را رندر و محتوای HTML را برمی‌گرداند."""
        if context is None:
            context = {}
            
        template = self.env.get_template(template_name)
        return template.render(context)
