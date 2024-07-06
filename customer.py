import pymysql


# 顾客类
class Customer:
    def __init__(self, customer_id, username, password, cust_phone):
        self.customer_id = customer_id
        self.username = username
        self.password = password
        self.cust_phone = cust_phone

    def insert_into_db(self):
        # 连接数据库
        connection = pymysql.connect(
            host='localhost',
            user='food_root_user',
            password='Aa123456_',
            database='sleepyfood'
        )

        try:
            # 创建游标对象
            cursor = connection.cursor()

            # 执行插入语句
            insert_query = "INSERT INTO Customer (username, password, cust_phone) " \
                           "VALUES (%s, %s, %s)"
            values = (self.username, self.password, self.cust_phone)
            cursor.execute(insert_query, values)

            # 提交事务
            connection.commit()

            print("顾客信息插入成功！")

        except Exception as e:
            # 发生错误时回滚事务
            connection.rollback()
            print("顾客信息插入失败:", e)

        finally:
            # 关闭游标和数据库连接
            cursor.close()
            connection.close()


def create_customer(username, password, cust_phone):
    # 创建顾客对象
    customer = Customer(
        customer_id=None,  # customer_id是自增字段，插入时不需要提供值
        username=username,
        password=password,
        cust_phone=cust_phone
    )
    # 插入顾客信息到数据库
    customer.insert_into_db()

def get_customer_id(user_phone):
    # 连接数据库
    connection = pymysql.connect(
        host='localhost',
        user='food_root_user',
        password='Aa123456_',
        database='sleepyfood'
    )
    try:
        cursor = connection.cursor()
        query = "SELECT customer_id FROM customer" \
                       " WHERE cust_phone = %s"
        cursor.execute(query, (user_phone,))
        result = cursor.fetchone()
        if result:
            print("顾客id获取成功！")
            return result[0]
        else:
            return -1
    finally:
        # 关闭游标和数据库连接
        cursor.close()
        connection.close()


def login_customer(cust_phone, password):
    connection = pymysql.connect(
        host='localhost',
        user='food_root_user',
        password='Aa123456_',
        database='sleepyfood'
    )
    try:
        with connection.cursor() as cursor:
            # Check if the customer with cust_phone exists in the database
            sql = "SELECT * FROM customer WHERE cust_phone=%s"
            cursor.execute(sql, (cust_phone,))
            result = cursor.fetchone()
            print(result)
            if result:
                # Customer exists, now check if the password matches
                stored_password = result[2]
                if stored_password == password:
                    return True
                else:
                    # Password is incorrect
                    return False
            else:
                print("no")
                return False

    finally:
        connection.close()


