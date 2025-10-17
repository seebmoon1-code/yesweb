from src.core import Response 

def homepage_view(request, renderer, **kwargs):
    """
    View برای صفحه اصلی که فرم ثبت‌نام را مدیریت می‌کند.
    - متد GET: نمایش فرم.
    - متد POST: پردازش داده‌های ارسالی.
    """
    
    if request.method == 'POST':
        # --- ۱. پردازش داده‌های ارسالی (POST) ---
        
        # استفاده از متد get_form_data در کلاس Request
        form_data = request.get_form_data() 
        
        first_name = form_data.get('first_name', 'ناشناس')
        last_name = form_data.get('last_name', 'ناشناس')
        
        # **گام دیتابیس:** در اینجا داده‌ها در کنسول چاپ می‌شوند.
        print(f"--- داده‌های جدید ثبت شد ---")
        print(f"نام: {first_name}")
        print(f"نام خانوادگی: {last_name}")
        print(f"-----------------------------")
        
        # رندر یک پیام موفقیت
        success_message = f"ثبت با موفقیت انجام شد! نام: {first_name} {last_name}"
        html_content = renderer.render('base.html', {'title': 'ثبت موفق', 'message': success_message})
        return Response(content=html_content)

    else:
        # --- ۲. نمایش فرم (GET) ---
        html_content = renderer.render('base.html', {'title': 'صفحه اصلی YesWeb', 'message': 'خوش آمدید به YesWeb!'})
        return Response(content=html_content)

def about_view(request, renderer, **kwargs):
    """View برای صفحه درباره ما."""
    # فرض می‌کنیم می‌خواهیم برای این صفحه هم از قالب استفاده کنیم.
    context = {
        'title': 'درباره فریم‌ورک ما',
        'message': f'این یک فریم‌ورک ماژولار است که با پایتون ساخته شده. متد درخواست: {request.method}',
    }
    html_content = renderer.render('base.html', context)
    return Response(content=html_content)

def user_profile_view(request, renderer, user_id, **kwargs):
    """View برای نمایش پروفایل کاربر بر اساس شناسه پویا."""
    content = f"<h1>پروفایل کاربر</h1><p>شناسه کاربری: <b>{user_id}</b></p><p>این یک مسیر پویا است.</p>"
    return Response(content=content)

def product_detail_view(request, renderer, category, product_slug, **kwargs):
    """View با چندین متغیر پویا."""
    content = f"<h1>جزئیات محصول</h1><p>دسته: {category}</p><p>نام محصول: {product_slug}</p>"
    return Response(content=content)

# دیکشنری مسیرها (URL_ROUTES)
URL_ROUTES = {
    "/": homepage_view,
    "/about": about_view,
    "/users/<user_id>": user_profile_view, 
    "/products/<category>/<product_slug>": product_detail_view, 
}
