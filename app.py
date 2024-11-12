# python的岗位展示的后端
from datetime import datetime, timedelta
import hashlib
import jwt
import numpy as np
from flask import Flask, jsonify,request
from flask_cors import CORS
import pymysql
from joblib import load
import book_recommand as recommand

# 构建后端应用程序
app = Flask(__name__)
# 先把后端的跨域问题解决了
CORS(app,resources={r"/*": {"origins": "*"}})

# 预测薪资函数
model1=load("model.joblib")
c=model1.intercept_
d=model1.coef_


# 定义一个提供岗位数据的后端函数
@app.route("/books")
def books():

    try:
        # 验证token是否正确

        connect = pymysql.connect(host="server.natappfree.cc", port=46589, user="books", passwd="books", db="books",
                                  charset="utf8", cursorclass=pymysql.cursors.DictCursor)
        sql = "select * from clean_bookinfo limit 10"
        cursor = connect.cursor()
        cursor.execute(sql)
        books = cursor.fetchall()
        sql_count = "SELECT COUNT(*) FROM clean_bookinfo"
        cursor.execute(sql_count)
        count = cursor.fetchone()['COUNT(*)']
        # 关闭数据库连接
        connect.close()
        cursor.close()
        # 返回结果
        return {"status": "success", "books": books, "count": count}

    except jwt.exceptions.DecodeError:
        # 验证失败，返回错误类型
        return {"status": "error"}

