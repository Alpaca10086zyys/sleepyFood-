from flask import Flask
from flask import jsonify
#导入Flask框架，这个框架可以快捷地实现了一个WSGI应用
from flask import render_template
#默认情况下，flask在程序文件夹中的templates子文件夹中寻找模块
from flask import request
#导入前台请求的request模块
from flask import redirect,url_for
import traceback
from customer import create_customer,login_customer,get_all_merchants,get_products_by_merchant
from merchant import create_merchant,login_merchant
from rider import create_rider,login_rider

# 传递根目录
app = Flask(__name__)

# login界面
@app.route('/')
def login():  # put application's code here
    return render_template('login.html')

@app.route('/gkzc')
def register_customer():
    return render_template('gkzc.html')

@app.route('/register_customer', methods=['POST'])
def register_customer_post():
    try:
        username = request.form['username']
        phone = request.form['phone']
        password = request.form['password']

        # 打印输入数据
        print("Received data:", username, phone, password)

        # 创建并插入顾客信息到数据库
        create_customer(username, password, phone)
        # return redirect(url_for('顾客注册成功'))
        return "顾客注册成功"

    except Exception as e:
        print("顾客注册失败:", e)
        print(traceback.format_exc())
        return "顾客注册失败，请重试。"

# 商家注册路由
@app.route('/sjzc')
def register_merchant():
    return render_template('sjzc.html')

@app.route('/register_merchant', methods=['POST'])
def register_merchant_post():
    try:
        merchant_phone = request.form['phone']
        merchant_identity = request.form['id_number']
        password = request.form['password']
        shop_name = request.form['shop_name']
        shop_address = request.form['address']
        management_licence_id = request.form['license_number']


        # 创建并插入顾客信息到数据库
        create_merchant(merchant_phone, merchant_identity,password, shop_name, shop_address, management_licence_id)
        # return redirect(url_for('顾客注册成功'))
        return "商家注册成功"

    except Exception as e:
        print("商家注册失败:", e)
        print(traceback.format_exc())
        return "商家注册失败，请重试。"

# 骑手注册路由
@app.route('/qszc')
def register_rider():
    return render_template('qszc.html')

@app.route('/register_rider', methods=['POST'])
def register_rider_post():
    try:
        rider_identity = request.form['id_number']
        licence_plate = request.form['car_number']
        username = request.form['name']
        password = request.form['password']
        rider_phone = request.form['phone']

        # 创建并插入骑手信息到数据库
        create_rider(rider_identity,rider_phone,username,username,password)
        # return redirect(url_for('顾客注册成功'))
        return "骑手注册成功"

    except Exception as e:
        print("骑手注册失败:", e)
        print(traceback.format_exc())
        return "骑手注册失败，请重试。"

@app.route('/login', methods=['POST'])
def login_post():
    user_type = request.form['type']
    user_phone = request.form['phone']
    password = request.form['password']
    try:
        print(user_type)
        if user_type == 'customer':
            print("是顾客")
            if login_customer(user_phone, password):
                return redirect(url_for('customer_dashboard')) # 后面改成顾客页
            else:
                return "顾客登录失败，请重试。"
        elif user_type == 'merchant':
            if login_merchant(user_phone, password):
                return redirect(url_for('merchant_dashboard')) # 后面改成商家页
            else:
                return "商家登录失败，请重试。"
        elif user_type == 'rider':
            if login_rider(user_phone, password):
                return redirect(url_for('rider_dashboard')) # 骑手页
            else:
                return "骑手登录失败，请重试。"
        else:
            return "无效的用户类型。"
    except Exception as e:
        print("登录失败:", e)
        print(traceback.format_exc())
        return "登录失败，请重试。"

@app.route('/customer_dashboard')
def customer_dashboard():
    return render_template('customer_restaurant.html')
@app.route('/customer_order')
def customer_order():
    return render_template('customer_order.html')
@app.route('/customer_home')
def customer_home():
    return render_template('customer_home.html')

@app.route('/get_all_merchants')
def get_merchants():
    try:
        merchants = get_all_merchants()
        return jsonify(merchants)
    except Exception as e:
        print("Error fetching merchants:", e)
        return jsonify({"error": "Error fetching merchants"}), 500

@app.route('/products/<int:merchant_id>')
def get_products(merchant_id):
    try:
        products = get_products_by_merchant(merchant_id)
        return jsonify(products)
    except Exception as e:
        print("Error fetching products:", e)
        return jsonify({"error": "Error fetching products"}), 500

@app.route('/merchant_dashboard')
def merchant_dashboard():
    return "商家界面"
@app.route('/merchant_order')
def merchant_order():
    return render_template('merchant_order.html')
@app.route('/merchant_menu')
def merchant_menu():
    return render_template('merchant_menu.html')


@app.route('/rider_dashboard')
def rider_dashboard():
    return "骑手界面"
@app.route('/rider_order')
def rider_order():
    return render_template('rider_order.html')
@app.route('/rider_map')
def rider_map():
    return render_template('rider_map.html')

if __name__ == '__main__':
    app.run()