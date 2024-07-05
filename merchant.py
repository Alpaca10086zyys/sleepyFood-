import pymysql

class Merchant:
    def __init__(self, merchant_id, merchant_phone, merchant_identity, password, shop_name, shop_address, management_licence_id):
        self.merchant_id = merchant_id
        self.merchant_phone = merchant_phone
        self.merchant_identity = merchant_identity
        self.password = password
        self.shop_name = shop_name
        self.shop_address = shop_address
        self.management_licence_id = management_licence_id


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
            print("connect successfully")
            # 执行插入语句
            insert_query = "INSERT INTO Merchant (merchant_phone, merchant_identity, password, shop_name, shop_address, management_licence_id) " \
                           "VALUES (%s, %s, %s, %s, %s, %s)"
            values = (self.merchant_phone, self.merchant_identity, self.password, self.shop_name, self.shop_address, self.management_licence_id)
            cursor.execute(insert_query, values)

            # 提交事务
            connection.commit()

            print("商家信息插入成功！")

        except Exception as e:
            # 发生错误时回滚事务
            connection.rollback()
            print("商家信息插入失败:", e)

        finally:
            # 关闭游标和数据库连接
            cursor.close()
            connection.close()

def create_merchant(merchant_phone,merchant_identity,password,shop_name,shop_address,management_licence_id):
    # 创建商家对象
    merchant = Merchant(
        merchant_id=None,  # merchant_id是自增字段，插入时不需要提供值
        merchant_phone=merchant_phone,
        merchant_identity=merchant_identity,
        password=password,
        shop_name=shop_name,
        shop_address=shop_address,
        management_licence_id=management_licence_id
    )
    # 插入商家信息到数据库
    merchant.insert_into_db()

def  login_merchant(merchant_phone,password):
    connection = pymysql.connect(
        host='localhost',
        user='food_root_user',
        password='Aa123456_',
        database='sleepyfood'
    )
    try:
        with connection.cursor() as cursor:
            # Check if the customer with cust_phone exists in the database
            sql = "SELECT * FROM merchant WHERE merchant_phone=%s"
            cursor.execute(sql, (merchant_phone,))
            result = cursor.fetchone()
            print(result)
            if result:
                # Customer exists, now check if the password matches
                stored_password = result[1]
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
if __name__ == "__main__":
    # 从键盘输入商家信息
    merchant_phone = input("请输入商家电话号码: ")
    merchant_identity = input("请输入商家身份证号码: ")
    password = input("请输入密码: ")
    shop_name = input("请输入店铺名称: ")
    shop_address = input("请输入店铺地址: ")
    management_licence_id = input("请输入经营许可证号码: ")
