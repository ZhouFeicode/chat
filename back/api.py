from flask import Flask,request,jsonify,Response,abort
import pymysql
import smtplib
import random
from datetime import datetime,timedelta
import os
import time
from flask_cors import CORS 
from email.mime.text import MIMEText
import socket
import threading
from flask_sock import Sock
import ast
app=Flask(__name__)
username=''
CORS(app,resources={r"/api/*": {"origins": "http://localhost:5173"}})
# 邮箱配置
EMAIL_HOST = 'smtp.sina.com'
EMAIL_PORT = 465
EMAIL_USER = 'amailabao@sina.com'
EMAIL_PASS ='0c6e8d5c85b74cfe'
EXPIRE_CODE=[]
sock=Sock(app)
client=None
def get_db_connection():
    conn=pymysql.connect(host='localhost',user='root',password='root',database='chat',charset='utf8mb4')
    return conn
@sock.route('/api/ws')
def websocket(ws_conn):
    global client
    client=ws_conn
    print("client connected")
    client.send("connected successfully")
    while True:
        msg=client.receive()
        if not msg:
            break
        print("data",msg)
    client=None
    
   

@app.route('/api/sendCode',methods=['POST'])
def sendCode():
    global EXPIRE_CODE
    data=request.get_json()
    email=data.get('email')
    if not email:
        return jsonify({'code':400,'message':'Email is required'})
    if not EMAIL_USER:
        return jsonify({'code':400,'message':'Email user is required'})
    if not EMAIL_PASS:
        return jsonify({'code':400,'message':'Email password is required'})
    code=random.randint(100000,999999)
    EXPIRE_CODE=[code,int(time.time())+300]
    try:
        msg=MIMEText(f'Your verification code is {code}.Please use it within 5 minutes.','plain','utf-8')
        msg['From']=EMAIL_USER
        msg['To']=email
        msg['Subject']='Verification Code'
        server=smtplib.SMTP_SSL(EMAIL_HOST,EMAIL_PORT)
        server.login(EMAIL_USER,EMAIL_PASS)
        server.sendmail(EMAIL_USER,email,msg.as_string())
        server.quit()
        return jsonify({'code':200,'message':'Code sent successfully'})
    except:
        return jsonify({'code':500,'message':'Code sending failed'})
