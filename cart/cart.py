from store.models import Product



class Cart:
    def __init__(self, request):
        
        self.session = request.session
        
        # current session key
        cart = self.session.get('session_key')
        
        # if now session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        
        # # available by all pages of site
        self.cart = cart
        
    
    def add(self, product, quantity):
        product_id = str(product.id)
        product_quantity = str(quantity)
        
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = product_quantity
            
        self.session.modified = True
        
    
    def __len__(self):
        
        return len(self.cart)
    
    
    def get_prods(self):
        
        # get ids of products in cart
        product_ids = self.cart.keys()
        
        # get products
        products = Product.objects.filter(id__in=product_ids)
        
        return products
    
    def get_quants(self):
        
        quantities = self.cart
        return quantities
    
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        
        ourcart = self.cart
        
        ourcart[product_id] = product_qty
        
        self.session.modified = True
        
        thing = self.cart
        return thing
    
    
    def delete(self, product):
        product_id = str(product)
        
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True
        
    
    def cart_total(self):
        # Get product IDS
        product_ids = self.cart.keys()
		# lookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
		# Get quantities
        quantities = self.cart
		# Start counting at 0
        total = 0

        for key, value in quantities.items():
			# Convert key string into into so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.on_sale:
                        
                        total = total + (product.sale_price * int(value))
                    else:
                        print(type(total))
                        print(type(product.sale_price))
                        print(type(value))
                        print(value)
                        total = total + (product.price * int(value))



        return total