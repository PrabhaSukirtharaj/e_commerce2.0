from flask import Flask
from flask_restful import Resource,Api,fields,abort,reqparse,marshal_with
from flask_sqlalchemy import SQLAlchemy
#from _datetime import datetime
app=Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tdp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.app_context().push()
db=SQLAlchemy(app)
class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    product_name=db.Column(db.String)
    price=db.Column(db.Integer)
    quality=db.Column(db.Integer)
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    price = db.Column(db.Integer)
    quality = db.Column(db.Integer)
    customer_name = db.Column(db.String)
    address=db.Column(db.String)
    status=db.Column(db.String)
class new_order(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    product=db.Column(db.String)
    price=db.Column(db.Integer)
    quality=db.Column(db.Integer)
    city=db.Column(db.String)
    place_order=db.Column(db.String)
    confirm_order=db.Column(db.String)


#class Customers(db.Model):
req_args_product=reqparse.RequestParser()
#req_args_product.add_argument("id",type=int,help="id is required",required="true")
req_args_product.add_argument("product_name",type=str)
req_args_product.add_argument("price",type=str)
req_args_product.add_argument("quality",type=str)
req_args_order=reqparse.RequestParser()
#req_args_product.add_argument("id",type=int,help="id is required",required="true")
req_args_order.add_argument("product_name",type=str)
req_args_order.add_argument("price",type=int)
req_args_order.add_argument("quality",type=int)
req_args_order.add_argument("customer_name",type=str)
req_args_order.add_argument("address",type=str)
req_args_order.add_argument("status",type=str)
req_args_neworder=reqparse.RequestParser()
req_args_neworder.add_argument("product",type=str)
req_args_neworder.add_argument("price",type=int)
req_args_neworder.add_argument("quality",type=int)
req_args_neworder.add_argument("city",type=str)
req_args_neworder.add_argument("place_order",type=str)
req_args_neworder.add_argument("confirm_order",type=str)

db.create_all()

e_product={
    "id": fields.Integer,
    "product_name": fields.String,
    "price": fields.Integer,
    "quality": fields.String,


}
e_order={
    "id":fields.Integer,
    "product_name":fields.String,
    "price":fields.Integer,
    "quality":fields.Integer,
    "customer_name" : fields.String,
    "address":fields.String,
    "status":fields.String,

}
e_neworder={
    "id":fields.Integer,
    "product":fields.String,
    "price":fields.Integer,
    "quality":fields.Integer,
    "city":fields.String,
    "place_order":fields.String,
    "confirm_order":fields.String,

}
class product_list(Resource):
    @marshal_with(e_product)
    def get(self):
        data=Product.query.all()
        return data
class product(Resource):
    @marshal_with(e_product)
    def get(self,pk):
        data=Product.query.filter_by(id=pk).first()
        return data
    @marshal_with(e_product)
    def post(self,pk):
        args=req_args_product.parse_args()
        data=Product.query.filter_by(id=pk).first()
        if data:
            abort(409,message="id already found")
        data_details=Product(id=pk,product_name=args['product_name'],price=args['price'],quality=args['quality'])
        db.session.add(data_details)
        db.session.commit()
        return data_details
    @marshal_with(e_product)
    def put(self,pk):
        args=req_args_product.parse_args()
        data=Product.query.filter_by(id=pk).first()
        if not data:
            abort(404,message="not found")
        if args['product_name']:
            data.product_name=args['product_name']
        if args['price']:
            data.price=args['price']
        if args['quality']:
            data.quality=args['quality']
        db.session.commit()
        return data
    @marshal_with(e_product)
    def delete(self,pk):
        data = Product.query.filter_by(id=pk).first()
        db.session.delete(data)
        db.session.commit()
        return "deleted"
class order_list(Resource):
    @marshal_with(e_order)
    def get(self):
        data=Order.query.all()
        return data
class order(Resource):
    @marshal_with(e_order)
    def get(self,pk):
        data=Order.query.filter_by(id=pk).first()
        if not data:
            abort(404,message="not found")
        return data
    @marshal_with(e_order)
    def post(self,pk):
        args=req_args_order.parse_args()
        data=Order.query.filter_by(id=pk).first()
        if data:
            abort(409,message='id already taken')
        order_details=Order(id=pk,product_name=args['product_name'],
                            price=args['price'],
                            quality=args['quality'],
                            customer_name=args['customer_name'],
                            address=args['address'],
                            status=args['status'])
        db.session.add(order_details)
        db.session.commit()
        return order_details
    @marshal_with(e_order)
    def delete(self,pk):
        data=Order.query.filter_by(id=pk).first()
        db.session.delete(data)
        db.commit(db)
        return "deleted"
class customer_orderlist(Resource):
    @marshal_with(e_neworder)
    def get(self):
        data=new_order.query.all()
        return data
class customer_order(Resource):
    @marshal_with(e_neworder)
    def get(self,pk):
        data=new_order.query.filter_by(id=pk).first()
        if not data:
            abort(404,message="not found")
        return data
    @marshal_with(e_neworder)
    def post(self,pk):
        args=req_args_neworder.parse_args()
        data=new_order.query.filter_by(id=pk).first()
        if data:
            abort(409,message="id already taken")
        data_details=new_order(id=pk,
                               product=args['product'],
                               price=args['price'],
                               quality=args['quality'],
                               city=args['city'],
                               place_order=args['place_order'],
                               confirm_order=args['confirm_order'])
        db.session.add(data_details)
        db.session.commit()
        return data_details
    
class Status(Resource):
    def get(self,pk):
        #args=req_args_order.parse_args()
        datas=Order.query.filter_by(id=pk).all()
        status={}
        for data in datas:
            status.update({"status":data.status})
            return status


api.add_resource(product,'/product/<int:pk>')
api.add_resource(product_list,'/product')
api.add_resource(order,'/order/<int:pk>')
api.add_resource(order_list,'/order')
api.add_resource(customer_orderlist,'/customer')
api.add_resource(customer_order,'/customer/<int:pk>')
api.add_resource(Status,'/status/<int:pk>')


if __name__=="__main__":
    app.run(debug=True,port=5002)





