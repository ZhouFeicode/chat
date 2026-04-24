from flask import Flask,request,jsonify,Response
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
app=Flask(__name__)
username=''
CORS(app,resources={r"/api/*": {"origins": "http://localhost:5173"}})
# 邮箱配置
EMAIL_HOST = 'smtp.sina.com'
EMAIL_PORT = 465
EMAIL_USER = 'amailabao@sina.com'
EMAIL_PASS ='0c6e8d5c85b74cfe'
EXPIRE_CODE=[]
def get_db_connection():
    conn=pymysql.connect(host='localhost',user='root',password='root',database='chat',charset='utf8mb4')
    return conn
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
    global EXPIRE_CODE,username,my_port,udp_ips
    print("ex",EXPIRE_CODE)
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
        return jsonify({'code':200,'data':{'email':email},'message':'login successfully'})
    if result and result[0] and not result[1]:
        return jsonify({'code':201,'data':{'email':email},'message':'no password, please set password'})
    peer.sendto(encrypt(f"!join:ALL:{username}:hello").encode('utf-8'),(BROADCAST,PORT))
    _,my_port=peer.getsockname()
    print("my_address:",my_ip,my_port)
    udp_ips[(my_ip,my_port)]=username
    cursor.execute("insert into user (email) values (%s)",(email,))
    table_name=email+'_groups'
    sql=f""" create table `{table_name}` (id int auto_increment primary key,
    group_id bigint(20),group_name varchar(255))ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"""
    cursor.execute(sql)
    table_name=email+'_friends'
    sql=f""" create table `{table_name}` (id int auto_increment primary key,
    user_name varchar(255))ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"""
    cursor.execute(sql)
    table_name=email+'_gm'
    sql=f""" create table `{table_name}` (id int auto_increment primary key,
    group_id bigint(20),sender varchar(255),msg text,datetime datetime)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"""
    cursor.execute(sql)
    table_name=email+'_fm'
    sql=f""" create table `{table_name}` (id int auto_increment primary key,
    sender varchar(255),msg text,datetime datetime)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"""
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
        cursor.close()
        conn.close()
        return jsonify({'code':200,'data':{'email':email},'message':'Setting password successfully'})
    except:
        return jsonify({'code':500,'message':'Setting password failed'})
@app.route('/api/accountLogin',methods=['POST'])
def accountLogin():
    global username,my_port,udp_ips
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
            peer.sendto(encrypt(f"!join:ALL:{username}:hello").encode('utf-8'),(BROADCAST,PORT))
            _,my_port=peer.getsockname()
            print("my_address:",my_ip,my_port)
            udp_ips[(my_ip,my_port)]=username
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
        cursor.execute(f"insert into `group` (group_id,group_name) values (%s,%s)",(id,name))
        cursor.execute(f"insert into `{email}_groups` (group_id,group_name) values (%s,%s)",(id,name))
        cursor.execute(f"insert into `group_{id}` (username) values (%s)",(email,))
        cursor.execute(f"select id from `{email}_groups` where group_id=%s",(id,))
        new=cursor.fetchone()
        conn.commit()
        send_to_group(new[0],f" User {email} created the group")
        return jsonify({'code':200,'data':{'email':email,'name':name},'message':'Group created successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Group creating failed'})
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
            cursor.execute(f"select id from  `{email}_groups` where group_id=%s",(name,))
            new=cursor.fetchone()
            conn.commit()
            send_to_group(new[0],f" User {email} joined the group")
            return jsonify({'code':200,'data':{'email':email,'name':name},'message':'Group joined successfully'})
        return jsonify({'code':400,'message':'Group not found'})
    except Exception as e:
        return jsonify({'code':500,'message':'Group joining failed'+str(e)})
    finally:
        cursor.close()
        conn.close()
PORT=50000;TCP_PORT=50001
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
        return False
    except Exception as e:
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def listen_for_group():
    global udp_ips,my_port
    node=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    node.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    node.bind(("",PORT))
    _,my_port=node.getsockname()
    while not username:
        time.sleep(0.1)
    while True:
        data,addr=node.recvfrom(5096)
        msg=decrypt(data.decode('utf-8'))
        parts=msg.split(':')
        print("username",username)
        if len(parts)<4:
            continue
        parts=msg.split(':',4)
        if parts[0]=='!join' and parts[2]!=username:
            udp_ips[addr]=parts[2]
            print(f"User {parts[2]} comes into the chat")
            group_list=intoChat(parts[2])
            for group in group_list:
                store_msg(group,parts[2],"comes into the chat")
                group_id=check_in_group(group)
                if group_id:
                    send_to_group(group_id,"welcome "+parts[2]+" comes into the chat")
        elif parts[0]=='!msg' and parts[2]!=username :
            udp_ips[addr]=parts[2]
            timestamp=time.strftime('%H:%M:%S')
            group_id=check_in_group(parts[1])
            if group_id:
                store_msg(parts[1],parts[2],parts[3])
                print(f"[{timestamp}] [{parts[1]}] {parts[2]}: {parts[3]}")
        elif parts[0]=='!files' and parts[2]!=username:
            udp_ips[addr]=parts[2]
            files=(",").join(get_group_files())
            group_id=check_in_group(parts[1])
            if group_id:
                peer.sendto(encrypt(f"FILE_LIST:{parts[1]}:{username}:{files}").encode('utf-8'),(BROADCAST,PORT))
        elif parts[0]=='FILE_LIST' and parts[2]!=username:
            udp_ips[addr]=parts[2]
            timestamp=time.strftime('%H:%M:%S')
            group_id=check_in_group(parts[1])
            if group_id:
                store_msg(parts[1],parts[2],parts[3])
                print(f"[{timestamp}] [{parts[1]}] {parts[2]}: {parts[3]}")
        elif parts[0]=='!search' and parts[2]!=username:
            udp_ips[addr]=parts[2]
            timestamp=time.strftime('%H:%M:%S')
            group_id=check_in_group(parts[1])
            if group_id:
                store_msg(parts[1],parts[2],"search for "+parts[3])
                print(f"[{timestamp}] [{parts[1]}] {parts[2]}: search for {parts[3]}")
                search_for_files(parts[1],parts[2],parts[3])
        elif parts[0]=='!users' and  parts[2]==username:
            udp_ips[addr]=parts[2]
            timestamp=time.strftime('%H:%M:%S')
            group_id=check_in_group(parts[1])
            if group_id:
                users=getUsers(parts[1])
                group_user=[u for u in udp_ips.values() if u in users]
                group_user=(",").join(list(set(group_user)))
                peer.sendto(encrypt(f"USER_LIST:{parts[1]}:{username}:{group_user}").encode('utf-8'),(BROADCAST,PORT))
                print(f"[{timestamp}] [{parts[1]}] {username}: {group_user}")
        elif parts[0]=='USER_LIST' and parts[2]==username:
            udp_ips[addr]=parts[2]
            timestamp=time.strftime('%H:%M:%S')
            group_id=check_in_group(parts[1])
            if group_id:
                store_msg(parts[1],parts[2],parts[3])
                print(f"[{timestamp}] [{parts[1]}] {parts[2]}: {parts[3]}")
