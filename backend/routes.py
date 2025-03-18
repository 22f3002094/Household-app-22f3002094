from  flask import render_template , redirect ,request,flash
from flask import current_app as app
from .models import db, Customer,Professional,ServiceCategory,Admin,ServicePlan ,Booking
from flask_login import login_required,login_user,current_user,logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_ , or_
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("agg")


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
                    login_user(user)
                    return redirect(f"/dashboard/customer")
                else:
                    return "password does not match for customer"
            if isinstance(user , Professional):
                if user.password ==pwd:
                    login_user(user)
                    return redirect("/dashboard/professional")    
                else:
                    return "password does not match"            
            if isinstance(user , Admin):
                if user.password ==pwd:
                    login_user(user)
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
                p = Professional(name = p_name ,status = "Requested" ,email = p_email , city = p_city,experiance = p_exp,password = p_password, categroy_id = p_cat)
                db.session.add(p)
                db.session.commit()
                return redirect("/login")
            else:
                return "User already exist"
    else:
        return "url not found"        
    

@app.route("/dashboard/admin" , methods=["GET" ,"POST"])
@login_required
def admin_dash():
    if isinstance(current_user,Admin):
        if request.method == "GET":
            cats = db.session.query(ServiceCategory).all()
            active_prof = db.session.query(Professional).filter_by(status="Active").all()
            request_prof = db.session.query(Professional).filter_by(status="Requested").all()
            flagged_prof = db.session.query(Professional).filter_by(status="Flagged").all()
            active_cust = db.session.query(Customer).filter_by(status="Active").all()
            flagged_cust = db.session.query(Customer).filter_by(status="Flagged").all()
            return render_template("admin/dashboard.html" , cu = current_user,cats = cats , active_prof = active_prof, flagged_prof=flagged_prof,request_prof=request_prof,active_cust = active_cust, flagged_cust=flagged_cust ,page = "dash" )
        elif request.method == "POST":
            if request.args.get("job") =="create":
                cat_name = request.form.get("cat_name")
                cat_desc = request.form.get("cat_desc")
                cat_price = request.form.get("cat_price")
                if cat_name and cat_desc and  cat_price:
                    cat = db.session.query(ServiceCategory).filter_by(name = cat_name).first()
                    if not cat:
                        new_cat = ServiceCategory(name = cat_name , descripiton = cat_desc, base_price = cat_price)
                        db.session.add(new_cat)
                        db.session.commit()
                        
                        return redirect("/dashboard/admin")
                    else : 
                        flash("Category alerady exist","warning")
                        return redirect("/dashboard/admin")
                else:
                    flash("Important fields missing","warning")
                    return redirect("/dashboard/admin")
            elif request.args.get("job") == "editcat":

                cat_id = request.args.get('id')
                name = request.form.get("cat_name")
                desc = request.form.get("cat_desc")
                price = request.form.get("cat_price")
                cat = db.session.query(ServiceCategory).filter_by(id = cat_id).first()
                if name:
                    cat.name = name
                if desc:
                    cat.descripiton = desc
                if price:
                    cat.base_price = price
                db.session.commit()
                flash("category is updated" ,"success")
                return redirect("/dashboard/admin")
            if request.args.get("job") == "acceptprof":
                id  = request.args.get("id")
                prof = db.session.query(Professional).filter_by(id = id).first()
                prof.status = "Active"
                db.session.commit()
                flash("Professional request is accepted" ,"success")
                return redirect("/dashboard/admin")
            if request.args.get("job") == "rejectprof":
                id  = request.args.get("id")
                prof = db.session.query(Professional).filter_by(id = id).first()
                prof.status = "Rejected"
                db.session.commit()
                flash("Professional request is Rejected" ,"danger")
                return redirect("/dashboard/admin")
            if request.args.get("job") == "flagprof":
                id  = request.args.get("id")
                prof = db.session.query(Professional).filter_by(id = id).first()
                prof.status = "Flagged"
                db.session.commit()
                flash("Professional is Flagged" ,"danger")
                return redirect("/dashboard/admin")
            if request.args.get("job") == "unflagprof":
                id  = request.args.get("id")
                prof = db.session.query(Professional).filter_by(id = id).first()
                prof.status = "Active"
                db.session.commit()
                flash("Professional is UnFlagged" ,"danger")
                return redirect("/dashboard/admin")
            if request.args.get("job") == "flagcust":
                id  = request.args.get("id")
                prof = db.session.query(Customer).filter_by(id = id).first()
                prof.status = "Flagged"
                db.session.commit()
                flash("Customer is Flagged" ,"danger")
                return redirect("/dashboard/admin")
            if request.args.get("job") == "unflagcust":
                id  = request.args.get("id")
                prof = db.session.query(Customer).filter_by(id = id).first()
                prof.status = "Active"
                db.session.commit()
                flash("Customer is UnFlagged" ,"danger")
                return redirect("/dashboard/admin")
    else:
        return "you are not authorised to go to this url"
    

