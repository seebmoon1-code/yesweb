
# src/core/Static.py

import os
from src.core.Response import Response # برای برگرداندن پاسخ
from mimetypes import guess_type # برای پیدا کردن Content-Type فایل (مثلاً text/css)

class StaticFileHandler:
    """
    مسئول پیدا کردن و برگرداندن فایل‌های استاتیک از پوشه‌های 'static/' اپلیکیشن‌ها.
    """
    def __init__(self, settings):
        self.settings = settings
        self.static_dirs = self._get_static_dirs()
        print(f"Static Handler راه‌اندازی شد. مسیرها: {self.static_dirs}")

    def _get_static_dirs(self):
        """مسیرهای پوشه static را از اپلیکیشن‌های نصب شده جمع‌آوری می‌کند."""
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'examples'))
        static_paths = []
        
        # گشتن در INSTALLED_APPS برای یافتن پوشه 'static'
        for app_name in self.settings.INSTALLED_APPS:
            # مسیر مورد انتظار: /yesweb/examples/oneapp/static
            app_path = os.path.join(base_dir, app_name, 'static') 
            if os.path.isdir(app_path):
                static_paths.append(app_path)
        
        return static_paths

    def serve_file(self, file_path):
        """فایل را بر اساس مسیر نسبی در پوشه‌های static پیدا و برمی‌گرداند."""
        
        for root_dir in self.static_dirs:
            # مسیر کامل مورد انتظار فایل
            full_path = os.path.join(root_dir, file_path)
            
            if os.path.isfile(full_path):
                # اگر فایل پیدا شد:
                mime_type, _ = guess_type(full_path)
                mime_type = mime_type if mime_type else 'application/octet-stream'
                
                with open(full_path, 'rb') as f:
                    content = f.read()
                    
                # ساخت Response
                return Response(
                    content=content, 
                    status=200, 
                    headers=[('Content-Type', mime_type)]
                )
        
        # اگر فایل پیدا نشد
        return Response(content="File Not Found", status=404)
