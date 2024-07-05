import pymysql

class MenuItem:
    def __init__(self, menu_item_id, merchant_id, name, price, score):
        self.menu_item_id = menu_item_id
        self.merchant_id = merchant_id
        self.name = name
        self.price = price
        self.score = score

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
            insert_query = "INSERT INTO Menu (merchant_id, name, price, score) VALUES (%s, %s, %s, %s)"
            values = (self.merchant_id, self.name, self.price, self.score)
            cursor.execute(insert_query, values)

            # 提交事务
            connection.commit()

            print("菜品信息插入成功！")

        except Exception as e:
            # 发生错误时回滚事务
            connection.rollback()
            print("菜品信息插入失败:", e)

        finally:
            # 关闭游标和数据库连接
            cursor.close()
            connection.close()

    def delete_from_db(self):
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
            # 执行删除语句
            delete_query = "DELETE FROM Menu WHERE menu_item_id = %s"
            cursor.execute(delete_query, (self.menu_item_id,))

            # 提交事务
            connection.commit()

            print("菜品信息删除成功！")

        except Exception as e:
            # 发生错误时回滚事务
            connection.rollback()
            print("菜品信息删除失败:", e)

        finally:
            # 关闭游标和数据库连接
            cursor.close()
            connection.close()

    def update_in_db(self):
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
            # 执行更新语句
            update_query = "UPDATE Menu SET merchant_id = %s, name = %s, price = %s, score = %s WHERE menu_item_id = %s"
            values = (self.merchant_id, self.name, self.price, self.score, self.menu_item_id)
            cursor.execute(update_query, values)

            # 提交事务
            connection.commit()

            print("菜品信息更新成功！")

        except Exception as e:
            # 发生错误时回滚事务
            connection.rollback()
            print("菜品信息更新失败:", e)

        finally:
            # 关闭游标和数据库连接
            cursor.close()
            connection.close()

def create_menu_item(merchant_id, name, price, score):
    # 创建菜品对象
    menu_item = MenuItem(
        menu_item_id=None,  # menu_item_id是自增字段，插入时不需要提供值
        merchant_id=merchant_id,
        name=name,
        price=price,
        score=score
    )
    # 插入菜品信息到数据库
    menu_item.insert_into_db()

def delete_menu_item(menu_item_id):
    # 创建菜品对象
    menu_item = MenuItem(
        menu_item_id=menu_item_id,
        merchant_id=None,
        name=None,
        price=None,
        score=None
    )
    # 从数据库删除菜品信息
    menu_item.delete_from_db()

def update_menu_item(menu_item_id, merchant_id, name, price, score):
    # 创建菜品对象
    menu_item = MenuItem(
        menu_item_id=menu_item_id,
        merchant_id=merchant_id,
        name=name,
        price=price,
        score=score
    )
    # 更新数据库中的菜品信息
    menu_item.update_in_db()

if __name__ == "__main__":
    # 示例操作
    print("1. 添加菜品")
    print("2. 删除菜品")
    print("3. 更新菜品")
    choice = input("请选择操作 (1/2/3): ")

    if choice == '1':
        merchant_id = input("请输入商家ID: ")
        name = input("请输入菜品名称: ")
        price = int(input("请输入菜品价格: "))
        score = float(input("请输入菜品评分: "))
        create_menu_item(merchant_id, name, price, score)
    elif choice == '2':
        menu_item_id = int(input("请输入菜品ID: "))
        delete_menu_item(menu_item_id)
    elif choice == '3':
        menu_item_id = int(input("请输入菜品ID: "))
        merchant_id = input("请输入商家ID: ")
        name = input("请输入菜品名称: ")
        price = int(input("请输入菜品价格: "))
        score = float(input("请输入菜品评分: "))
        update_menu_item(menu_item_id, merchant_id, name, price, score)
    else:
        print("无效的选择")
