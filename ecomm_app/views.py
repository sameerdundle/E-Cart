from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from ecomm_app.models import Products,Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail
from ecomm import settings
import json
import hmac
import hashlib
from django.http import JsonResponse

# Create your views here.

def home1(request):
    context={}
    context['greet']="Hello   Good Morning..."
    context['x']=10
    context['y']=20
    context['l']=[1,2,3,4,5]
    context['product']=[
        {'id':1,'name':"Samsung",'Cat':"Mobile",'Price':25000},
        {'id':2,'name':"Jeans",'Cat':"Clothes",'Price':2000},
        {'id':3,'name':"iPhone",'Cat':"Mobile",'Price':75000},
        {'id':4,'name':"Woodland",'Cat':"Shoes",'Price':3000},
        {'id':5,'name':"Adidas",'Cat':"clothes",'Price':1500}
        
    ]
    # return HttpResponse("Hello You are on home page")
    return render(request,'home.html',context)

def home(request):
    userid=request.user.id
    print("id of logged in user is : ",userid)
    context={}
    p=Products.objects.filter(is_active=True)
    context["products"]=p
    return render(request,'index.html',context)


def about(request):
    return HttpResponse("This is about page")

def pdetails(request,pid):
    p=Products.objects.filter(id=pid)
    context={}
   
    context['products']=p
    return render(request,'product_details.html',context)

def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    np=len(c)
    print(np)
    s=0
    for x in c:
        print(x)
        print(x.pid.price)
        s=s+x.pid.price*x.qty
        print(s)

    # print(c)
    # print(c[0].pid)
    # print(c[0].uid)
    # print(c[0].pid.price)
    # print(c[0].pid.name)
    # print(c[0].pid.pdetails)
    # print(c[0].uid.username)
    context={}
    context['products']=c
    context['total']=s
    context['n']=np
    return render(request,'cart.html',context)

def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        if uname=="" or upass=="" or ucpass=="":
            context={}
            context['errmsg']="Field can not be empty"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context={}
            context['errmsg']="Password Did not Match"
            return render(request,'register.html',context)
        else:
            # print(uname,upass,ucpass)
            try:
                u=User.objects.create(username=uname,email=uname,password=upass)
                u.set_password(upass)
                u.save()
                context={}
                context['success']="User Created Successfully.."
                return render(request,'register.html',context)
            except Exception:
                context={}
                context['errmsg']="user with same username already exists"
                return render(request,'register.html',context)

    else:
        return render(request,'register.html')

def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        # print(uname,upass)
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Field can not be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            print(u)#none
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errmsg']="Invalid username and password."
                return render(request,'login.html',context)
        # return HttpResponse("Login Successfully...")
    else:
     return render(request,'login.html')
 
def user_logout(request):
    logout(request)
    return redirect('/home')

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Products.objects.filter(q1&q2)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    if request.method=='POST':
        min=request.POST['min']
        max=request.POST['max']
        # print(min,max)
        q1=Q(price__gte=min)
        q2=Q(price__lte=max)
        q3=Q(is_active=True)
        p=Products.objects.filter(q1&q2&q3)
        context={}
        context['Products']=p
        return render(request,'index.html',context)
    else:
        return HttpResponse("we are getting the min max values")
    

def sort(request,sv):
    if sv =='0':
        col='price'
    else:
        col='-price'
    
    p=Products.objects.order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)
    
def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        p=Products.objects.filter(id=pid)
        # print(u[0])#Dipali16
        # print(p[0])#samsung
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1&q2)
        n=len(c)#n=1
        context={}
        context['products']=p
        # print(c)
        if n == 1:
            context['msg']="Product Already Exist."
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product added Successfully in the cart....!  "
        return render(request,'product_details.html',context)
    else:
        return redirect('/login')

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')


def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv == '1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect('/viewcart')       
    # return HttpResponse("Quantity")

def placeorder(request):
    userid=request.user.id
    # print(userid)
    c=Cart.objects.filter(uid=userid)
    # print(c)
    oid=random.randrange(1000,9999)
    # print(oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=userid)
    # print(orders)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty

    context={}
    context['total']=s
    context['product']=orders
    return render(request,'placeorder.html',context)

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
        oid=x.order_id
        print(oid)
    
    client = razorpay.Client(auth=("rzp_test_HQA2EMtGz19iN0", "s10PyY4gs2PsrE5MiVtPfzKF"))

    DATA = {
    "amount": s,
    "currency": "INR",
    "receipt": oid,
    "notes": {
        "key1": "value3",
        "key2": "value2"
    }
    }
    payment=client.order.create(data=DATA)
    print(payment)
    context={}
    context['amount']=payment
    return render(request,'pay.html')
    # return HttpResponse("In payment section.")



def verify_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("Payment verification data:", data)

        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')

        # Verify signature
        key_secret = b"s10PyY4gs2PsrE5MiVtPfzKF"  # Razorpay Secret Key
        msg = f"{razorpay_order_id}|{razorpay_payment_id}".encode()
        generated_signature = hmac.new(key_secret, msg, hashlib.sha256).hexdigest()

        if generated_signature == razorpay_signature:
            return JsonResponse({'status': 'Payment verified'})
        else:
            return JsonResponse({'status': 'Signature mismatch'}, status=400)
        


def sendmail(request):
    orders = Order.objects.filter(uid=request.user.id)
    
    total_amount = 0
    for x in orders:
        total_amount += x.pid.price * x.qty

    user_name = request.user.username

    # Compose and send the email
    send_mail(
        subject='Ecart - Payment Confirmation',
        message=f'Thank you {user_name} for your payment of ₹{total_amount}. Your order has been placed successfully.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_name],
        fail_silently=False
    )

    
    return render(request, 'thankyou.html', {'total': total_amount})