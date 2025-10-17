
# src/core/Template.py

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
        print(f"Template Renderer راه‌اندازی شد. مسیرها: {self.template_dirs}")

    def _get_template_dirs(self):
        """مسیرهای پوشه templates را از اپلیکیشن‌های نصب شده جمع‌آوری می‌کند."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_paths = []
        
        # فرض می‌کنیم اپلیکیشن‌ها در کنار پوشه src قرار دارند.
        for app_name in self.settings.INSTALLED_APPS:
            app_path = os.path.join(base_dir, 'examples', app_name, 'templates') 
            if os.path.isdir(app_path):
                template_paths.append(app_path)
        
        return template_paths

    def render(self, template_name, context=None):
        """فایل قالب را رندر و محتوای HTML را برمی‌گرداند."""
        if context is None:
            context = {}
            
        template = self.env.get_template(template_name)
        return template.render(context)
