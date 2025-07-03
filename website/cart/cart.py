from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session =request.session
        #Get request
        self.request = request
        #Get a current session cart
        cart = self.session.get('session_key')
        
        #Create a new session key if user don't have one yet
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #Make sure cart is avalaible on all the pages
        self.cart = cart

    def get_quants(self):
        quantities = self.cart
        return quantities

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id]= {'price': str(product.price)}
            self.cart[product_id]= int(product_qty)

        self.session.modified = True

        #If user is logged in
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Conver '' to "" from cart DB
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id]= {'price': str(product.price)}
            self.cart[product_id]= int(product_qty)

        self.session.modified = True

        #If user is logged in
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Conver '' to "" from cart DB
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)

    def get_products(self):
        #Get products from the cart
        product_ids = self.cart.keys()
        #Add the products to db based on their ids
        products = Product.objects.filter(id__in=product_ids)

        return products
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        #Get cart
        ourcart = self.cart
        ourcart[product_id]=product_qty

        self.session.modified = True
        
        #If user is logged in
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Conver '' to "" from cart DB
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

        thing = self.cart

        return thing
    
    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        #If user is logged in
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Conver '' to "" from cart DB
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))


    def total(self):
        products = self.get_products()

        quantities = self.cart
        cart_sum = 0

        for key, val in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    cart_sum += product.price * val

        return cart_sum