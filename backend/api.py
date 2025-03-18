from flask_restful import Resource, Api
from .models import db,ServiceCategory
from flask import request

api = Api()



class Servicecategory(Resource):
    def get(self):
        all_cat = db.session.query(ServiceCategory).all()
        cats = []
        for i in all_cat:
            cats.append({"name":i.name , "base_price": i.base_price})

        return cats, 200
    def post(self):
        name = request.json.get("cat_name")
        base_price = request.json.get("cat_price")
        desc = request.json.get("cat_desc")
        if name and base_price and desc:
            cat = ServiceCategory(name = name , base_price = base_price, descripiton = desc)
            db.session.add(cat)
            db.session.commit()
            return {"message":"Service Category is Created"} , 200
        else:
            return {"message" : "Input missing"} , 400
    

api.add_resource(Servicecategory,"/api/categories" , "/api/category")