@app.route('/api/login',methods=['POST'])
def login():
    global EXPIRE_CODE,username,my_port,udp_ips,tcp_ips
    data=request.get_json()
    email=data.get('email')
    code=data.get('code')
    if not email:
        return jsonify({'code':400,'message':'Email is required'})
    if not code:
        return jsonify({'code':400,'message':'Code is required'})
    if len(EXPIRE_CODE)==0:
        return jsonify({'code':400,'message':'Code invalid'})
    if  EXPIRE_CODE[1]<int(time.time()):
        EXPIRE_CODE.clear()
        return jsonify({'code':400,'message':'Code expired'})
    if int(code)!=EXPIRE_CODE[0]:
        return jsonify({'code':400,'message':'Code incorrect'})
    username=email
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute("select email,password from user where email=%s",(email,))
    result=cursor.fetchone()
    if result and result[0] and result[1]:
        peer.sendto((encrypt(f"!join:ALL:{username}:hello").encode('utf-8')+b'\n'),(BROADCAST,PORT))
        group_list=intoChat(username)
        for group in group_list:
            store_msg(group,username,"comes into the chat")
        _,my_port=peer.getsockname()
        udp_ips[(my_ip,my_port)]=username
        tcp_ips[(my_ip,TCP_PORT)]=username
        print("tcp_ips and udp_ips",tcp_ips,udp_ips)
        cursor.execute("update user set status=0 where email=%s",(email,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'code':200,'data':{'email':email},'message':'login successfully'})
    if result and result[0] and not result[1]:
        cursor.close()
        conn.close()
        return jsonify({'code':201,'data':{'email':email},'message':'no password, please set password'})
    cursor.execute("insert into user (email) values (%s)",(email,))
    table_name=email+'_groups'
    sql=f""" create table `{table_name}` (id int auto_increment primary key,
    group_id bigint(20),group_name varchar(255))ENGINE=InnoDB DEFAULT CHARSET=utf8mb4  ;"""
    cursor.execute(sql)
    table_name=email+'_friends'
    sql=f""" create table `{table_name}` (id int auto_increment primary key,
    user_name varchar(255))ENGINE=InnoDB DEFAULT CHARSET=utf8mb4  ;"""
    cursor.execute(sql)
    table_name=email+'_gm'
    sql=f""" create table `{table_name}` (id int auto_increment primary key,
    group_id bigint(20),sender varchar(255),msg text,datetime datetime)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4  ;"""
    cursor.execute(sql)
    table_name=email+'_fm'
    sql=f""" create table `{table_name}` (id int auto_increment primary key,
    sender varchar(255),receiver varchar(255),msg text,datetime datetime)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4  ;"""
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'code':201,'data':{'email':email},'message':'no account, automatically create an account'})
@app.route('/api/setPassword',methods=['POST'])
def setPassword():
    data=request.get_json()
    password=data.get('password')
    email=data.get('email')
    if not email:
        return jsonify({'code':400,'message':'Email is required'})
    if not password:
        return jsonify({'code':400,'message':'Password is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("update user set password=%s where email=%s",(password,email))
        conn.commit()
        return jsonify({'code':200,'data':{'email':email},'message':'Setting password successfully'})
    except:
        return jsonify({'code':500,'message':'Setting password failed'})
    finally:
        cursor.close()
        conn.close()
@app.route('/api/accountLogin',methods=['POST'])
def accountLogin():
    global username,my_port,udp_ips,tcp_ips
    data=request.get_json()
    email=data.get('email')
    password=data.get('password')
    if not email:
        return jsonify({'code':400,'message':'Email is required'})
    if not password:
        return jsonify({'code':400,'message':'Password is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("select email,password from user where email=%s and password=%s",(email,password))
        result=cursor.fetchone()
        if result:
            username=email
            peer.sendto((encrypt(f"!join:ALL:{username}:hello").encode('utf-8')+b'\n'),(BROADCAST,PORT))
            _,my_port=peer.getsockname()
            udp_ips[(my_ip,my_port)]=username
            tcp_ips[(my_ip,TCP_PORT)]=username
            print("tcp_ips and udp_ips",tcp_ips,udp_ips)
            cursor.execute("update user set status=0 where email=%s",(email,))
            conn.commit()
            return jsonify({'code':200,'data':{'email':email},'message':'login successfully'})
        return jsonify({'code':400,'message':'Email or password is incorrect'})
    except Exception as e:
        return jsonify({'code':500,'message':'Login failed'+str(e)})
    finally:
        cursor.close()
        conn.close()
@app.route('/api/group/list',methods=['GET'])
def getGroupList():
    email=request.args.get('email')
    if not email:
        return jsonify({'code':400,'message':'Email is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select id,group_id,group_name from `{email}_groups` order by group_name asc")
        result=cursor.fetchall()
        return jsonify({'code':200,'data':result,'message':'Group list fetched successfully'})
    except Exception as e:
        print(e)
        return jsonify({'code':500,'message':'Group list fetching failed'})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/group/add',methods=['POST'])
def addFriend():
    data=request.get_json()
    email=data.get('email')
    name=data.get('name')
    if not email:
        return jsonify({'code':400,'message':'Email is required'})
    if not name:
        return jsonify({'code':400,'message':'Name is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("select count(*) from user where email=%s",(name,))
        user=cursor.fetchone()[0]
        if not user:
            return jsonify({'code':400,'message':'User not found'})
        peer.sendto(encrypt(f"request:{email}:{name}:friend request").encode('utf-8'),(BROADCAST,PORT))
        cursor.execute("insert into `friend_request` (inviter,invitee,status) values(%s,%s,%s)",(email,name,0))
        conn.commit()
        return jsonify({'code':200,'data':{'email':email,'name':name},'message':'Friend request sent successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Adding friend failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/friend/list',methods=['GET'])
def getFriendList():
    email=request.args.get('email')
    if not email:
        return jsonify({'code':400,'message':'Email is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select t1.user_name,t2.status from `{email}_friends` t1 join user t2 on t1.user_name=t2.email")
        result=cursor.fetchall()
        friends=[[i[0],'online'  if i[1]==b'\x00' else 'offline']for i in result]
        return jsonify({'code':200,'data':friends,'message':'Friend list fetched successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Friend list fetching failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/friend/requests',methods=['GET'])
def getFriendRequests():
    email=request.args.get('email') 
    if not email:
        return jsonify({'code':400,'message':'Email is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("select inviter from friend_request where invitee=%s and status=0",(email))
        result=cursor.fetchall()
        requests=[i[0] for i in result]
        return jsonify({'code':200,'data':requests,'message':'Friend requests fetched successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Friend requests fetching failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/friend/accept',methods=['POST'])
def acceptRequests():
    data=request.get_json()
    email=data.get('email')
    friend=data.get('request')
    if not email:
        return jsonify({'code':400,'message':'Email is required'})
    if not friend:
        return jsonify({'code':400,'message':'Friend is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("update friend_request set status=1 where inviter=%s and invitee=%s",(friend,email))
        cursor.execute(f"insert into `{email}_friends` (user_name) values(%s)",(friend,))
        cursor.execute(f"insert into `{friend}_friends` (user_name) values(%s)",(email,))
        conn.commit()
        return jsonify({'code':200,'message':'Friend request accepted successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Friend request accepting failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/friend/messages',methods=['GET'])
def getFriendMessages():
    global username
    while not username:
        time.sleep(0.1)
    friend=request.args.get('email')
    email=username
    if not email:
        return jsonify({'code':400,'message':'User is not logged in'})
    if not friend:
        return jsonify({'code':400,'message':'Friend is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select id,sender,msg,datetime from `{email}_fm` where sender=%s or receiver=%s order by datetime asc",(friend,friend))
        messages=cursor.fetchall()
        return jsonify({'code':200,'data':messages,'message':'Friend messages fetched successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Friend messages fetching failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
#给好友发消息
@app.route('/api/friend/message',methods=['POST'])
def sendFriendMessage():
    global username
    while not username:
        time.sleep(0.1)
    data=request.get_json()
    email=data.get('email')
    message=data.get('message')
    if not email:
        return jsonify({'code':400,'message':'Email is required'})
    if not message:
        return jsonify({'code':400,'message':'Message is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        t=datetime.now()+timedelta(hours=-8)
        timestamp=t.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(f"insert into `{username}_fm` (sender,receiver,msg,datetime) values (%s,%s,%s,%s)",(username,email,message,timestamp))
        cursor.execute(f"select status from user where email=%s",(email,))
        status=cursor.fetchone()[0]
        if status==b'\x00':
            ip=''
            for i in udp_ips:
                if udp_ips[i]==email:
                    ip=i[0]
                    break
            try:
                tcp_sender=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                tcp_sender.connect((ip,TCP_PORT+1))
                tcp_sender.send((encrypt(f"MESSAGE_SEND:{username}:{email}:{message}").encode('utf-8')+b'\n'))
                return jsonify({'code':200,'message':'Message sent successfully'})
            except Exception as e:
                return jsonify({'code':500,'message':'Message sending failed'+str(e)})
            finally:
                tcp_sender.close()
                conn.commit()
        else:
            cursor.execute(f"insert into `{email}_fm` (sender,receiver,msg,datetime) values (%s,%s,%s,%s)",(username,email,message,timestamp))
            conn.commit()
        return jsonify({'code':200,'message':'Message sent successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Message sending failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/file/all',methods=['GET'])
def getAllFiles():
    if not username:
        return jsonify({'code':400,'message':'User is not logged in'})
    try:
        private_files=[f for f in os.listdir('C:/Users/HP/Desktop/chat/back/Private')]
        return jsonify({'code':200,'data':private_files,'message':'All files fetched successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Files directory is not found'+str(e)})
#给好友发文件
@app.route('/api/file/send',methods=['POST'])
def sendFile():
    global username
    while not username:
        time.sleep(0.1)
    data=request.get_json()
    email=data.get('email')
    file=data.get('file')
    if not email:
        return jsonify({'code':400,'message':'Email is required'})
    if not file:
        return jsonify({'code':400,'message':'File is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select status from user where email=%s",(email,))
        status=cursor.fetchone()[0]
        with open(f'C:/Users/HP/Desktop/chat/back/Private/{file}','rb') as f:
            file_data=f.read()
        t=datetime.now()+timedelta(hours=-8)
        timestamp=t.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(f"insert into `{username}_fm` (sender,receiver,msg,datetime) values (%s,%s,%s,%s)",(username,email,f"send file:{file}:{file_data}",timestamp))
        if status==b'\x00':
            ip=''
            for i in udp_ips:
                if udp_ips[i]==email:
                    ip=i[0]
                    break
            try:
                tcp_sender=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                tcp_sender.connect((ip,TCP_PORT+1))
                #conn.commit()提交 修改语句才会执行
                tcp_sender.send((encrypt(f"FILE_SEND:{username}:{email}:{file}:{str(len(file_data))}")).encode('utf-8')+b'\n')
                piece=4096
                for i in range(0,len(file_data),piece):
                    tcp_sender.sendall(file_data[i:i+piece])
                return jsonify({'code':200,'message':'File sending successfully'})
            except Exception as e:
                return jsonify({'code':500,'message':'File sending failed'+str(e)})
            finally:
                tcp_sender.close()
                conn.commit()
        else:
            cursor.execute(f"insert into `{email}_fm` (sender,receiver,msg,datetime) values (%s,%s,%s,%s)",(username,email,f"send file:{file}:{file_data}",timestamp))
            conn.commit()
            return jsonify({'code':200,'message':'File sending successfully'})
    finally:
        cursor.close()
        conn.close()
#读取好友文件
@app.route('/api/file/view',methods=['GET'])
def viewFriendFile():
    global username
    while not username:
        time.sleep(0.1)
    messageId=request.args.get('messageId')
    if not messageId:
        return jsonify({'code':400,'message':'Message ID is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select msg from `{username}_fm` where id=%s",(messageId,))
        msg=cursor.fetchone()
        if msg:
            return Response(ast.literal_eval(msg[0].split(':',2)[2]))
        return jsonify({'code':400,'message':'File not found'})
    except Exception as e:
        return jsonify({'code':500,'message':'File viewing failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/friend/saveFile',methods=['POST'])
def saveFriendFile():
    global username
    while not username:
        time.sleep(0.1)
    data=request.get_json()
    fileId=data.get('fileId')
    fileType=data.get('fileType')
    if not fileId:
        return jsonify({'code':400,'message':'File ID is required'})
    if not fileType:
        return jsonify({'code':400,'message':'File type is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select msg from `{username}_fm` where id=%s",(fileId,))
        result=cursor.fetchone()[0]
        content=result.split(":",2)[2]
        file_name=result.split(":",2)[1]
        file_type=fileType.capitalize()
        if content and file_name:
            ufilePath=file_name
            count=0
            while ufilePath in os.listdir(f"C:/Users/HP/Desktop/chat/back/{file_type}"):
                count+=1
                ufilePath=f"{file_name.rsplit('.')[0]}_{count}.{file_name.rsplit('.')[1]}"
            with open(f"C:/Users/HP/Desktop/chat/back/{file_type}/{ufilePath}","wb") as f:
                f.write(ast.literal_eval(content))
            return jsonify({'code':200,'message':'File saved successfully'})
        return jsonify({'code':400,'message':'File not found'})
    except Exception as e:
        return jsonify({'code':500,'message':'File saving failed'+str(e)})
@app.route('/api/group/create',methods=['POST'])
def createGroup():
    data=request.get_json()
    email=data.get('email')
    name=data.get('name')
    if not email:
        return jsonify({'code':400,'message':'Email is required'})
    if not name:
        return jsonify({'code':400,'message':'Name is required'})
    id=str(int(time.time()))
    if len(id)<15:
        id=str(int(time.time())%(10**(15-len(id))))+id
    else:
        id=id[:15]
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        while True:
            cursor.execute(f"select group_id from `group` where group_id=%s",(id,))
            group_id=cursor.fetchone()
            if group_id:
                id=str(int(time.time())%100000)+id[:10]
            else: 
                break
        cursor.execute(f"create table `group_{id}` (id int(11) auto_increment primary key,username varchar(255),active_status bit(1))")
        cursor.execute(f"insert into `group` (group_id,group_name) values (%s,%s)",(id,name))
        cursor.execute(f"insert into `{email}_groups` (group_id,group_name) values (%s,%s)",(id,name))
        cursor.execute(f"insert into `group_{id}` (username,active_status) values (%s,%s)",(email,b'\x00'))
        cursor.execute(f"select id from `{email}_groups` where group_id=%s",(id,))
        new=cursor.fetchone()
        conn.commit()
        send_to_group(new[0],f" User {email} created the group")
        return jsonify({'code':200,'data':{'email':email,'name':name},'message':'Group created successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Group creating failed'+str(e)})
    finally:
        cursor.close()
        conn.close()
@app.route('/api/group/join',methods=['POST'])
def joinGroup():
    data=request.get_json()
    email=data.get('email')
    name=data.get('name')
    if not email:
        return jsonify({'code':400,'message':'Email is required'})
    if not name:
        return jsonify({'code':400,'message':'Name is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select group_id,group_name from `group` where group_id=%s",(name,))
        group=cursor.fetchone()
        if group:
            cursor.execute(f"select id from `{email}_groups` where group_id=%s",(group[0],))
            id=cursor.fetchone()
            if id:
                return jsonify({'code':400,'message':'You have already joined this group'})
            cursor.execute(f"insert into `{email}_groups` (group_id,group_name) values (%s,%s)",(group[0],group[1]))
            cursor.execute(f"insert into `group_{group[0]}` (username,active_status) values (%s,%s)",(email,b'\x00'))
            conn.commit()
            cursor.execute(f"select id from  `{email}_groups` where group_id=%s",(name,))
            new=cursor.fetchone()
            print("new",new)
            send_to_group(new[0],f" User {email} joined the group")
            return jsonify({'code':200,'data':{'email':email,'name':name},'message':'Group joined successfully'})
        return jsonify({'code':400,'message':'Group not found'})
    except Exception as e:
        return jsonify({'code':500,'message':'Group joining failed'+str(e)})
    finally:
        cursor.close()
        conn.close()
PORT=50000;TCP_PORT=50001;oPORT=50003
BROADCAST="255.255.255.255"
my_ip=''
my_port=0
udp_ips={}
tcp_ips={}
key=5
def encrypt(text):
    res=""
    for i in text:
        res+=chr(ord(i)+key)
    return res
def decrypt(text):
    res=""
    for i in text:
        res+=chr(ord(i)-key)
    return res
#store group msg if in group,(group_no,sender,msg)
def store_msg(group_no,email,msg):
    global username
    while not username:
        time.sleep(0.1)
    t=datetime.now()+timedelta(hours=-8)
    timestamp=t.strftime('%Y-%m-%d %H:%M:%S')
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select id from `{username}_groups` where group_id=%s",(group_no,))
        count=cursor.fetchone()
        if count[0]==None:
            return False
        cursor.execute(f"insert into `{username}_gm` (group_id,sender,msg,datetime) values (%s,%s,%s,%s)",(count[0],email,msg,timestamp))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
#check whether user is in group and is active,param:group_no 
def check_in_group(group_id):
    global username
    while not username:
        time.sleep(0.1)
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select id from `{username}_groups` where group_id=%s",(group_id,))
        groupId=cursor.fetchone()
        cursor.execute(f"select active_status from `group_{group_id}` where username=%s",(username,))
        status=cursor.fetchone()
        if groupId and status[0]==b'\x00':
            return groupId[0]
        return None
    finally:
        if cursor:
            cursor.close()  
        if conn:
            conn.close()
def intoChat(sender):
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select group_id from `{sender}_groups` ")
        groups=cursor.fetchall()
        group_list=[i[0] for i in groups]
        if group_list:
            return group_list
        return []
    except Exception as e:
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def listen_for_group():
    global udp_ips,tcp_ips,my_port,client,my_ip
    node=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    node.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    node.bind(("",oPORT))
    _,my_port=node.getsockname()
    udata=b''
    while not username:
        time.sleep(0.1)
    while True:
        addr=None
        
        piece,addr=node.recvfrom(4096)
        udata+=piece
        while b'\n' in udata:
            print("udata",decrypt(udata.decode('utf-8')))
            msg_bytes, udata = udata.split(b'\n', 1)
            try:
                msg = decrypt(msg_bytes.decode('utf-8'))
            except:
                continue
            print("msg received",msg)
            parts=msg.split(':')
            if len(parts)<4 or username==parts[2]:
                udp_ips[addr]=parts[2]
                tcp_ips[(addr[0],TCP_PORT)]=parts[2]
                continue;
            parts=msg.split(':',4)
            if client:
                client.send("message update")
                print("message update")
            if parts[0]=='!join' and parts[2]!=username:
                udp_ips[addr]=parts[2]
                tcp_ips[(addr[0],TCP_PORT+1)]=parts[2]
                print(f"User {parts[2]} comes into the chat")
                group_list=intoChat(parts[2])
                for group in group_list:
                    group_id=check_in_group(group)
                    if group_id:
                        peer.sendto((encrypt(f"!welcome:{group_id}:{username}:{parts[2]} comes into the chat").encode('utf-8')+b'\n'),(BROADCAST,PORT))
            elif parts[0]=='!welcome' and parts[2]!=username:
                udp_ips[addr]=parts[2]
                tcp_ips[(addr[0],TCP_PORT+1)]=parts[2]
            elif parts[0]=='!leave' and parts[2]!=username:
                for user in udp_ips:
                    if udp_ips[user]==parts[2]:
                        del udp_ips[user]
                        break
                for user in tcp_ips:
                    if tcp_ips[user]==parts[2]:
                        del tcp_ips[user]
                        break
                group_list=intoChat(parts[2])
                for group in group_list:
                    group_id=check_in_group(group)
                    if group_id:
                        print(f"User {parts[2]} leaves the chat")
            elif parts[0]=='!msg' and parts[2]!=username :
                udp_ips[addr]=parts[2]
                timestamp=time.strftime('%H:%M:%S')
                group_id=check_in_group(parts[1])
                if group_id:
                    #store_msg(parts[1],parts[2],parts[3])
                    print(f"[{timestamp}] [{parts[1]}] {parts[2]}: {parts[3]}")
            elif parts[0]=='!files' and parts[2]!=username:
                udp_ips[addr]=parts[2]
                files=(",").join(get_group_files())
                group_id=check_in_group(parts[1])
                if group_id:
                    tcp_sender=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    tcp_sender.connect((addr[0],TCP_PORT+1))
                    tcp_sender.send((encrypt(f"FILE_LIST:{parts[1]}:{username}:{files}").encode('utf-8')+b'\n'))
                    my_ip=tcp_sender.getsockname()[0]
                    tcp_sender.close()
                    store_msg(parts[1],username,f"send file list: {files}")
                    db=get_db_connection()
                    cursor=db.cursor()
                    cursor.execute(f"select id from `{parts[2]}_groups` where group_id=%s",(parts[1],))
                    count=cursor.fetchone()
                    if count[0]==None:
                        return False
                    t=datetime.now()+timedelta(hours=-8)
                    timestamp=t.strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute(f"insert into `{parts[2]}_gm` (group_id,sender,msg,datetime) values (%s,%s,%s,%s)",(count[0],username,f"send file list: {files}",timestamp))
                    db.commit()
                    cursor.close()
                    db.close()
            elif parts[0]=='FILE_LIST' and parts[2]!=username:
                udp_ips[addr]=parts[2]
                timestamp=time.strftime('%H:%M:%S')
                group_id=check_in_group(parts[1])
                if group_id:
                    print(f"[{timestamp}] [{parts[1]}] {parts[2]}: {parts[3]}")
            elif parts[0]=='!search' and parts[2]!=username:
                udp_ips[addr]=parts[2]
                timestamp=time.strftime('%H:%M:%S')
                group_id=check_in_group(parts[1])
                if group_id:
                    store_msg(parts[1],parts[2],"search for "+parts[3])
                    print(f"[{timestamp}] [{parts[1]}] {parts[2]}: search for {parts[3]}")
                    search_for_files(parts[1],parts[2],parts[3])
#用户广播其他人查找文件                
def search_for_files(group_id,receiver,filename):
    files=get_group_files()
    file_list=[f for f in files if filename in f]
    send_file_list(group_id,file_list,receiver)
def send_file_list(group_id,file_list,receiver):
    print(file_list)
    for addr in udp_ips:
        if udp_ips[addr]==receiver:
            ip=addr[0]
            break
    for file in file_list:
        tcp_sender=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tcp_sender.connect((ip,TCP_PORT+1))
        with open(f'C:/Users/HP/Desktop/chat/back/Public/{file}','rb') as f:
            data=f.read()
        tcp_sender.send((encrypt(f"SEARCH_RESULT:{group_id}:{username}:{receiver}:{file}:{str(len(data))}")).encode('utf-8')+b'\n')
        store_msg(group_id,username,f"search result: {file}")
        db=get_db_connection()
        cursor=db.cursor()
        t=datetime.now()+timedelta(hours=-8)
        timestamp=t.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(f"select id from `{receiver}_groups` where group_id=%s",(group_id,))
        count=cursor.fetchone()
        if count[0]==None:
            return False
        cursor.execute(f"insert into `{receiver}_gm` (group_id,sender,msg,datetime) values (%s,%s,%s,%s)",(count[0],username,f"search result: {file}",timestamp))
        piece=4096
        for i in range(0,len(data),piece):
            tcp_sender.sendall(data[i:i+piece])
        store_msg(group_id,username,f"send file:{file}:{data}")
        cursor.execute(f"insert into `{receiver}_gm` (group_id,sender,msg,datetime) values (%s,%s,%s,%s)",(count[0],username,f"send file:{file}:{data}",timestamp))
        tcp_sender.close()
        db.commit()
        cursor.close()
        db.close()
def tcp_listener():
    global username
    while not username:
        time.sleep(0.1)
    listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    listener.bind(("",TCP_PORT))
    listener.listen()
    while True:
        conn,addr=listener.accept()
        data=b''
        while True:
            piece=conn.recv(4096)
            data+=piece
            if b'\n' in data:
                break
        msg=decrypt(data.split(b'\n')[0].decode('utf-8'));file=data.split(b'\n')[1]
        print("file",file)
        parts=msg.split(':')
        print("tcp message received",msg)
        if client:
            client.send("tcp message update")
            print("tcp message update")
        if parts[0]=='SEARCH_RESULT':
            username=parts[3]
            size=int(parts[5])
            data=b''
            if file:
                data=file
            
            while len(data)<size:
                piece=conn.recv(4096)
                data+=piece
            print(f"send file:{parts[4]}:{data}")
        elif parts[0]=='FILE_SEND':
            username=parts[2]
            size=int(parts[4])
            data=b''
            if file:
                data=file
            while len(data)<size:
                piece=conn.recv(4096)
                data+=piece
            try:
                db=get_db_connection()
                cursor=db.cursor()
                t=datetime.now()+timedelta(hours=-8)
                timestamp=t.strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(f"insert into `{username}_fm` (sender,receiver,msg,datetime) values (%s,%s,%s,%s)",(parts[1],parts[2],f"send file:{parts[3]}:{data}",timestamp))
                print(f"send file:{parts[3]}:{data}")
                db.commit()
            except Exception as e:
                return jsonify({'code':500,'message':'File sending failed'+str(e)})
            finally:
                cursor.close()
                db.close()
        #纠错：tcp连接建立后及时关闭 socket不能重复使用
        elif parts[0]=='!files' and parts[2]!=username:
            files=(",").join(get_group_files())
            tcp_sender=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            t=datetime.now()-timedelta(hours=-8)
            timestamp=t.strftime("%Y-%m-%d %H:%M:%S")
            try:
                tcp_sender.connect((addr[0],TCP_PORT+1))
                tcp_sender.send(encrypt(f"FILE_LIST:{parts[1]}:{username}:{files}").encode()+b'\n')
                store_msg(parts[1],username,files)
            except:
                print("User are not online")
            finally:
                tcp_sender.close()
        elif parts[0]=='FILE_LIST':
            store_msg(parts[1],parts[2],parts[3])
            print(f"FILE_LIST: {parts[3]}")
        elif parts[0]=='MESSAGE_SEND':
            username=parts[2]
            message=parts[3]
            db=get_db_connection()
            cursor=db.cursor()
            t=datetime.now()+timedelta(hours=-8)
            timestamp=t.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(f"insert into `{username}_fm` (sender,receiver,msg,datetime) values (%s,%s,%s,%s)",(parts[1],parts[2],message,timestamp))
            db.commit()
            cursor.close()
            db.close()
            print(f"[{timestamp}] [{parts[1]}] {parts[2]}: {message}")
@app.route('/api/files',methods=['GET'])
def getFiles():
    if not username:
        return jsonify({'code':400,'message':'User not logged in'})
    try:
        public_files=[f for f in os.listdir('C:/Users/HP/Desktop/chat/back/Public')]
        private_files=[f for f in os.listdir('C:/Users/HP/Desktop/chat/back/Private')]
        return jsonify({'code':200,'data':{'publicFiles':public_files,'privateFiles':private_files},'message':'Files fetched successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Files fetching failed'+str(e)})
@app.route('/api/file/content',methods=['GET'])
def getFileContent():
    file=request.args.get('file')
    file_type=request.args.get('fileType').capitalize()
    if not file:
        return jsonify({'code':400,'message':'File is required'})
    if not username:
        return jsonify({'code':400,'message':'User not logged in'})
    try:
        with open(f'C:/Users/HP/Desktop/chat/back/{file_type}/{file}','rb') as f:
            data=f.read()
        return Response(data)
    except Exception as e:
        return jsonify({'code':500,'message':'File content fetching failed'+str(e)})
@app.route('/api/file/upload',methods=['POST'])
def uploadFile():
    file=request.files['file']
    fileType=request.form.get('fileType')
    if not file:
        return jsonify({'code':400,'message':'File is required'})
    if not fileType:
        return jsonify({'code':400,'message':'File type is required'})
    file_type=fileType.capitalize()
    path=f'{file.filename}'
    upath=path
    count=0
    while upath in os.listdir(f'C:/Users/HP/Desktop/chat/back/{file_type}'):
        count+=1
        upath=path.rsplit('.')[0]+f"_{count}."+path.rsplit('.')[1]
    file.save(f'C:/Users/HP/Desktop/chat/back/{file_type}/{upath}')
    return jsonify({'code':200,'message':'File uploaded successfully'})
@app.route('/api/group/members',methods=['GET'])
def getGroupMembers():
    group_id=request.args.get('groupId')
    if not group_id:
        return jsonify({'code':400,'message':'Group ID is required'})
    if not username:
        return jsonify({'code':400,'message':'User not logged in'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select group_id from `{username}_groups` where id=%s",(group_id,))
        group_no=cursor.fetchone()
        cursor.execute(f"select id,username from `group_{group_no[0]}`")
        result=cursor.fetchall()
        return jsonify({'code':200,'data':result,'message':'Group members fetched successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Group members fetching failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def getActiveUsers(group_id):
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select email from user where `STATUS`=0 and email in (select username from `group_{group_id}` where active_status=0)")
        users=cursor.fetchall()
        users_list=[i[0] for i in users]
        return users_list
    except Exception as e:
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def getUsers(group_id):
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select username from `group_{group_id}` where active_status=0")
        users=cursor.fetchall()
        users_list=[i[0] for i in users]
        return users_list
    except Exception as e:
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


#send group messages,params:(personal group id,common msg)
def send_to_group(group_id,msg):
    global username
    while not username:
        time.sleep(0.1)
    conn=get_db_connection()
    cursor=conn.cursor()
    timestamp=time.strftime('%H:%M:%S')
    t=datetime.now()+timedelta(hours=-8)
    t2=t.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(f"insert into `{username}_gm` (group_id,sender,msg,datetime) values (%s,%s,%s,%s)",(group_id,username,msg,t2))
    cursor.execute(f"select group_id from `{username}_groups` where id= %s",(group_id,))
    group_no=cursor.fetchone()
    peer.sendto((encrypt(f"!msg:{group_no[0]}:{username}:{msg}").encode('utf-8')+b'\n'),(BROADCAST,PORT))
    print(f"[{timestamp}] [{group_no[0]}] {username}: {msg}")
    conn.commit()
    cursor.close()
    conn.close()
@app.route('/api/group/logout',methods=['POST'])
def logout():
    global username,udp_ips,my_ip,my_port,client
    data=request.get_json()
    email=data.get('email')
    if not email:
        return jsonify({'code':400,'message':'Email is required'})
    if username==email or username=='':
        peer.sendto((encrypt(f"!leave:ALL:{username}:bye").encode('utf-8')+b'\n'),(BROADCAST,PORT))
        groups=intoChat(username)
        try:
            conn=get_db_connection()
            cursor=conn.cursor()
            cursor.execute(f"update user set status=1 where email=%s",(email,))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(e)
        username=''
        udp_ips.clear();my_ip=''; my_port=0;tcp_ips.clear();
        if client:
            client.close()
        client=None
        return jsonify({'code':200,'message':'Logout successfully'})
    return jsonify({'code':400,'message':'Email is incorrect'})
def get_group_files():
    path="C:/Users/HP/Desktop/chat/back/Public"
    return [f for f in os.listdir(path)]
#get filelist
@app.route('/api/group/files',methods=['GET'])
def getGroupFiles():
    groupId=request.args.get('groupId')
    if not groupId:
        return jsonify({'code':400,'message':'Group ID is required'})
    if not username:
        return jsonify({'code':400,'message':'User not logged in'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select group_id  from `{username}_groups` where id=%s",(groupId,))
        group_id=cursor.fetchone()
       
        tcp_users=[i for i in tcp_ips if tcp_ips[i] in getUsers(group_id[0])]
        print("tcp_u",tcp_users,tcp_ips)
        for i in tcp_users:
            try:
                tcp_sender=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                tcp_sender.connect(i)
                tcp_sender.send((encrypt(f"!files:{group_id[0]}:{username}:get group files").encode('utf-8')+b'\n'))
                print(f"TCP:get group files")
            except:
                print("Receivers are not online")
        #peer.sendto((encrypt(f"!files:{group_id[0]}:{username}:get group files").encode('utf-8')+b'\n'),(BROADCAST,PORT))
                
            finally:
                tcp_sender.close()
        return jsonify({'code':200,'message':'Group files fetched successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Group files fetching failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/group/messages',methods=['GET'])
def getGroupMessages():
    groupId=request.args.get('groupId')
    if not groupId:
        return jsonify({'code':400,'message':'Group ID is required'})
    if not username:
        return jsonify({'code':400,'message':'User not logged in'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select id,sender,msg,datetime from `{username}_gm` where group_id=%s order by datetime asc",(groupId,))
        result=cursor.fetchall()
        return jsonify({'code':200,'data':result,'message':'Group messages fetched successfully'})
    except Exception as e:  
        return jsonify({'code':500,'message':'Group messages fetching failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/group/users',methods=['GET'])
def getGroupUsers():
    groupId=request.args.get('groupId')
    if not groupId:
        return jsonify({'code':400,'message':'Group ID is required'})
    if not username:
        return jsonify({'code':400,'message':'User not logged in'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select group_id from `{username}_groups` where id= %s",(groupId,))
        group_no=cursor.fetchone()
        group_id=check_in_group(group_no[0])
        store_msg(group_no[0],username,f"get group active users")
        if group_id:
            users=getActiveUsers(group_no[0])
            group_user=[u for  u in users]
            print("udp_ips",udp_ips)
            print("users",users)
            print("group_user",group_user)
            group_user=(",").join(list(set(group_user)))
            store_msg(group_no[0],username,f"{group_user}")
        return jsonify({'code':200,'message':'Group users fetched successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Group users fetching failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
#群组发消息
@app.route('/api/group/sendMessage',methods=['POST'])
def sendMessage():
    global peer
    data=request.get_json()
    group_id=data.get('groupId')
    username=data.get('username')
    message=data.get('message')
    if not group_id:
        return jsonify({'code':400,'message':'Group ID is required'})
    if not username:
        return jsonify({'code':400,'message':'Username is required'})
    if not message:
        return jsonify({'code':400,'message':'Message is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select group_id from `{username}_groups` where id=%s",(group_id,))
        group_no=cursor.fetchone()
        peer.sendto((encrypt(f"!msg:{group_no[0]}:{username}:{message}").encode('utf-8')+b'\n'),(BROADCAST,PORT))
        if group_no:
            group_users=getUsers(group_no[0])
            for i in group_users:
                t=datetime.now()+timedelta(hours=-8)
                timestamp=t.strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(f"select id from `{i}_groups` where group_id=%s",(group_no[0],))
                groupId=cursor.fetchone()
                cursor.execute(f"insert into `{i}_gm` (group_id,sender,msg,datetime) values (%s,%s,%s,%s)",(groupId[0],username,message,timestamp))
                conn.commit()
        return jsonify({'code':200,'message':'Message sent successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Message sending failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/group/exit',methods=['POST'])
def exitGroup():
    global udp_ips
    data=request.get_json()
    group_id=data.get('groupId')
    if not group_id:
        return jsonify({'code':400,'message':'Group ID is required'})
    if not username:
        return jsonify({'code':400,'message':'User not logged in'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select group_id from `{username}_groups` where id=%s",(group_id,))
        group_no=cursor.fetchone()
        cursor.execute(f"update `group_{group_no[0]}` set active_status=%s where username=%s",(1,username))
        conn.commit()
        udp_ips.clear()
        return jsonify({'code':200,'message':'Group exited successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Group exiting failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/group/into',methods=['POST'])
def intoGroup():
    data=request.get_json()
    group_id=data.get('groupId')
    if not group_id:
        return jsonify({'code':400,'message':'Group ID is required'})
    if not username:
        return jsonify({'code':400,'message':'User not logged in'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select group_id from `{username}_groups` where id=%s",(group_id,))
        group_no=cursor.fetchone()
        cursor.execute(f"update `group_{group_no[0]}` set active_status=%s where username=%s",(0,username))
        conn.commit()
        peer.sendto((encrypt(f"!join:{group_no[0]}:{username}:hello").encode('utf-8')+b'\n'),(BROADCAST,PORT))
        return jsonify({'code':200,'message':'Group into successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Group into failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/group/activeStatus',methods=['GET'])
def getActiveStatus():
    groupId=request.args.get('groupId')
    if not groupId:
        return jsonify({'code':400,'message':'Group ID is required'})
    if not username:
        return jsonify({'code':400,'message':'User not logged in'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select group_id from `{username}_groups` where id=%s",(groupId,))
        group_no=cursor.fetchone()
        cursor.execute(f"select active_status from `group_{group_no[0]}` where username=%s",(username,))
        status=cursor.fetchone()
        active_status=True if status[0]==b'\x00' else False
        return jsonify({'code':200,'data':active_status,'message':'Active status fetched successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Active status fetching failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/group/searchFiles',methods=['GET'])
def searchFiles():
    groupId=request.args.get('groupId')
    filename=request.args.get('filename')
    if not groupId:
        return jsonify({'code':400,'message':'Group ID is required'})
    if not filename:
        return jsonify({'code':400,'message':'Filename is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select group_id from `{username}_groups` where id=%s",(groupId,))
        group_no=cursor.fetchone()
        peer.sendto((encrypt(f"!search:{group_no[0]}:{username}:{filename}").encode('utf-8')+b'\n'),(BROADCAST,PORT))
        store_msg(group_no[0],username,f"search for {filename}")
        return jsonify({'code':200,'message':'Search files successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Search files failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/group/viewFile',methods=['GET'])
def viewFile():
    messageId=request.args.get('messageId')
    if not messageId:
        return Response("Message id is not given")
    if not username:
        return Response("User not logged in")
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select msg from `{username}_gm` where id=%s",(messageId,))
        msg=cursor.fetchone()[0]
        file=msg.split(":",2)[2]
        return Response(ast.literal_eval(file))
    except Exception as e:
        return Response("View file failed"+str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
@app.route('/api/group/saveFile',methods=['POST'])
def saveFile():
    data=request.get_json()
    file_id=data.get('fileId')
    file_type=data.get('fileType')
    if not file_id:
        return jsonify({'code':400,'message':'File ID is required'})
    if not file_type:
        return jsonify({'code':400,'message':'File type is required'})
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select msg from `{username}_gm` where id=%s",(file_id,))
        msg=cursor.fetchone()[0]
        filename=msg.split(":",2)[1]
        file=msg.split(":",2)[2]
        ufilename=filename
        count=0
        file_type=file_type.capitalize()
        while os.path.exists(f'C:/Users/HP/Desktop/chat/back/{file_type}/{ufilename}'):
            count+=1
            ufilename=filename.rsplit('.')[0]+'_'+str(count)+'.'+filename.rsplit('.')[1]
        with open(f'C:/Users/HP/Desktop/chat/back/{file_type}/{ufilename}','wb') as f:
            f.write(ast.literal_eval(file))
        return jsonify({'code':200,'message':'File saved successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'File saving failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
peer=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
peer.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
def getrealip():
    global my_ip
    tcp_sender=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        tcp_sender.connect(("8.8.8.8",80))
        my_ip=tcp_sender.getsockname()[0]
    except:
        tcp_sender.close()
if __name__=='__main__':
    threading.Thread(target=listen_for_group).start()
    threading.Thread(target=tcp_listener).start()
    threading.Thread(target=getrealip).start()
    app.run(host='0.0.0.0', port=5000, debug=True)
