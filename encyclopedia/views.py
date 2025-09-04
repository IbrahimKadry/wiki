from django.shortcuts import render, redirect
import markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # هنا بيشوف لو في مقالة بنفس اسم المدخل 
    content = util.get_entry(title)

    # لو مفيش مقالة بنفس الاسم بيرجع None 
    if content == None:
        return render(request, "encyclopedia/error.html",{
            "title": title,
            "message":"The requested page was not found."
        })
    
    # هنا تحويل المحتوى الى لغة (اتش تي ام ال)
    html_content = markdown.markdown(content)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    # احصل على اللي هدور عليه من البحث
    query = request.GET.get('q','').strip()
    # لو البحث فاضي خالص ابعته للصفحة الرئيسية
    if not query:
        return redirect("index")
    # هنا بحفظ كل اسامي المقالات عندي في متغير 
    all_entries = util.list_entries()

    # هنا بحول اي حرف  للاصغر عشان كله يبقا متشابه 
    # ده شرط هيكون بصح او خطأ و بقول لو اللي بحثت عنه موجو بالظبط بنفس الحروف ولا لا 
    if query.lower() in [entry.lower() for entry in all_entries]:

        return redirect("entry", title=query)
    # هنا تحويل للصفحة اللي فيها نتيجة البحث المتطابق تماما فقط


    # هنا بجيب اي نتيجة تحتوي على حروف شبيهة للبحث و بحفهم في متغير واحد
    results = [entry for entry in all_entries if query.lower() in entry.lower()]
    
    # هنا بيظهر كل النتائج في صفحة البحث على شكل لينكات
    return render(request, "encyclopedia/search.html",{
        "query": query,
        "results": results
    })