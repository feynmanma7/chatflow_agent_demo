# 1. 产品大类找客户
+ 启动服务
```shell
python cate_to_user.py
```

+ 测试服务
```shell
curl -X POST \
http://localhost:5001/recommend/category \
-H "Content-Type: application/json" \
-d '{
    "manager_id":"M001",
    "product_category":"理财"
}'
```


# 2. 产品找客户

+ 启动服务
```shell
python item_to_user.py
```

+ 测试服务
```shell
curl -X POST \
http://localhost:5002/recommend/product \
-H "Content-Type: application/json" \
-d '{
    "manager_id":"M001",
    "product_id":"P12345"
}'
```


