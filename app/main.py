from typing import Union
from typing import List, Dict

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from sqlalchemy import create_engine, text

app = FastAPI()

# データベースへの接続情報
#db_user = os.environ["DB_USER"]  # e.g. 'my-database-user'
#db_pass = os.environ["DB_PASS"]  # e.g. 'my-database-password'
#db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
db_username = "cloudsql-application"
db_password = "cloudsql-application"
db_name = "orders"
connection_name = "[[Your Connection Name]]"

# SQLAlchemy接続文字列
connection_str = f"mysql+pymysql://{db_username}:{db_password}@/{db_name}?unix_socket=/cloudsql/{connection_name}"

# SQLAlchemyエンジン生成
engine = create_engine(connection_str)

@app.get("/", response_class=HTMLResponse)
def read_root():
    message = '<H1>注文情報入力 </H1>'
    message = message + '<form action="/order" method="post">'
    message = message + '  cart_id: <input type="text" name="cart_id" /></br>'
    message = message + '  order_amount: <input type="text" name="order_amount" /></br>'
    message = message + '  customer_id: <input type="text" name="customer_id" /></br>'
    message = message + '  product_type: <input type="text" name="product_type" /></br>'
    message = message + '  <input type="submit" value="送信" />'
    message = message + '</form>'
    return message

@app.get("/order")
def create_order(cart_id: str, order_amount: float, customer_id: str, product_type: str):
    query = text("INSERT INTO orders (cart_id, order_amount, customer_id, product_type) VALUES (:cart_id, :order_amount, :customer_id, :product_type) ")
    params = {"cart_id": cart_id, "order_amount": order_amount, "customer_id": customer_id, "product_type": product_type}
    with engine.begin() as connection:
        connection.execute(query, params)

    return {"message": "Cart created successfully!"}

@app.get("/order_list", response_class=HTMLResponse)
def get_order_list():
    query = text("select * from orders ORDER BY order_id limit 100")
    with engine.begin() as connection:
        result = connection.execute(query)
    html = ""
    for row in result:
        html = html + str(row) + "</br>"
    return html

@app.get("/order_info/{order_id}", response_class=HTMLResponse)
def get_order(order_id: str):
    query = text("SELECT * FROM orders WHERE order_id = :order_id")
    params = {"order_id": order_id}
    with engine.begin() as connection:
        result = connection.execute(query, params)
    html = ""
    for row in result:
        html = html + str(row) + "</br>"
    return html

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    app.run(debug=True)