from  flask import render_template , redirect ,request
from flask import current_app as app
from .models import db, Customer,Professional,ServiceCategory,Admin


@app.route("/" , methods = ["GET" , "POST"])
def home():
    return render_template("home.html" )



@app.route("/login" , methods = ["GET" , "POST"])
def login():
    if request.method=="GET":
        return render_template("login.html" )
    elif request.method =="POST":
        email = request.form.get("email")
        pwd = request.form.get("password")
        
        user  = db.session.query(Customer).filter_by(email = email).first() or db.session.query(Professional).filter_by(email = email).first() or db.session.query(Admin).filter_by(email = email).first()
      
        if not user:
            return "emaill does not exist"
        else:
            if isinstance(user , Customer):
                if user.password ==pwd:
                    return redirect("/dashboard/customer")
                else:
                    return "password does not match for customer"
            if isinstance(user , Professional):
                if user.password ==pwd:
                    return redirect("/dashboard/professional")    
                else:
                    return "password does not match"            
            if isinstance(user , Admin):
                if user.password ==pwd:
                    return redirect("/dashboard/admin")     
                else:
                    return "password does not match"


@app.route("/register/<utype>" , methods = ["GET" , "POST"])
def register(utype):
    if utype == "customer":
        if request.method=="GET":
            return render_template("/customer/register.html")
        if request.method == "POST":
            c_name = request.form.get("c_name")
            c_email = request.form.get("c_email")
            c_city = request.form.get("c_city")
            c_address = request.form.get("c_address")
            c_password = request.form.get("c_password")
            cust = db.session.query(Customer).filter_by(email = c_email).first() or db.session.query(Professional).filter_by(email = c_email).first()
            if not cust:
                c = Customer(name = c_name , email = c_email , city = c_city,address = c_address,password = c_password)
                db.session.add(c)
                db.session.commit()
                return redirect("/login")
            else:
                return "User already exist"
    elif utype == "professional":
        print("hello")
        if request.method=="GET":
            cats = db.session.query(ServiceCategory).all() or db.session.query(Customer).filter_by(email = c_email).first() 
            return render_template("/professional/register.html" , categories = cats)
        if request.method=="POST":
            print("hi")
            p_name = request.form.get("p_name")
            p_email = request.form.get("p_email")
            p_city = request.form.get("p_city")
            p_exp = request.form.get("p_exp")
            p_cat = request.form.get("p_cat")
            p_password = request.form.get("p_password")
            prof = db.session.query(Professional).filter_by(email = p_email).first()
            if not prof:
                p = Professional(name = p_name , email = p_email , city = p_city,experiance = p_exp,password = p_password, categroy_id = p_cat)
                db.session.add(p)
                db.session.commit()
                return redirect("/login")
            else:
                return "User already exist"
    else:
        return "url not found"        
    

@app.route("/dashboard/admin" , methods=["GET" ,"POST"])
def admin_dash():
    return "<h1>admin dashboard</h1>"

@app.route("/dashboard/customer" , methods=["GET" ,"POST"])
def cust_dash():
    return "<h1>Customer dashboard</h1>"

@app.route("/dashboard/professional" , methods=["GET" ,"POST"])
def prof_dash():
    return "<h1>Professional dashboard</h1>"