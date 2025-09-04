from django.shortcuts import render, redirect
import markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/error.html",{
            "title": title,
            "message":"The requested page was not found."
        })
    
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
    
    if query.lower() in [entry.lower() for entry in all_entries]:
        return redirect("entry", title=query)
    
    results = [entry for entry in all_entries if query.lower() in entry.lower()]

    return render(request, "encyclopedia/search.html",{
        "query": query,
        "results": results
    })