@app.route("/search/admin" , methods = ["GET" , "POST"])
@login_required
def admin_search():
    if isinstance(current_user, Admin):
        if request.method=="GET":
            return render_template("/admin/search.html" , page = "search")
        elif request.method=="POST":
            utype= request.form.get("u_type")
            n_keyword = request.form.get("name_keyword")
            if utype == "cust":
                users = db.session.query(Customer).filter(Customer.name.ilike(f'%{n_keyword}%')).all()
            elif utype=="prof"   :
                users = db.session.query(Professional).filter(Professional.name.ilike(f'%{n_keyword}%')).all()
            return render_template("/admin/search.html" , page = "search",users=users , utype=utype)

@app.route("/stats/admin" , methods =["GET" , "POST"])    
@login_required
def admin_stas():
    if isinstance(current_user,Admin):
        cats = db.session.query(ServiceCategory).all()
        counts = []
        label = []
        for cat in cats:
            count =0
            label.append(cat.name)
            for i in cat.all_plans:
                count+=len(i.assoiciated_booking)
            counts.append(count)
            
            
        plt.bar(label, counts)
        plt.xlabel("Categories")
        plt.ylabel("Count")
        plt.title("Category wise booking count")
        plt.savefig("./static/admin/admin_book_count.png")
        plt.close()
        

        return render_template("/admin/stats.html" , page = "stats")

@app.route("/dashboard/customer" , methods=["GET" ,"POST"])
@login_required
def cust_dash():
    if isinstance(current_user , Customer):
        categories = db.session.query(ServiceCategory).all() 
        bookings = db.session.query(Booking).filter_by(customer_id = current_user.id).all()
        return render_template("/customer/dashboard.html" , page = "dashboard" , cu = current_user, categories = categories, bookings = bookings)


@app.route("/customer/search" , methods = ["GET" , "POST"])
@login_required
def cust_search():
    if isinstance(current_user,Customer):
        if request.method == "GET" and not request.args :
            cats = db.session.query(ServiceCategory).all()
            return  render_template("/customer/search.html" , page= "search" , cu = current_user , cats = cats)
        

        if request.method == "GET" and request.args.get("catname"):
            catname = request.args.get("catname")
            cat = db.session.query(ServiceCategory).filter_by(name = catname).first()
            plans = []
            for plan in cat.all_plans:
                if current_user.city == plan.professional.city :
                    plans.append(plan)
            
            cats = db.session.query(ServiceCategory).all()
            return render_template("/customer/search.html" , cu = current_user , catname = catname , page = "search" , plans = plans , cats= cats)
        if request.method=="POST" :
            cats = db.session.query(ServiceCategory).all()
            cat_id = request.form.get("category")
            plan_keyword = request.form.get("plan_keyword")
            
            service_plans = db.session.query(ServicePlan).filter( and_(ServicePlan.categroy_id == cat_id , 
                                                                       or_(
                                                                       ServicePlan.name.ilike(f"%{plan_keyword}%" ) ,
                                                                       ServicePlan.descripiton.ilike(f"%{plan_keyword}%" ) 
                                                                       ))  ).all()
            print(service_plans)
            plans = []
            for plan in service_plans:
                if current_user.city == plan.professional.city:
                    plans.append(plan)
            print(plans)
            return render_template("/customer/search.html" , cu = current_user , page = "search" , plans = plans, cats= cats)

