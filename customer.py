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
