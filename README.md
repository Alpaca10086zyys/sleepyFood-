# sleepyFood
企业实训小组作业--外卖管理系统

## 项目介绍
本项目由本组成员通力完成，本组成员有前端组：[@wyxzc](https://github.com/wyxzc)和[@despereaten](https://github.com/despereaten)，和后端组：[@Alpaca10086zyys](https://github.com/Alpaca10086zyys)和[@suiicvc](https://github.com/suiicvc)。
实现的基本功能为外卖管理系统，三个不同角色的注册登录和基本操作。后端框架为Flask框架，前端由html+css+js三件套完成，database为MySQL。

## 使用方法
在git bash里输入：
```shell
git clone [仓库地址]
```
克隆项目到本地后用pycharm打开，注意在edit configuration中将interpreter设置为本机默认的interpreter。
### 准备数据库
配置数据库，基本信息为：
```
user='food_root_user',
password='Aa123456_',
database='sleepyfood'
```
建表后用`food_root_user`用户访问`sleepyfood`这个schema，然后在这个database中建表。
建表语句如下：
```SQL
-- 顾客信息表
CREATE TABLE Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    cust_phone CHAR(11) NOT NULL UNIQUE
);

-- 顾客地址表
CREATE TABLE CustomerAddress (
	address_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    user_address VARCHAR(50) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

-- 商家信息表
CREATE TABLE Merchant (
    merchant_id INT AUTO_INCREMENT PRIMARY KEY,
    merchant_phone CHAR(11) NOT NULL UNIQUE,
    merchant_identity CHAR(18) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    shop_name VARCHAR(50) NOT NULL UNIQUE,
    shop_address VARCHAR(100) NOT NULL UNIQUE,
    management_licence_id CHAR(15) NOT NULL
);

-- 骑手信息表
CREATE TABLE Rider (
    rider_id INT AUTO_INCREMENT PRIMARY KEY,
    rider_identity CHAR(18) NOT NULL UNIQUE,
    rider_phone CHAR(11) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL,
    licence_plate CHAR(6) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    status BOOLEAN NOT NULL
);

-- 菜单表
CREATE TABLE Menu (
    menu_item_id INT AUTO_INCREMENT PRIMARY KEY,
    merchant_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    price INT NOT NULL,
    score DECIMAL(2,1),
    FOREIGN KEY (merchant_id) REFERENCES Merchant(merchant_id)
);
-- 订单表
CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    rider_id INT,
    merchant_id INT NOT NULL,
    total_price INT NOT NULL,
    cus_address VARCHAR(100) NOT NULL,
    shop_address VARCHAR(100) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (rider_id) REFERENCES Rider(rider_id),
    FOREIGN KEY (merchant_id) REFERENCES Merchant(merchant_id)
);

-- 订单明细表
CREATE TABLE OrderDetail (
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    menu_item_count INT NOT NULL,
    PRIMARY KEY (order_id, menu_item_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (menu_item_id) REFERENCES Menu(menu_item_id)
);

-- 评价表
CREATE TABLE Review (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    review_content TEXT NOT NULL,
    feedback TEXT,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- merchant_id自动访问shop_address触发器
DELIMITER //

CREATE TRIGGER update_shop_address
BEFORE INSERT ON Orders
FOR EACH ROW
BEGIN
    DECLARE shopAddress VARCHAR(100);
    SELECT shop_address INTO shopAddress FROM Merchant WHERE merchant_id = NEW.merchant_id;
    SET NEW.shop_address = shopAddress;
END//

DELIMITER ;
```
然后运行app.py即可,在控制台会生成本地访问链接。
