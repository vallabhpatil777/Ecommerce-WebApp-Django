from .cart import Cart

# context processor to make sure it works on every page
def cart(request):
    return {'cart': Cart(request)}