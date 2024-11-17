from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, Category, ProductComment, Profile, Customer, Order

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ProductCommentForm, EditUserForm

from django.views import generic
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm


from django.urls import reverse, reverse_lazy

from .forms import EditProfile, ProfileForm
from django.contrib.auth.views import PasswordChangeView

from django.core.paginator import Paginator
from hitcount.views import HitCountDetailView

from django.contrib.auth import update_session_auth_hash

from datetime import datetime, timedelta


def home(request):
    products = Product.objects.all()
    
    sort_by = request.GET.get("sort", "l2h") 
    if sort_by == "l2h":
       products = products.order_by("price")
    elif sort_by == "h2l":
       products = products.order_by("-price")
    elif sort_by == "mv":
       products = products.order_by("-is_visited")
    elif sort_by == "lv":
       products = products.order_by("is_visited")
       
    
    paginator = Paginator(products, 8)
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    
    
       
    
    
    
    return render(request, 'home.html', {'products': products, 'page_obj': page_obj})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    
    if request.method == 'POST':
        usernames = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=usernames, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'با موفقیت وارد شدید')
            return redirect('home')
    
        else:
            messages.error(request, 'مشکلی پیش آمده است')
            return redirect('login')
    else:
        return render(request, 'login.html', {})
    
    

def logout_user(request):
    logout(request)
    messages.success(request, 'با موفقیت حارج شدید')
    return redirect('home')



def register_user(request):
    
    form = SignUpForm()
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            
            #login
            user = authenticate(username=username, password=password)
            user_profile = Profile.objects.create(user=user)
            user_profile.save()
            login(request, user)
            messages.success(request, 'با موفقیت ثبت نام کردید')
            return redirect('home')
        
        else:
            messages.error(request, 'مشکلی پیش آمده است')
            return redirect('register')
        
    else:
        return render(request, 'register.html', {'form': form})
    

class CreateProfileView(generic.CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'create_profile.html'
    
    def form_valid(self, form):
        form.instance_user = self.request.user
        return super().form_valid(form)
    
    
def product(request, pk):
    
    product = Product.objects.get(id=pk)
    product.count_visited()
    return render(request, 'product.html', {'product': product})

class ProductDetailView(HitCountDetailView):
    model = Product
    template_name = 'product.html'
    
    
    form = ProductCommentForm
    
    def post(self, request, pk, *args, **kwargs):
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            product = self.get_object()
            form.instance.user = request.user
            form.instance.product = product
            form.save()
            
            
            return redirect(reverse('product', args=[str(pk)]))
        
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Product, id = self.kwargs['pk'])
        stuff.is_visited = stuff.is_visited + 1
        
        product_comments = ProductComment.objects.filter(product=self.object.id)
        comment_count = product_comments.count()
        
        
        # liked = False
        # if stuff.like.filter(id=self.request.user.id).exists():
        #     liked = True
        context["form"] = self.form
        context["product_comments"] = product_comments
        context["comment_count"] = comment_count
        stuff.save()
        print('context works')
        return context


def category(request, cat):
    
    cat = cat.replace('-', ' ')
    print('wrong view')
    try:
		# Look Up The Category
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(Category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("همچین دسته بندی وجود ندارد..."))
        return redirect('home')
            
            
def category_summary(request):
    
    categories = Category.objects.all()
    
    return render(request, 'category_summary.html', {'categories': categories})


class UserEditView(generic.UpdateView):
    model = User
    template_name = 'edit_profile.html'
    form_class = EditUserForm
    
    
    def get_success_url(self) -> str:
        user = self.request.user.id
        return reverse_lazy('profile', kwargs={'pk': user})
    
    
    def get_object(self) -> Model:
        return self.request.user


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')
    
def change_password(request, pk):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد')
            return redirect('home')
        else:
            messages.error(request, 'مشکلی پیش آمده است')
            messages.error(request, f'{form.errors}')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })
    
    
class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'edit_profile_page.html'
    form_class = EditProfile
    
    def get_success_url(self) -> str:
        user = self.request.user.id
        return reverse_lazy('profile', kwargs={'pk': user})
    
    
    
def profile_page_view(request, pk):
    profile = Profile.objects.get(id=pk)
    
    return render(request, 'profile.html', {'profile': profile})

def navbar_stuff(request):
    categories = Category.objects.all()
    return render(request, 'navbar.html', {'categories': categories})


def search_stuff(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        products = Product.objects.filter(name__contains=searched)
        
    return render(request, 'searched.html', {'searched': searched, 'products': products})



def payment(request):
    new_order = Order.objects.create(product=Product.objects.filter(name__contains='plant'), user=request.user, quantity=1, address='hell', phone='09125559999')
    new_order.save()
    orders = Order.objects.all()
    return render(request, 'payment.html', {'orders': orders})


def admin_panel(request, pk):
    
    total_users = User.objects.all().count()
    admin_users = User.objects.filter(is_staff=True).count()
    
    today = datetime.now().date()
    users_today = User.objects.filter(date_joined__date=today).count()
    
    products = Product.objects.all().order_by('-is_visited')
    most_visited = products[0]
    
    total_products = Product.objects.all().count()
    
    x = {}
    comments = ProductComment.objects.all()
    for c in comments:
        if c.product.id not in x:
            x[c.product.id] = 1
        else:
            x[c.product.id] = x[c.product.id] + 1
    
    result = max(x, key=x.get)
    most_commented_product = Product.objects.get(pk=result)
    comment_count = x[result]
    
    
    return render(request, 'admin_panel.html', {'total_users': total_users, 'admin_users': admin_users, 'users_today': users_today, 'most_visited': most_visited, 'total_products': total_products, 'most_commented_products': most_commented_product, 'comment_count': comment_count})


def entrance(request):
    return render(request, 'entrance.html', {})


def payment(request):
    return render(request, 'payment.html')