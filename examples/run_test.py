
# examples/run_test.py (بروزرسانی شده)

import sys
import os
from waitress import serve 

# این دو خط برای اضافه کردن مسیر 'src' به سیستم پایتون ضروری است
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import Application
from examples.views import URL_ROUTES # ایمپورت مسیرهای جدا شده

# ساخت یک نمونه از فریم‌ورک و ارسال مسیرها به آن
if __name__ == "__main__":
    # مسیرها را به Application می‌فرستیم تا در Router قرار دهد.
    app = Application(routes=URL_ROUTES) 
    
    host = '127.0.0.1'
    port = 8000
    print(f"YesWeb در حال اجرا در: http://{host}:{port}")
    print("(برای توقف سرور، Ctrl+C را فشار دهید)")
    
    # اجرای فریم‌ورک با سرور Waitress
    serve(app, host=host, port=port)