# 从数据库中获取商家名称列表
def get_all_merchants():
    connection = pymysql.connect(
        host='localhost',
        user='food_root_user',
        password='Aa123456_',
        database='sleepyfood'
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM merchant"
            cursor.execute(sql)
            result = cursor.fetchall()
            merchants = []
            for row in result:
                # 假设 row[0] 是商家 ID，row[4] 是商家名称
                merchants.append({
                    'id': row[0],
                    'name': row[4]
                })
            return merchants
    finally:
        connection.close()
# 从数据库中获取指定商家的商品列表
def get_products_by_merchant(merchant_id):
    connection = pymysql.connect(
        host='localhost',
        user='food_root_user',
        password='Aa123456_',
        database='sleepyfood'
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM menu WHERE merchant_id = %s"
            cursor.execute(sql, (merchant_id,))
            result = cursor.fetchall()
            products = []
            for row in result:
                # 假设 row[0] 是商品 ID，row[1] 是商品名称
                products.append({
                    'id': row[0],
                    'name': row[2]
                })
            return products
    finally:
        connection.close()

# 生成订单
def generate_order(customer_id, merchant_id,total_price,cus_address):
    connection = pymysql.connect(
        host='localhost',
        user='food_root_user',
        password='Aa123456_',
        database='sleepyfood'
    )
    try:
        cursor = connection.cursor()
        # 执行插入语句
        insert_query = "INSERT INTO orders (customer_id, merchant_id,total_price,cus_address) " \
                       "VALUES (%s, %s, %s, %s)"
        values = (customer_id, merchant_id,total_price,cus_address)
        cursor.execute(insert_query, values)
        connection.commit()
        print("订单信息插入成功！1")
        query = "SELECT order_id FROM orders WHERE customer_id = %s AND merchant_id = %s AND total_price = %s AND cus_address = %s"
        cursor.execute(query, (customer_id, merchant_id, total_price, cus_address,))
        print("订单信息插入成功！2")
        result = cursor.fetchone()
        return result[0] # 返回订单编号
    except Exception as e:
        # 发生错误时回滚事务
        connection.rollback()
        print("订单信息插入失败:", e)
        return -1
    finally:
        # 关闭游标和数据库连接
        cursor.close()
        connection.close()

# 某种商品的价格
def calculate_price(merchant_id,productName,quantity):
    total_price = 0
    connection = pymysql.connect(
        host='localhost',
        user='food_root_user',
        password='Aa123456_',
        database='sleepyfood'
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT price FROM menu WHERE merchant_id = %s AND name = %s"
            cursor.execute(sql, (merchant_id,productName))
            result = cursor.fetchall()
            return float(result[0][0])*quantity
    finally:
        connection.close()

# 获取商品id
def get_menu_item_id(merchant_id,productName):
    connection = pymysql.connect(
        host='localhost',
        user='food_root_user',
        password='Aa123456_',
        database='sleepyfood'
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT menu_item_id FROM menu WHERE merchant_id = %s AND name = %s"
            cursor.execute(sql, (merchant_id, productName))
            result = cursor.fetchall()
            if result:
                return int(result[0][0]) # 商品id
            else:
                return -1
    finally:
        connection.close()

# 订单明细
def generate_order_details(order_id,menu_item_id,menu_item_count):
    connection = pymysql.connect(
        host = 'localhost',
        user = 'food_root_user',
        password='Aa123456_',
        database='sleepyfood'
    )
    try:
        cursor = connection.cursor()
        # 执行插入语句
        insert_query = "INSERT INTO orderdetail (order_id,menu_item_id,menu_item_count) " \
                       "VALUES (%s, %s, %s)"
        values = (order_id,menu_item_id,menu_item_count)
        cursor.execute(insert_query, values)
        connection.commit()
        print("订单细节信息插入成功！")
    except Exception as e:
        # 发生错误时回滚事务
        connection.rollback()
        print("订单细节信息插入失败:", e)
    finally:
        # 关闭游标和数据库连接
        cursor.close()
        connection.close()

def customer_get_all_orders(customer_id):
    connection = pymysql.connect(
        host='localhost',
        user='food_root_user',
        password='Aa123456_',
        database='sleepyfood'
    )
    try:
        with connection.cursor() as cursor:
            sql = """
                        SELECT o.order_id, o.customer_id, o.total_price, od.menu_item_count, m.name,o.cus_address,mer.shop_name
                        FROM Orders o
                        JOIN OrderDetail od ON o.order_id = od.order_id
                        JOIN Menu m ON od.menu_item_id = m.menu_item_id
                        JOIN merchant mer ON o.merchant_id = mer.merchant_id
                        WHERE o.customer_id = %s
                        """

            cursor.execute(sql, (customer_id,))
            result = cursor.fetchall()
            orders = []
            for row in result:
                orders.append({
                    'order_id': row[0],
                    'customer_id': row[1],
                    'total_price': row[2],
                    'menu_item_count': row[3],
                    'menu_name': row[4],
                    'cus_address':row[5],
                    'shop_name':row[6],
                })
            return orders
    finally:
        connection.close()

# 顾客地址类
class CustomerAddress:
    def __init__(self, customer_id, user_address):
        self.customer_id = customer_id
        self.user_address = user_address

    def insert_into_db(self):
        # 连接数据库
        connection = pymysql.connect(
            host='localhost',
            user='food_root_user',
            password='Aa123456_',
            database='sleepyfood'
        )

        try:
            # 创建游标对象
            cursor = connection.cursor()
            # 执行插入语句
            insert_query = "INSERT INTO CustomerAddress (customer_id, user_address) " \
                           "VALUES (%s, %s)"
            values = (self.customer_id, self.user_address)
            cursor.execute(insert_query, values)

            # 提交事务
            connection.commit()

            print("顾客地址信息插入成功！")

        except Exception as e:
            # 发生错误时回滚事务
            connection.rollback()
            print("顾客地址信息插入失败:", e)

        finally:
            # 关闭游标和数据库连接
            cursor.close()
            connection.close()


def create_customer_address(customer_id, user_address):
    # 创建顾客地址对象
    customer_address = CustomerAddress(
        customer_id=customer_id,
        user_address=user_address
    )
    # 插入顾客地址信息到数据库
    customer_address.insert_into_db()

# 从数据库中获取地址列表
def get_all_address(customer_id):
    connection = pymysql.connect(
        host='localhost',
        user='food_root_user',
        password='Aa123456_',
        database='sleepyfood'
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM customeraddress WHERE customer_id = %s"
            cursor.execute(sql, (customer_id,))
            result = cursor.fetchall()
            address = []
            for row in result:
                # 假设 row[0] 是商品 ID，row[1] 是商品名称
                address.append({
                    'id': row[0],
                    'address': row[2]
                })
            return address
    finally:
        connection.close()

# 删除顾客地址的函数
def delete_customer_address(address_id):
    try:
        # 连接 MySQL 数据库
        connection = pymysql.connect(
            host='localhost',
            user='food_root_user',
            password='Aa123456_',
            database='sleepyfood'
        )

        with connection.cursor() as cursor:
            delete_query = "DELETE FROM customeraddress WHERE address_id = %s"
            cursor.execute(delete_query, (address_id,))
            connection.commit()
            print(f"Deleted customer address with address_id {address_id} successfully.")
            return True

    except pymysql.Error as e:
        # 发生错误时回滚事务
        print(f"Error deleting customer address: {e}")
        connection.rollback()
        return False

    finally:
        if connection:
            connection.close()


# Example usage:
# delete_customer_address(123)  # Replace 123 with the actual address_id you want to delete


if __name__ == "__main__":
    # # 从键盘输入顾客地址信息
    # customer_id = int(input("请输入顾客ID: "))
    # user_address = input("请输入顾客地址: ")
    #
    # create_customer_address(customer_id, user_address)
    # # 从键盘输入顾客信息
    # username = input("请输入用户名: ")
    # password = input("请输入密码: ")
    # cust_phone = input("请输入顾客电话号码: ")
    #
    # create_customer(username, password, cust_phone)

    print(get_all_merchants())
