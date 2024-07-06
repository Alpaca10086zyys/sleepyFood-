import pymysql


class Rider:
    def __init__(self, rider_id, rider_identity, rider_phone,username, licence_plate, password, status=False):
        self.rider_id = rider_id
        self.rider_identity = rider_identity
        self.rider_phone = rider_phone
        self.username = username
        self.licence_plate = licence_plate
        self.password = password
        self.status = status


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
            print("Connected successfully")
            # 执行插入语句
            insert_query = "INSERT INTO Rider (rider_identity, rider_phone , username, licence_plate, password, status) " \
                           "VALUES (%s, %s, %s, %s, %s, %s)"
            values = (self.rider_identity, self.rider_phone,self.username, self.licence_plate, self.password, self.status)
            cursor.execute(insert_query, values)

            # 提交事务
            connection.commit()

            print("骑手信息插入成功！")

        except Exception as e:
            # 发生错误时回滚事务
            connection.rollback()
            print("骑手信息插入失败:", e)

        finally:
            # 关闭游标和数据库连接
            cursor.close()
            connection.close()


def create_rider(rider_identity, rider_phone,licence_plate, username, password):
    # 创建骑手对象
    rider = Rider(
        rider_id=None,  # rider_id是自增字段，插入时不需要提供值
        rider_identity=rider_identity,
        rider_phone= rider_phone,
        username=username,
        licence_plate=licence_plate,
        password=password,
        status=True  # 初始状态为空闲
    )
    # 插入骑手信息到数据库
    rider.insert_into_db()

# 骑手登录
def  login_rider(rider_phone,password):
    connection = pymysql.connect(
        host='localhost',
        user='food_root_user',
        password='Aa123456_',
        database='sleepyfood'
    )
    try:
        with connection.cursor() as cursor:
            # Check if the customer with cust_phone exists in the database
            sql = "SELECT * FROM rider WHERE rider_phone=%s"
            cursor.execute(sql, (rider_phone,))
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
                return False

    finally:
        connection.close()

def get_rider_id(rider_phone):
    connection = pymysql.connect(
        host='localhost',
        user='food_root_user',
        password='Aa123456_',
        database='sleepyfood'
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM rider where rider_phone=%s"
            cursor.execute(sql,(rider_phone,))
            result = cursor.fetchall()
            return result[0][0]
    finally:
        connection.close()

def rider_get_all_orders(rider_id):
    connection = pymysql.connect(
        host='localhost',
        user='food_root_user',
        password='Aa123456_',
        database='sleepyfood'
    )
    try:
        with connection.cursor() as cursor:
            sql = """
                        SELECT order_id,cus_address,shop_address,order_status
                        FROM Orders
                        WHERE rider_id = %s
                        """
            cursor.execute(sql, (rider_id,))
            result = cursor.fetchall()
            orders = []
            for row in result:
                orders.append({
                    'order_id': row[0],
                    'cus_address': row[1],
                    'shop_address': row[2],
                    'order_status': row[3]
                })
            return orders
    finally:
        connection.close()
def recover_rider_status(order_id):
    connection = pymysql.connect(
        host='localhost',
        user='food_root_user',
        password='Aa123456_',
        database='sleepyfood'
    )
    try:
        with connection.cursor() as cursor:
            sql = """SELECT rider_id FROM Orders WHERE order_id = %s"""
            cursor.execute(sql, (order_id,))
            rider_id=cursor.fetchall()[0][0]
            print('rider_id', rider_id)
            cursor.execute("UPDATE rider SET status = True WHERE rider_id = %s", (rider_id,))
            cursor.execute("UPDATE orders SET order_status = 2 WHERE order_id = %s", (order_id,))
            connection.commit()
            # print(rider_id)
            cursor.execute("SELECT * FROM rider WHERE rider_id = %s", (rider_id,))
            result = cursor.fetchone()
            # print(result)
    except Exception as e:
        # 发生错误时回滚事务
        connection.rollback()
        print("Error:", e)
    finally:
        connection.close()


if __name__ == "__main__":
    # 从键盘输入骑手信息
    rider_identity = input("请输入骑手身份证号码: ")
    licence_plate = input("请输入骑手车牌号: ")
    username = input("请输入骑手姓名: ")
    password = input("请输入骑手密码: ")
    rider_phone = "123"

    # 创建骑手并插入数据库
    create_rider(rider_identity,rider_phone, licence_plate, username, password)
