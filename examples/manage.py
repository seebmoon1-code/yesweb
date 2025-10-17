
import sys
import os
from waitress import serve 

# تنظیم مسیرها برای پیدا کردن src و oneapp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))) 

from src.core import Application
from examples.settings import USER_SETTINGS
from oneapp.views import URL_ROUTES # ایمپورت مسیرها از اپلیکیشن


if __name__ == "__main__":
    app = Application(routes=URL_ROUTES, settings=USER_SETTINGS) 
    
    host = app.settings.DEFAULT_HOST
    port = app.settings.DEFAULT_PORT
    
    print("-" * 20)
    print(f"YesWeb در حال اجرا در: http://{host}:{port}")
    print(f"DEBUG Mode: {app.settings.DEBUG}")
    print(f"اپلیکیشن‌های نصب شده: {app.settings.INSTALLED_APPS}")
    print("برای توقف سرور، Ctrl+C را فشار دهید.")
    print("-" * 20)
    
    # اجرای فریم‌ورک با سرور Waitress
    serve(app, host=host, port=port)
