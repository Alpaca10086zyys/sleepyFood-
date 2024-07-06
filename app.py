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
from customer import get_all_address,create_customer_address,delete_customer_address
from customer import get_customer_id
from customer import generate_order_details,generate_order
from customer import calculate_price,get_menu_item_id,customer_get_all_orders

from merchant import create_merchant, login_merchant, get_all_foods, get_merchant_id, insert_food, \
    merchant_get_all_orders, set_rider
from rider import create_rider, login_rider,get_rider_id,rider_get_all_orders,recover_rider_status



# 传递根目录
app = Flask(__name__)
customer_id = -1
cus_merchant_id = -1
merchant_id = 0
rider_id = 0
# login界面
@app.route('/')
def cover():  # put application's code here
    return render_template('cover.html')

@app.route('/login')
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
        global customer_id
        customer_id = get_customer_id(phone)
        return render_template("customer_restaurant.html")

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

        # 创建并插入商家信息到数据库
        create_merchant(merchant_phone, merchant_identity,password, shop_name, shop_address, management_licence_id)
        #### 这里一定要加自动跳转，啊啊啊啊等会再加
        global merchant_id
        merchant_id = get_merchant_id(merchant_phone)
        return render_template("merchant_menu.html")

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
        global rider_id
        rider_id = get_rider_id(rider_phone)
        return render_template("rider_order.html")

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
                global customer_id
                customer_id=get_customer_id(user_phone)
                return redirect(url_for('customer_dashboard')) # 后面改成顾客页
            else:
                return "顾客登录失败，请重试。"
        elif user_type == 'merchant':
            if login_merchant(user_phone, password):
                global merchant_id
                merchant_id = get_merchant_id(user_phone)
                return redirect(url_for('merchant_dashboard')) # 后面改成商家页
            else:
                return "商家登录失败，请重试。"
        elif user_type == 'rider':
            if login_rider(user_phone, password):
                global rider_id
                rider_id = get_rider_id(user_phone)
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

# 顾客界面打印菜单
@app.route('/products/<int:merchant__id>')
def get_products(merchant__id):
    print("ok")
    try:
        products = get_products_by_merchant(merchant__id)
        global cus_merchant_id
        cus_merchant_id = merchant__id
        print(merchant__id)
        return jsonify(products)
    except Exception as e:
        print("Error fetching products:", e)
        return jsonify({"error": "Error fetching products"}), 500

# 顾客界面打印订单
@app.route('/customer_get_all_orders')
def customer_get_all_order():
    # global customer_id
    # print(customer_get_all_orders(customer_id))
    return jsonify(customer_get_all_orders(customer_id))

@app.route('/add_address', methods=['POST'])
def add_address():
    data = request.get_json()
    address = data.get('address')
    if not address or customer_id==-1:
        return jsonify({'success': False, 'message': 'Customer ID and address are required'}), 400
    try:
        create_customer_address(customer_id, address)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/get_addresses', methods=['GET'])
def get_addresses():
    # 假设从数据库获取地址信息的代码，这里用一个示例列表代替
    addresses = get_all_address(customer_id)
    # addresses = ['地址1', '地址2', '地址3']  # 替换为实际从数据库获取的地址列表
    return jsonify(addresses)

# 删除地址的路由处理函数
@app.route('/delete_address/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    try:
        # 调用 delete_cus_address 函数来删除地址
        result = delete_customer_address(address_id)  # 假设这是你的删除地址函数
        if result:
            return jsonify({'message': 'Address deleted successfully'}), 200
        else:
            return jsonify({'message': 'Address not found'}), 404

    except Exception as e:
        return jsonify({'message': 'Error deleting address', 'error': str(e)}), 500



# 提交订单
@app.route('/submit-cart', methods=['POST'])
def customer_submit_order():
    try:
        data = request.json
        cart_items = data['cart_items']
        address = data['address']

        # 处理逻辑，如存储到数据库
        total_price = 0
        for item in cart_items:
            total_price += calculate_price(cus_merchant_id,item['name'],int(item['quantity']))
        order_id = generate_order(customer_id,cus_merchant_id,total_price,address)
        for item in cart_items:
            generate_order_details(order_id,int(get_menu_item_id(cus_merchant_id,item['name'])),int(item['quantity']))
        return '购物车提交成功'

    except Exception as e:
        print("购物车提交失败:", e)
        print(traceback.format_exc())
        return "购物车提交失败，请重试。"


@app.route('/merchant_dashboard')
def merchant_dashboard():
    print("merchant_dashboard")
    return render_template('merchant_menu.html')

@app.route('/get_all_foods')
def foods():
    global merchant_id
    return jsonify(get_all_foods(merchant_id))
@app.route('/send_food', methods=['POST'])
def send_foods():
    data = request.get_json()
    name = data['name']
    price = data['price']
    print(name)
    print(price)

    # 处理数据的逻辑代码

    global merchant_id
    print(merchant_id)
    insert_food(merchant_id, name, price)
    response = {'message': 'Data received successfully'}
    return jsonify(response)

@app.route('/merchant_order')
def merchant_order():
    return render_template('merchant_order.html')
@app.route('/merchant_send_state', methods=['POST'])
def send_state():
    try:
        data = request.get_json()
        state = data['state']
        order_id = data['order_id']

        if state == 'ok':
            set_rider(order_id)

        response = {'message': 'Data received successfully'}
        return jsonify(response)

    except Exception as e:
        response = {'message': 'Invalid data format'}
        return jsonify(response), 400
@app.route('/merchant_get_all_orders')
def merchant_get_all_order():
    global merchant_id
    print(merchant_get_all_orders(merchant_id))
    return jsonify(merchant_get_all_orders(merchant_id))

@app.route('/rider_dashboard')
def rider_dashboard():
    return render_template("rider_order.html")

@app.route('/rider_map')
def rider_map():
    return render_template('rider_map.html')
@app.route('/rider_get_all_orders')
def rider_get_all_order():
    global rider_id
    print('rider_id',rider_id)
    print(rider_get_all_orders(rider_id))
    return jsonify(rider_get_all_orders(rider_id))
@app.route('/rider_send_state', methods=['POST'])
def rider_send_state():
    try:
        data = request.get_json()
        state = data['state']
        order_id = data['order_id']

        if state == 'ok':
            recover_rider_status(order_id)

        response = {'message': 'Data received successfully'}
        return jsonify(response)

    except Exception as e:
        response = {'message': 'Invalid data format'}
        return jsonify(response), 400
if __name__ == '__main__':
    app.run()