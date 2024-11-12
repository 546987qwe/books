'''
获取数据库所有的清洗完成的岗位数据
把每一个岗位数据向量化，和参数向量化求一个向量的余弦值
判断如果余弦值大于0.8 代表岗位可以推荐。岗位加入到一个数组中，准备给前端返回
'''
import numpy as np
import pymysql
import book_vector as book_vector
def recommand(param_array,count):
    # 定义一个数组，存放推荐的数据
    recommand_datas = []
    size=0
    start=0
    # 链接数据库获取清洗完成的岗位数据
    connect = pymysql.connect(host="server.natappfree.cc",port=46589,user="books",passwd="books",db="books",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
    cursor = connect.cursor()
    sql_count = "SELECT COUNT(*) FROM clean_bookinfo"
    cursor.execute(sql_count)
    countnum = cursor.fetchone()['COUNT(*)']
    while True:
        sql = "select  * from clean_bookinfo limit %s,500 "
        cursor.execute(sql,(start))
        start+=500
        books = cursor.fetchall()
        # 遍历所有的岗位信息，先把岗位向量化，然后和参数的向量化求余弦值（推荐算法的核心），判断余弦值>=0.8 加入推荐数组
        for book in books:
            # job向量化
            book_vec_array = book_vector.book_vector(book)
            # 将参数向量化数组和job向量化数组转成向量
            param_vec = np.array(param_array)
            book_vec = np.array(book_vec_array)
            # 两个向量的余弦值
            cos = np.dot(param_vec, book_vec) / (np.linalg.norm(param_vec) * np.linalg.norm(book_vec))
            # 判断余弦值是不是大于等于0.8
            if cos >= 0.98:
                book['book_score'] = cos * 100
                # 保留2位小数
                book['book_score'] = round(book['book_score'], 2)
                recommand_datas.append(book)
                size=size+1
                if size>=count:
                    break
        if size>=count:
            break
        if start >= countnum:
            break
    connect.close()
    return recommand_datas