@app.route("/dashboard/professional" , methods=["GET" ,"POST"])
@login_required
def prof_dash():
    if isinstance(current_user,Professional):
        if request.method=="GET":
            plans = db.session.query(ServicePlan).filter_by(professional_id = current_user.id).all()
            bookings = current_user.recive_bookings
            # Requested , Accepted / Rejected , In Progress , Done ,  Closed

            todays_bookings = []
            accepted_bookings = []
            requested_bookings = []
            other_bookings = []
          
            for booking in bookings:
                if not booking.status == "Closed"  and not booking.status == "Rejected" and not booking.status=="Requested" and booking.date == datetime.now().strftime("%d-%m-%Y"):
                    todays_bookings.append(booking)
                elif booking.status == "Accepted":
                    accepted_bookings.append(booking)
                elif booking.status == "Requested":
                    requested_bookings.append(booking)
                else:
                    other_bookings.append(booking)
            print(todays_bookings)
            return render_template("/professional/dashboard.html" , todays_bookings = todays_bookings, accepted_bookings =accepted_bookings , requested_bookings = requested_bookings,other_bookings = other_bookings, page="dash" , cu = current_user , plans = plans)
        elif request.method == "POST":
            if request.args.get("job")== "create":
                p_name = request.form.get("plan_name") #Weed Removal
                p_desc = request.form.get("plan_desc")
                p_price = request.form.get("plan_price")
                plan = db.session.query(ServicePlan).filter_by(name = p_name , professional_id = current_user.id ).first()
                if plan:
                    flash("A plan already exist with the same name","danger")
                    return redirect("/dashboard/professional")
                else:
                    p = ServicePlan(name = p_name , descripiton = p_desc , price = p_price , categroy_id = current_user.categroy_id , professional_id = current_user.id)
                    db.session.add(p)
                    db.session.commit()
                    flash("service plan created" , "success")
                    return redirect("/dashboard/professional")
            elif request.args.get("job") == "editplan":

                plan_id = request.args.get('id')
                name = request.form.get("plan_name")
                desc = request.form.get("plan_desc")
                price = request.form.get("plan_price")
                plan = db.session.query(ServicePlan).filter_by(id = plan_id).first()
                if name:
                    plan.name = name
                if desc:
                    plan.descripiton = desc
                if price:
                    plan.price = price
                db.session.commit()
                flash("Plan is updated" ,"success")
                return redirect("/dashboard/professional")

@app.route("/search/professional" , methods = ["GET" , "POST"])
@login_required
def prof_search():
    if isinstance(current_user, Professional):
        return render_template("/professional/search.html" , page = "search", cu = current_user)
    


@app.route("/booking" , methods=["GET" ,"POST"])
def booking():
    if isinstance(current_user,Professional):
        if request.args.get("job") == "accept":
            id = request.args.get("id")
            booking = db.session.query(Booking).filter_by(id = id).first()
            booking.status = "Accepted"
            db.session.commit()
            flash("booking request is accepted" , "success")
            return redirect("/dashboard/professional")
        
        elif request.args.get("job") == "reject":
            id = request.args.get("id")
            booking = db.session.query(Booking).filter_by(id = id).first()
            booking.status = "Rejected"
            db.session.commit()
            flash("booking request is Rejected" , "warning")
            return redirect("/dashboard/professional")
        elif request.args.get("job") == "start":
            id = request.args.get("id")
            booking = db.session.query(Booking).filter_by(id = id).first()
            booking.status = "In Progress"
            db.session.commit()
            flash("booking fullfillment is Started" , "success")
            return redirect("/dashboard/professional")
        elif request.args.get("job") == "done":
            id = request.args.get("id")
            booking = db.session.query(Booking).filter_by(id = id).first()
            booking.status = "Done"
            db.session.commit()
            flash("booking is done" ,"success")
            return redirect("/dashboard/professional")
    elif isinstance(current_user,Customer):
        
        if request.args.get("job") =="book":
            
            plan_id = request.args.get("p_id")
            prof_id = request.args.get("prof_id")
            date = request.form.get("book_date")
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            formated_Date = datetime.strftime(date_obj , "%d-%m-%Y")
            
            time = request.form.get("book_time")
            book = Booking(date= formated_Date,time= time , professional_id = prof_id ,status = "Requested" ,  service_plan_id = plan_id, customer_id = current_user.id)
            db.session.add(book)
            db.session.commit()
            flash("Booking request created" , "success")
            return redirect("/dashboard/customer")
        if request.args.get("job") =="edit":
            
            id = request.args.get("id")
            date = request.form.get("book_date")
            time = request.form.get("book_time")
            booking = db.session.query(Booking).filter_by(id = id).first()
            if date:
                booking.date = date
            if time:
                booking.time = time
            db.session.commit()
            flash("Booking request is updated" , "success")
            return redirect("/dashboard/customer")
        if request.args.get("job") =="close":
            
            id = request.args.get("id")
            rating = request.args.get("rating")
            booking = db.session.query(Booking).filter_by(id = id).first()
            booking.rating= rating
            booking.status="Closed"
            db.session.commit()
            flash("Booking is Closed" , "success")
            return redirect("/dashboard/customer")



@app.route("/logout" , methods=["GET"])
@login_required
def log_out():

    logout_user()
    return redirect("/login")

