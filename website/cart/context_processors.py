from .cart import Cart

#Create context processor so cart can work on every page
def cart(request):
    return {'cart': Cart(request)}