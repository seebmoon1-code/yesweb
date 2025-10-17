# src/core/Static.py (کد کامل و نهایی)

import os
from src.core.Response import Response
from mimetypes import guess_type

class StaticFileHandler:
    """مسئول پیدا کردن و برگرداندن فایل‌های استاتیک و Media."""
    
    def __init__(self, settings, is_media=False): # is_media: جدید
        self.settings = settings
        self.is_media = is_media
        self.file_dirs = self._get_file_dirs()
        print(f"{'Media' if is_media else 'Static'} Handler راه‌اندازی شد. مسیرها: {self.file_dirs}")

    def _get_file_dirs(self):
        """مسیرهای جستجو را بر اساس Static یا Media بودن جمع‌آوری می‌کند."""
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'examples'))
        
        if self.is_media:
            # مسیر جستجو: پوشه MEDIA_ROOT در ریشه پروژه
            media_root_path = os.path.join(base_dir, '..', self.settings.MEDIA_ROOT)
            return [media_root_path] if os.path.isdir(media_root_path) else []
        else:
            # مسیر جستجو: پوشه‌های 'static/' داخل INSTALLED_APPS
            static_paths = []
            for app_name in self.settings.INSTALLED_APPS:
                app_path = os.path.join(base_dir, app_name, 'static') 
                if os.path.isdir(app_path):
                    static_paths.append(app_path)
            return static_paths

    def serve_file(self, file_path):
        """فایل را بر اساس مسیر نسبی در پوشه‌های جستجو پیدا و برمی‌گرداند."""
        # ... (بقیه متد serve_file بدون تغییر)
        for root_dir in self.file_dirs:
            full_path = os.path.join(root_dir, file_path)
            
            if os.path.isfile(full_path):
                # اگر فایل پیدا شد:
                mime_type, _ = guess_type(full_path)
                mime_type = mime_type if mime_type else 'application/octet-stream'
                
                with open(full_path, 'rb') as f:
                    content = f.read()
                    
                return Response(
                    content=content, 
                    status=200, 
                    headers=[('Content-Type', mime_type)]
                )
        return Response(content="File Not Found", status=404)


def static_view(request, handler, filename, **kwargs):
    """View برای فایل‌های Static و Media."""
    return handler.serve_file(filename)
