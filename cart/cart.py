class Cart():
    def __init__(self,request):
        self.session=request.session

        #get the current session key
        cart=self.session.get('session_key')

        #if the user is new
        if 'session_key' not in request.session:
            cart=self.session['session_key']={}

        #cart is available on all page
        self.cart=cart
    
    def add(self,product):
        prd_id=str(product.id)
        if prd_id in self.cart:
            pass
        else:
            self.cart[prd_id]={'price':str(product.price)}

        self.session.modified=True

class Wish():
    def __init__(self,request):
        self.session=request.session

        #get the current session key
        wish=self.session.get('session_key')

        #if the user is new
        if 'session_key' not in request.session:
            wish=self.session['session_key']={}

        #cart is available on all page
        self.wish=wish
    
    def add(self,product):
        prd_id=str(product.id)
        if prd_id in self.wish:
            pass
        else:
            self.wish[prd_id]={'price':str(product.price)}

        self.session.modified=True