@app.route("/book")
def get_page_books():        # 关闭数据库连接

    start=int(request.args.get('start'))
    pagsize=int(request.args.get('pagsize'))
    print(start,pagsize)
    try:
        # 连接数据库
        conn = pymysql.connect(
            host="server.natappfree.cc",
            port=46589,
            user="books",
            passwd="books",
            db="books",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur=conn.cursor()
        sql = "SELECT * FROM clean_bookinfo limit %s,%s"
        # 执行语句
        cur.execute(sql, (start,pagsize,))
        books = cur.fetchall()
        #获取lpjobs数据库中所有数据条数sql语句
        sql_count = "SELECT COUNT(*) FROM clean_bookinfo"
        cur.execute(sql_count)
        count = cur.fetchone()['COUNT(*)']
        conn.close()
        cur.close()
        # 返回结果
        return {"books": books, "count": count}
    except Exception as e:
        # 记录错误信息
        print(f"Error: {e}")
        return {"error": str(e)}


# @app.route("/query_books")
# def query_books():
#     connect = pymysql.connect(host="server.natappfree.cc",port=46589,user="books",passwd="books",db="books",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
#     # 接受前端传递的参数
#     bookname = request.args.get("bookname")
#     sql = f"select * from clean_bookinfo where bookname like '%{bookname}%'"
#     cursor = connect.cursor()
#     cursor.execute(sql)
#     books = cursor.fetchall()
#     return books

@app.route("/types")
def types():
    connect = pymysql.connect(host="server.natappfree.cc",port=46589,user="books",passwd="books",db="books",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
    sql = "select * from clean_types limit 10"
    cursor = connect.cursor()
    cursor.execute(sql)
    types = cursor.fetchall()
    sql_count = "SELECT COUNT(*) FROM clean_types"
    cursor.execute(sql_count)
    count = cursor.fetchone()['COUNT(*)']
    # 关闭数据库连接
    connect.close()
    cursor.close()
    # 返回结果
    return {"types": types, "count": count}
@app.route("/typ")
def get_page_types():
    start=int(request.args.get('start'))
    pagsize=int(request.args.get('pagsize'))
    print(start,pagsize)
    try:
        # 连接数据库
        conn = pymysql.connect(
            host="server.natappfree.cc",
            port=46589,
            user="books",
            passwd="books",
            db="books",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur=conn.cursor()
        sql = "SELECT * FROM clean_types limit %s,%s"
        # 执行语句
        cur.execute(sql, (start,pagsize,))
        types = cur.fetchall()
        #获取lpjobs数据库中所有数据条数sql语句
        sql_count = "SELECT COUNT(*) FROM clean_types"
        cur.execute(sql_count)
        count = cur.fetchone()['COUNT(*)']
        # 关闭数据库连接
        conn.close()
        cur.close()
        # 返回结果
        return {"types": types,  "count": count}
    except Exception as e:
        # 记录错误信息
        print(f"Error: {e}")
        return {"error": str(e)}

@app.route("/ratingScore")
def ratingScore():
    connect = pymysql.connect(host="server.natappfree.cc",port=46589,user="books",passwd="books",db="books",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
    sql = "select * from ratingscore_statistics"
    cursor = connect.cursor()
    cursor.execute(sql)
    datas = cursor.fetchall()
    connect.close()
    cursor.close()
    returndatas =[]
    for data in datas:
        returndatas.append({"value":data['book_count'],"name":data['ratingScore_range']})
    return returndatas
@app.route("/ratingNum")
def ratingNum():
    connect = pymysql.connect(host="server.natappfree.cc",port=46589,user="books",passwd="books",db="books",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
    sql = "select * from ratingnum_statistics"
    cursor = connect.cursor()
    cursor.execute(sql)
    datas = cursor.fetchall()
    connect.close()
    cursor.close()
    returndatas =[]
    for data in datas:
        returndatas.append({"value":data['book_count'],"name":data['ratingNum_range']})
    return returndatas
@app.route("/type")
def type():
    connect = pymysql.connect(host="server.natappfree.cc",port=46589,user="books",passwd="books",db="books",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
    sql = "select * from type_statistics"
    cursor = connect.cursor()
    cursor.execute(sql)
    datas = cursor.fetchall()
    connect.close()
    cursor.close()
    returndatas =[]
    for data in datas:
        returndatas.append({"value":data['type_count'],"name":data['type']})
    return returndatas

@app.route("/commentNum")
def commentNum():
    connect = pymysql.connect(host="server.natappfree.cc",port=46589,user="books",passwd="books",db="books",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
    sql = "select * from commentnum_statistics"
    cursor = connect.cursor()
    cursor.execute(sql)
    datas = cursor.fetchall()
    connect.close()
    cursor.close()
    returndatas =[]
    for data in datas:
        returndatas.append({"value":data['book_count'],"name":data['commentNum_range']})
    return returndatas

@app.route('/books/<int:RID>', methods=['PUT'])
def update_book(RID):
    try:
        # 连接数据库
        conn = pymysql.connect(
            host="server.natappfree.cc",
            port=46589,
            user="books",
            passwd="books",
            db="books",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()
        data = request.json
        print(data)
        if not data:
            return jsonify({"error": "Invalid request data"}), 400
        update_columns = ', '.join([f"{key}=%s" for key in data.keys()])
        update_values = list(data.values())+[RID]
        query = f"UPDATE clean_bookinfo SET {update_columns} WHERE RID=%s"
        print(query)
        cur.execute(query, tuple(update_values))
        conn.commit()
        return jsonify("success")
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
@app.route('/books/<int:RID>', methods=['DELETE'])
def delete_book(RID):
    try:
        # 连接数据库
        conn = pymysql.connect(
            host="server.natappfree.cc",
            port=46589,
            user="books",
            passwd="books",
            db="books",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()
        query = f"DELETE FROM clean_bookinfo WHERE RID=%s"
        print(query)
        cur.execute(query, (RID,))
        conn.commit()
        return jsonify("success")
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route("/books/<string:tag>")
def select_book(tag):
    try:
        # 连接数据库
        conn = pymysql.connect(
            host="server.natappfree.cc",
            port=46589,
            user="books",
            passwd="books",
            db="books",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()
        # 使用参数化查询防止 SQL 注入
        sql = "SELECT * FROM clean_bookinfo WHERE tag LIKE %s LIMIT 10"
        cur.execute(sql, ('%' + tag + '%'))
        books = cur.fetchall()
        sql_count = "SELECT COUNT(*) FROM clean_bookinfo WHERE tag LIKE %s"
        cur.execute(sql_count, ('%' + tag + '%'))
        count = cur.fetchone()['COUNT(*)']
        # 关闭数据库连接
        conn.close()
        # 返回结果
        return {"books": books, "count": count}
    except Exception as e:
        # 记录错误信息
        print(f"Error: {e}")
        return {"error": str(e)}
@app.route("/book/<string:tag>")
def select_book_tag(tag):
    start = int(request.args.get('start'))
    pagsize = int(request.args.get('pagsize'))
    try:
        # 连接数据库
        conn = pymysql.connect(
            host="server.natappfree.cc",
            port=46589,
            user="books",
            passwd="books",
            db="books",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()

        # 使用参数化查询防止 SQL 注入
        sql = "SELECT * FROM clean_bookinfo WHERE tag LIKE %s LIMIT %s,%s"
        cur.execute(sql, ('%' + tag + '%', start, pagsize))
        books = cur.fetchall()
        sql_count = "SELECT COUNT(*) FROM clean_bookinfo WHERE tag LIKE %s"
        cur.execute(sql_count, ('%' + tag + '%'))
        count = cur.fetchone()['COUNT(*)']
        conn.close()
        cur.close()
        return {"books": books, "count": count}
    except Exception as e:
            # 记录错误信息
            print(f"Error: {e}")
            return {"error": str(e)}
@app.route('/types/<int:RID>', methods=['PUT'])
def update_types(RID):
    try:
        # 连接数据库
        conn = pymysql.connect(
            host="server.natappfree.cc",
            port=46589,
            user="books",
            passwd="books",
            db="books",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()
        data = request.json
        print(data)
        if not data:
            return jsonify({"error": "Invalid request data"}), 400
        update_columns = ', '.join([f"{key}=%s" for key in data.keys()])
        update_values = list(data.values())+[RID]
        query = f"UPDATE clean_types SET {update_columns} WHERE RID=%s"
        print(query)
        cur.execute(query, tuple(update_values))
        conn.commit()
        return jsonify("success")
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
@app.route('/types/<int:RID>', methods=['DELETE'])
def delete_types(RID):
    try:
        # 连接数据库
        conn = pymysql.connect(
            host="server.natappfree.cc",
            port=46589,
            user="books",
            passwd="books",
            db="books",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()
        query = f"DELETE FROM clean_types WHERE RID=%s"
        print(query)
        cur.execute(query, (RID,))
        conn.commit()
        return jsonify("success")
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route("/types/<string:type>")
def select_types(type):
    try:
        # 连接数据库
        conn = pymysql.connect(
            host="server.natappfree.cc",
            port=46589,
            user="books",
            passwd="books",
            db="books",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()
        # 使用参数化查询防止 SQL 注入
        sql = "SELECT * FROM clean_types WHERE type LIKE %s LIMIT 10"
        cur.execute(sql, ('%' + type + '%'))
        types = cur.fetchall()
        sql_count = "SELECT COUNT(*) FROM clean_types WHERE type LIKE %s"
        cur.execute(sql_count, ('%' + type + '%'))
        count = cur.fetchone()['COUNT(*)']
        # 关闭数据库连接
        conn.close()
        cur.close()
        # 返回结果
        return {"types": types, "count": count}
    except Exception as e:
        # 记录错误信息
        print(f"Error: {e}")
        return {"error": str(e)}
@app.route("/typ/<string:type>")
def select_types_page(type):
    start = int(request.args.get('start'))
    pagsize = int(request.args.get('pagsize'))
    try:
        # 连接数据库
        conn = pymysql.connect(
            host="server.natappfree.cc",
            port=46589,
            user="books",
            passwd="books",
            db="books",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()

        # 使用参数化查询防止 SQL 注入
        sql = "SELECT * FROM clean_types WHERE type LIKE %s LIMIT %s,%s"
        cur.execute(sql, ('%' + type + '%', start, pagsize))
        types = cur.fetchall()
        sql_count = "SELECT COUNT(*) FROM clean_types WHERE type LIKE %s"
        cur.execute(sql_count, ('%' + type + '%'))
        count = cur.fetchone()['COUNT(*)']
        conn.close()
        cur.close()
        return {"types": types, "count": count}
    except Exception as e:
            # 记录错误信息
            print(f"Error: {e}")
            return {"error": str(e)}
@app.route('/predict_book')
def predict_book():
        param_array = []
        # 岗位类型维度的向量值进入数组
        param_array.append(int(request.args.get('tag')))
        param_array.append(int(request.args.get('ratingNum')))
        # 岗位的学历和岗位的工作经验要向量化进入数组
        param_array.append(int(request.args.get('commentNum')))
        book_vec_array = np.array(param_array)
        result = book_vec_array.dot(d)+c
        result = round(result, 2)
        return {"result": result}
@app.route('/recommand_book')
def book_recommand_book():
    # 1、接受前端传递的五个参数：岗位类型 岗位区域：向量化处理  学历 薪资：向量化  经验
    # 参数的向量化之前数组  向量化数组的每一个维度必须和岗位的向量化的维度保持一致
    param_array = []
    # 岗位类型维度的向量值进入数组
    tag = int(request.args.get('tag'))
    param_array.append(tag)
    # 岗位薪资向量化进入数组
    ratingScore = float(request.args.get("ratingScore"))
    param_array.append(ratingScore)
    # 岗位的学历和岗位的工作经验要向量化进入数组
    ratingNum=int(request.args.get('ratingNum'))
    param_array.append(ratingNum)
    commentNum = int(request.args.get('commentNum'))
    param_array.append(commentNum)
    # count = int(request.args.get('count'))
    # 2、开发推荐算法，准备给前端返回的数据
    result = recommand.recommand(param_array,10)
    # 3、返回数据
    return result
@app.route('/Phonelogin', methods=['PUT'])
def Phonelogin():
        conn = pymysql.connect(
            host="server.natappfree.cc",
            port=46589,
            user="books",
            passwd="books",
            db="books",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()
        data = request.json
        print(data)
        if not data:
            return jsonify({"status": "error", "error": "Invalid request data"})
        phone = data["phone"]
        password = data["pass"]
        # 密码加密
        password = hashlib.md5(password.encode()).hexdigest()
        sql = f"select * from users where  phone=%s"
        cur.execute(sql, (phone,))
        user = cur.fetchone()
        if user:
            if user['password'] == password:
                # 实现token存储用户数据
                token = jwt.encode({'user': user, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                                    'secret', algorithm='HS256')
                   # 获取token,并判断是否正确
                return jsonify({"status": "success", "message": "Login successful", "user": user['username'], "token": token})
            else:
                return jsonify({"status": "error", "error": "Invalid password"})
        else:
            return jsonify({"status": "error", "error": "User not found"})
@app.route('/login', methods=['PUT'])
def login():
        conn = pymysql.connect(
            host="server.natappfree.cc",
            port=46589,
            user="books",
            passwd="books",
            db="books",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()
        data = request.json
        print(data)
        if not data:
            return jsonify({"status": "error", "error": "Invalid request data"})
        username = data["username"]
        password = data["pass"]
        # 密码加密
        password = hashlib.md5(password.encode()).hexdigest()
        sql = f"select * from users where  username=%s"
        cur.execute(sql, (username,))
        user = cur.fetchone()
        if user:
            if user['password'] == password:
                # 实现token存储用户数据
                token = jwt.encode({'user': user, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                                    'secret', algorithm='HS256')
                   # 获取token,并判断是否正确
                return jsonify({"status": "success", "message": "Login successful", "user": user['username'], "token": token})
            else:
                return jsonify({"status": "error", "error": "Invalid password"})
        else:
            return jsonify({"status": "error", "error": "User not found"})

@app.route('/register', methods=['POST'])
def register():
    conn = pymysql.connect(
        host="server.natappfree.cc",
        port=46589,
        user="books",
        passwd="books",
        db="books",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    data = request.json
    print(data)
    if not data:
        return {"status": "error", "error": "Invalid request data"}
    user_name = data["user"]
    phone = data["phone"]
    # 查询数据库是否有对应用户user和phone
    sql = f"select * from users where  username=%s or phone=%s"
    cur.execute(sql, (user_name, phone))
    user = cur.fetchone()
    if user:
        return {"status": "error", "error": "User already exists"}
    email = data["email"]
    area = data["area"]
    sex = data["sex"]
    password = data["pass"]
    age = data["age"]
    password = hashlib.md5(password.encode()).hexdigest()
    sql = f"insert into users(username,phone,email,area,sex,password,age) values(%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(sql, (user_name, phone, email, area, sex, password, age))
    conn.commit()
    return {"status": "success", "message": "Register successful"}
if __name__ == '__main__':
    # 允许所有网络访问
    app.run(host='0.0.0.0',port=5000)