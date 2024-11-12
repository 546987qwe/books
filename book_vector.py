'''

'''
types=['文化', '生活','经管', '流行', '文学','科技']
economy = ['经济学', '管理', '经济', '商业', '金融', '投资', '营销', '创业', '理财', '广告', '股票', '企业史', '策划']
culture=['历史', '心理学', '哲学', '传记', '文化', '社会学', '艺术', '设计', '社会', '政治', '建筑', '宗教', '电影', '数学','政治学', '回忆录', '中国历史', '思想', '国学', '音乐', '人文', '人物传记', '绘画', '戏剧', '艺术史', '佛教','军事', '西方哲学', '二战', '近代史', '考古', '自由主义', '美术']
life=['爱情', '旅行', '生活', '成长', '励志', '心理', '摄影', '女性', '职场', '美食', '教育', '游记', '灵修', '健康','情感', '手工', '两性', '养生', '人际关系', '家居', '自助游']
technology=['科普', '互联网', '编程', '科学', '交互设计', '用户体验', '算法', 'web', '科技', 'UE', '通信', '交互', 'UCD','神经网络', '程序']
fashion=['漫画', '绘本', '推理', '青春', '东野圭吾', '科幻', '言情', '悬疑', '武侠', '奇幻', '韩寒', '日本漫画', '耽美','亦舒', '推理小说', '三毛', '网络小说', '安妮宝贝', '郭敬明', '穿越', '金庸', '轻小说', '阿加莎·克里斯蒂', '几米','科幻小说', '魔幻', '青春文学', '张小娴', '幾米', 'J.K.罗琳', '高木直子', '古龙', '沧月', '落落', '张悦然', '校园']
library=['小说', '外国文学', '文学', '随笔', '中国文学', '经典', '日本文学', '散文', '村上春树', '诗歌', '童话', '王小波','杂文', '古典文学', '儿童文学', '名著', '张爱玲', '余华', '当代文学', '钱钟书', '外国名著', '鲁迅', '诗词', '茨威格', '米兰·昆德拉', '杜拉斯', '港台']

def tag_vector(tag):
    if tag in culture:
        return 1
    elif tag in life:
        return 2
    elif tag in economy:
        return 3
    elif tag in fashion:
        return 4
    elif tag in library:
        return 5
    elif tag in technology:
        return 6
    else:
        return 0
def ratingScore_vector(ratingScore):
    if ratingScore>=2 and ratingScore<4:
        return 1
    elif ratingScore>=4 and ratingScore<6:
        return 2
    elif ratingScore>=6 and ratingScore<8:
        return 3
    elif ratingScore>=8 and ratingScore<10:
        return 4
    else:
        return 0
def ratingNum_vector(ratingNum):
    if ratingNum<10000:
        return 1
    elif ratingNum>=10000 and ratingNum<50000:
        return 2
    elif ratingNum>=50000 and ratingNum<100000:
        return 3
    elif ratingNum>=100000 and ratingNum<150000:
        return 4
    else:
        return 5
def commentNum_vector(commentNum):
    if commentNum<3000:
        return 1
    elif commentNum>=3000 and commentNum<9000:
        return 2
    elif commentNum>=9000 and commentNum<15000:
        return 3
    else:
        return 4
def book_vector(book):
    book_array=[]
    # 先拿到岗位的4个信息
    tag = book['tag']
    ratingScore = book['ratingScore']
    ratingScore=float(ratingScore)
    ratingNum = book['ratingNum']
    ratingNum=int(ratingNum)
    commentNum = book['commentNum']
    commentNum=int(commentNum)
    book_array.append(tag_vector(tag))
    book_array.append(ratingScore_vector(ratingScore))
    book_array.append(ratingNum_vector(ratingNum))
    book_array.append(commentNum_vector(commentNum))
    return book_array