def search_for_files(group_id,receiver,filename):
    files=get_group_files()
    file_list=[f for f in files if filename in f]
    send_file_list(group_id,file_list,receiver)
def send_file_list(group_id,file_list,receiver):
    for addr in udp_ips:
        if udp_ips[addr]==receiver:
            ip=addr[0]
            break
    tcp_sender=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_sender.connect((ip,TCP_PORT+1))
    for file in file_list:
        with open(f'C:/Users/HP/Desktop/chat/back/Public/{file}','rb') as f:
            data=f.read()
            tcp_sender.send(encrypt(f"SEARCH_RESULT:{group_id}:{username}:{receiver}:{file}:{len(data)}").encode('utf-8'))
            store_msg(group_id,username,f"search result: {file}")
            tcp_sender.sendall(data)
            store_msg(group_id,username,f"send file:{file}:{data}")
    tcp_sender.close()
def tcp_listener():
    global username
    listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    listener.bind(("",TCP_PORT))
    listener.listen()
    while True:
        conn,addr=listener.accept()
        data=conn.recv(5096)
        msg=data.decode('utf-8')
        parts=msg.split(':')
        if parts[0]=='SEARCH_RESULT':
            username=parts[3]
            store_msg(parts[1],parts[2],f"search result: {parts[4]}")
            size=int(parts[5])
            data=conn.recv(size+1024)
            store_msg(parts[1],parts[2],f"send file:{parts[4]}:{data}")
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
def getUsers(group_id):
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute(f"select username from `group_{group_id}`")
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
    conn=get_db_connection()
    cursor=conn.cursor()
    timestamp=time.strftime('%H:%M:%S')
    t=datetime.now()+timedelta(hours=-8)
    t2=t.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(f"insert into `{username}_gm` (group_id,sender,msg,datetime) values (%s,%s,%s,%s)",(group_id,username,msg,t2))
    cursor.execute(f"select group_id from `{username}_groups` where id= %s",(group_id,))
    group_no=cursor.fetchone()
    peer.sendto(encrypt(f"!msg:{group_no[0]}:{username}:{msg}").encode('utf-8'),(BROADCAST,PORT))
    print(f"[{timestamp}] [{group_no[0]}] {username}: {msg}")
    conn.commit()
    cursor.close()
    conn.close()
@app.route('/api/group/logout',methods=['POST'])
def logout():
    global username
    data=request.get_json()
    email=data.get('email')
    if not email:
        return jsonify({'code':400,'message':'Email is required'})
    if username==email or not username:
        username=''
        return jsonify({'code':200,'message':'Logout successfully'})
    return jsonify({'code':400,'message':'Email is incorrect'})
def get_group_files():
    path="C:/Users/HP/Desktop/chat/back/Public"
    return [f for f in os.listdir(path)]
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
        peer.sendto(encrypt(f"!files:{group_id[0]}:{username}:get group files").encode('utf-8'),(BROADCAST,PORT))
        return jsonify({'code':200,'message':'Group files fetched successfully'})
    except:
        return jsonify({'code':500,'message':'Group files fetching failed'})
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
        peer.sendto(encrypt(f"!users:{group_no[0]}:{username}:get group users").encode('utf-8'),(BROADCAST,PORT))
        store_msg(group_no[0],username,"get group active users")
        return jsonify({'code':200,'message':'Group users fetched successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Group users fetching failed'+str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
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
        send_to_group(group_id,message)
        return jsonify({'code':200,'message':'Message sent successfully'})
    except Exception as e:
        return jsonify({'code':500,'message':'Message sending failed'+str(e)})
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
        peer.sendto(encrypt(f"!search:{group_no[0]}:{username}:{filename}").encode('utf-8'),(BROADCAST,PORT))
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
        file=msg.split(":")[2]
        return Response(file)
    except Exception as e:
        return Response("View file failed"+str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
peer=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
peer.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
if __name__=='__main__':
    threading.Thread(target=listen_for_group).start()
    try:
        client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect(("localhost",10000))
        my_ip,_=client.getsockname()
    except Exception as e:
        print("Error getting my address:",e)
    threading.Thread(target=tcp_listener).start()
    app.run(debug=True,host='0.0.0.0',port=5000)
    
