from merchant import create_merchant
from customer import create_customer,create_customer_address,login_customer
from rider import create_rider

# # 商家注册测试
# merchant_phone = input("请输入商家电话号码: ")
# merchant_identity = input("请输入商家身份证号码: ")
# password = input("请输入密码: ")
# shop_name = input("请输入店铺名称: ")
# shop_address = input("请输入店铺地址: ")
# management_licence_id = input("请输入经营许可证号码: ")
# create_merchant(merchant_phone, merchant_identity, password, shop_name, shop_address, management_licence_id)

# 顾客
# username = input("请输入用户名: ")
# password = input("请输入密码: ")
# cust_phone = input("请输入顾客电话号码: ")
# create_customer(username, password, cust_phone)


# 骑手注册测试
# rider_identity = input("请输入骑手身份证号码: ")
# licence_plate = input("请输入骑手车牌号: ")
# username = input("请输入骑手姓名: ")
# password = input("请输入骑手密码: ")
# create_rider(rider_identity, licence_plate, username, password)

# 从键盘输入顾客地址信息
# customer_id = int(input("请输入顾客ID: "))
# user_address = input("请输入顾客地址: ")
# create_customer_address(customer_id, user_address)

# 顾客登录注册
cust_phone=input("Enter customer phone number: ")
password=input("enter password: ")
result=login_customer(cust_phone,password)
print(result)