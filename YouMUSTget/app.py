#载入 Flask
from logging import root
from flask import *  
app=Flask(
    __name__,
    static_folder="public",        
    static_url_path="/" 
    #所有在public文件夹当下的文件，都对应到网址路径./文件名称

    #static_folder="static",        #static_folder="存放静态档案的文件夹名称"
    #static_url_path="/static"      #static_url_path="对应到的网址路径" 
    #所有在static文件夹当下的文件，都对应到网址路径./static/文件名称
    ) #建立 Application 物件,透过参数指定静态档案路径
import pymysql
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    port=3306,
    db='cabinet'
)


def empty():
    conn.ping(reconnect=True)
    sql='select count(state=0 or null) as "empty cabinets" from cabinet_list'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    solution=cursor.fetchall()
    cursor.close()
    return solution

from ronglian_sms_sdk import SmsSDK

accId = '8a216da8806f31ad0180d601fed91912'
accToken = 'b12c4fe037354fef88b104cbe199f2fc'
appId = '8a216da8806f31ad0180d60200011919'


def send_message():

    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    mobile = '13952576220'
    datas = ('265746', '1')
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)


 

#什么是路由？
#路由决定网址路径和处理函数的对应关系
#前端输入不同路径时，后端程序要决定对应的处理函数
#路由的设定方式：透过函数的装饰器[@app.route(路径)]设定路由
#语法：@app.route(路径)
#     def 处理函数名称(参数名称)：
#         处理函数的程式区块

@app.route("/") # / 代表root,建立路径 "/" 的对应的处理函数
def first(): # def 定义一个函数 index-用来回应路径 "/" 的处理函数
        return render_template("first.html") #返回网站首页内容

@app.route("/cindex")#
def cindex():
    return render_template("cindex.html")

@app.route("/cstore")#快递员的存界面
def cstore():
    return render_template("stel.html")

@app.route("/cpick")#快递员取界面
def cpick():
    return render_template("ptel.html")

@app.route("/uindex")#用户首页
def uindex():
    return render_template("uindex.html")

@app.route("/ustore")#用户存界面  在uindex后，显示有多少个柜子   
def ustore():
    solution = empty()
    conn.close()
    return render_template("count.html", solution=solution)

@app.route("/upick")#用户取界面
def upick():
    return render_template("pickupcode.html")

#third-取部分
@app.route("/open", methods=['POST', 'GET'])#用户取东西输入code提交后跳转判断，并显示哪个柜，在upick后
def open():
    if request.method == 'POST':
        code = request.form["inputArea"]
    elif request.method == 'GET':
        code = request.form["inputArea"]
    conn.ping(reconnect=True)
    sql= 'select id from cabinet_list where pickup_code = "%s"' % (code)
    sql_update='update cabinet_list set state=0,pickup_code=null where pickup_code = "%s"' % (code)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    cabinet=cursor.fetchall()
    cursor.execute(sql_update)
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("openc.html",cabinet=cabinet)

@app.route("/copen", methods=['POST', 'GET'])#快递员取东西输入tel提交后跳转判断，并显示哪个柜，在upick后
def copen():
    if request.method == 'POST':
        tel = request.form["inputArea"]
    elif request.method == 'GET':
        tel = request.form["inputArea"]
    conn.ping(reconnect=True)
    sql= 'select id from cabinet_list where courier_tel = "%s"' % (tel)
    sql_update= 'update cabinet_list set state=0,courier_tel=null where courier_tel = "%s"' % (tel)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    cabinet=cursor.fetchall()
    cursor.execute(sql_update)
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("copenc.html",cabinet=cabinet)

@app.route("/pend")#取功能最后界面
def pend():
    return render_template("pend.html")

#   
#third 存功能实现
@app.route("/update")#用户存，查找出第一个空柜子，将柜子id显示出来，并且分配快递员电话号码给该柜子
def update():
    conn.ping(reconnect=True)
    sql='SELECT id from cabinet_list WHERE state=0'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    id=cursor.fetchone()
    sql_update='UPDATE cabinet_list set state=1,courier_tel=64642222 WHERE id=(select id from (select id from cabinet_list WHERE state=0 LIMIT 1) as temp)'
    cursor.execute(sql_update)
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("update.html",id=id)




@app.route("/random")#快递员存，查找出第一个空柜子，（输入的用户电话号码发送短信），生成随机码，将随机码写入该柜子的数据库
def random():
    send_message()
    conn.ping(reconnect=True)
    sql='SELECT id from cabinet_list WHERE state=0'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    id=cursor.fetchall()
    sql_update='UPDATE cabinet_list set state=1,pickup_code=265746 WHERE id=(select id from (select id from cabinet_list WHERE state=0 LIMIT 1) as temp)'
    cursor.execute(sql_update)
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("update.html",id=id)

@app.route("/send")#取功能最后界面
def send():
    return render_template("send.html")



#启动网站服务器
app.run()
#app.run(port=3000)改变指定端口号5000为3000

#这个warning说的是以上代码的做法不适合上线比较适合开发
#以上只是学习如何用flask构造后端框架，之后会用云端服务进行上线，这个warning就不存在了
#Running on 网址 ：意思是我们的网站正在这个网址中运行，可以用ctrl+点击，就会看到网站正常运作
#服务器一旦运作起来就不会自动停止（不会自动出现命令行），它会随时等待前端的连接
#如果要停止就需要ctrl+c，如果中断后，再刷新网页页面，就会看到连接失败

