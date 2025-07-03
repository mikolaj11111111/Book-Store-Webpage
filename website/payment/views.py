from django.shortcuts import render
from cart.cart import Cart
from cart.views import *
from payment.forms import ShippingForm, PaymentsForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product, Profile
import datetime


# Create your views here.
def payment_success(request):
    return render(request, 'payment/payment_success.html')

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            #Check if True or False
            if status == "true":
                order = Order.objects.filter(id=pk)
                #Update status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order = Order.objects.filter(id=pk)
                #Update status
                order.update(shipped=False)
            
            return redirect('home')
        return render(request, "payment/orders.html", {'order':order, 'items':items})

    else:
        messages.success(request, 'Access Denied')
        return redirect('home')   
def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        
        return render(request, "payment/not_shipped_dash.html", {'orders':orders})
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)

        return render(request, "payment/shipped_dash.html", {'orders':orders})
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')

def process_order(request):
    if request.POST:
        payment_form = PaymentsForm(request.POST or None)
        #Get Shipping Info Data
        my_shipping = request.session.get('my_shipping')

        #Gather Order Info
        #Create Shipping Address form Shipping Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_adress1']}\n{my_shipping['shipping_adress2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_country']}"
        
        cart = Cart(request)
        cart_products = cart.get_products
        num_to_loop = range(1,10)
        quantities = cart.get_quants
        totals = cart.total()
        amout_to_pay = totals

        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_adress=shipping_address, amout_to_pay=amout_to_pay)
            create_order.save()
            #Add Order Items
            order_id = create_order.pk

            for product in cart_products():
                product_id = product.id
                product_price = product.price

                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=product_price)
                        create_order_item.save()
            #Delete Cart
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key] 
            
            #Delete Cart form DB
            current_user = Profile.objects.filter(user__id=request.user.id)

            current_user.update(old_cart="")
            
        else:
            create_order = Order(full_name=full_name, email=email, shipping_adress=shipping_address, amout_to_pay=amout_to_pay)
            create_order.save()
            #Add Order Items
            order_id = create_order.pk

            for product in cart_products():
                product_id = product.id
                product_price = product.price

                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=product_price)
                        create_order_item.save()
                
                #Delete Cart
                for key in list(request.session.keys()):
                    if key == 'session_key':
                        del request.session[key]

        messages.success(request, 'Order completed')
        return redirect('home')


    else:
        return redirect('home')

def checkout(request):
    
    cart = Cart(request)
    cart_products = cart.get_products
    num_to_loop = range(1,10)
    quantities = cart.get_quants
    totals = cart.total()
    if request.user.is_authenticated:
        
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None,instance=shipping_user)
        return render(request, "payment/checkout.html", {'cart_products':cart_products,'shipping_form':shipping_form, 'num_to_loop':num_to_loop, 'quantities':quantities, 'totals':totals})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {'shipping_form':shipping_form,'cart_products':cart_products, 'num_to_loop':num_to_loop, 'quantities':quantities, 'totals':totals})

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products
        num_to_loop = range(1,10)
        quantities = cart.get_quants
        totals = cart.total()

        #Create a Session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping


        if request.user.is_authenticated:
            billing_form = PaymentsForm()

            return render(request, "payment/billing_info.html", {'shipping_info':request.POST,'billing_form':billing_form,'cart_products':cart_products, 'num_to_loop':num_to_loop, 'quantities':quantities, 'totals':totals})

        else:
            billing_form = PaymentsForm()
        shipping_form = request.POST

        return render(request, "payment/billing_info.html", {'shipping_info':request.POST,'shipping_form':shipping_form,'billing_form':billing_form,'cart_products':cart_products, 'num_to_loop':num_to_loop, 'quantities':quantities, 'totals':totals})
    else:
        return redirect('home')