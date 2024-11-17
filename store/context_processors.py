from .models import Category

def get_nav_category(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return context