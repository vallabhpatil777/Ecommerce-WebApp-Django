from .models import Category

def nav_category(request):
    blog_categories = Category.objects.all()
    context = {'blog_categories': blog_categories}
    return context