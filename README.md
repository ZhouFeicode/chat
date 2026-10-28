加密、查看所有/在线用户、文件、
msg:群号/friend：用户名:类型：内容
0.join 1.msg 2.file 3.fileinfo 4.allusers 5.activeusers
6.退出群聊 7.加解密 8.发文件 8.存文件
私聊：
0.加好友 1.发消息 2.发文件
文件：
1.上传、查看、下载
This template should help get you started developing with Vue 3 in Vite.
ascii:1字节，0-127位数
unicode:万国码，不固定字节，0-127照搬ascii
# 接口要返回值，js文件定义了return res.data
功能逻辑：
1.群组消息：
def sendMessage: 
sento(encrypt(f"!msg:{groupNo}:{username}:{msg}").encode()+b'\n',(BROADCAST,PORT)) 发送不存数据库
遍历群组所有成员，插入各自表
groupUsers=[u for u in getUsers()]
2.获取在线用户：
store_msg(groupNo,username,"get group acitve users")
groupUsers=[i for i in udp_ips.values() in getUsers() ]
userlist=(",").join(list(set(groupUsers)))
store_msg(groupNo,username,userlist)
# udp_ips数组
3.群组获取文件列表
在线活跃在群用户，遍历发送请求：
tcp_users=[i for i in tcp_ips if tcp_ips[i] in getUsers(group_id[0])]
for i in tcp_user:
tcp_sender.connect(i)
tcp_sender.send(encrypt(f"!files:{groupNo}:{username}:get group files").encode()+b'\n')
tcp_listener():
parts[0]=='!files' and parts[2]!=username:
files=get_group_files()
tcp_sender.send(encrypt(f"FILE_LIST:{parts[1]}:{username}:{files}").encode()+b'\n')
store_msg(parts[1],username,files)
对方：
parts[0]=='FILE_LIST':
store_msg(parts[1],parts[2],parts[3])
4.群组搜索文件
peer.sendto(encrypt(f"!search:{groupNo}:{username}:{file}").encode(),(BROADCAST,PORT))
store_msg(groupNo,username,{file})
listen_for_group():
store_msg(parts[1],parts[2],parts[3])
send_file_list():
for f in filelist:
data=f.read()
tcp_sender.send(encrypt(f"SEARCH RESULT:{groupNo}:{receiver}:{f}"))
for i in range(0,len(data),4096):
tcp_sender.sendall(data[i:i+4096])
接受方：
cursor.execute(f"insert into `{parts[2]}_gm` values()")
cursor.execute(f"insert into `{parts[2]}_gm` values()")
5.好友信息：
if status[0]=b'\x00'
tcp_sender.sendto(encrypt(f"MESSAGE SEND:{username}:{user}:{msg}"))
接收方：
if parts[0]=='MESSAGE SEND':
cursor.execute(f"insert into `{username}_fm` (sender,receiver,msg,datetime) values(%s,%s,%s,%s))
else:
cursor.execute(f"insert into `{email}_fm` (sender,receiver,msg,datetime) values(%s,%s,%s,%s))
6.好友文件：
cursor.execute(f"insert into `{username}_fm` (sender,receiver,msg,datetime) values(%s,%s,%s,%s))
if status[0]==b'\x00':
tcp_sender.send(encrypt(f"FILE SEND:{username}:{email}:{file}:{str(len(data))}"))
for i in range(0,len(data),4096):
tcp_sender.sendall(data[i:i+4096])
接收方：
data=b''
while True:
piece=conn.recv(4096)
data+=piece
if b'\n' in data:
break
msg,file=data.split(b'\n')[0],data.split(b'\n')[1]
if parts[1]=='FILE SEND':
cursor.execute(f"insert into `{parts[2]}_fm` ("") values())
7.好友查看文件：
8.好友保存文件：
9.上传文件：
10.查看文件：




