<template>
    <div class="home-container">
        <div class="menu-container">
        <div class="user-info">
         <img src="@/assets/user.png" class="user-img">
        </div>
        <el-menu
:default-active="activeIndex"
class="el-menu-vertical"
mode="vertical"
router
@select="handleSelect"
        >
            <el-menu-item  class="menu-item" index="/home/files">
                <img src="@/assets/message.png" class="menu-img">
                <span>Files</span>
            </el-menu-item>
            <el-menu-item  class="menu-item" index="/home/friends">
                <img src="@/assets/friend.png" class="menu-img">
                <span>Friends</span>
            </el-menu-item>
            <el-menu-item  class="menu-item" index="/home/groups">
                <img src="@/assets/group.png" class="menu-img">
                <span>Groups</span>
            </el-menu-item>
        </el-menu>
        </div>
        <div class="headline-container">
        <router-view @activateGroup="activateGroup" @activateFriend="activateFriend" @activateFile="activateFile" :fetch="fetch" @updateFetch="updateFetch" :refresh="refresh" @updateRefresh="updateRefresh"/>
        </div>
        <div v-if="activeGroup[0]" class="content-container">
        <div class="message-header">
        <div class="group-name-container">
        <span >{{activeGroup[2]}}:{{activeGroup[1]}}</span>
        </div>
        <div class="group-buttons">
        <el-button style="width:70px;" :icon="Notebook" @click="viewMembers">Users</el-button>
        <el-button @click="exitGroup"><img v-if="ingroup" src="@/assets/out.png" class="user-img">{{groupstatus}}</el-button>
        </div>
        </div>
        <div class="message-content">
        <div class="message-item" v-for="message in messages" :key="message[0]">
        <div class="message-item-container">
        <span class="item-sender">{{message[1]}}:</span>
        <div v-if="message[2].file" class="item-package" @click="viewFile(message[0],message[2].file)">
         <span style="width:80%" >{{message[2].file}}</span>
         <img class="file-img" src="@/assets/file.png">
        </div >
       <span  v-else-if="message[1]!=username" class="item-content" >{{message[2]}}</span>
        <span v-else class="item-content-self">{{message[2]}}</span>
        <span class="item-datetime">{{convertDate(message[3])}}</span>
         </div>
        </div>
        </div>
        <div v-if="showMembers" :class="{'members-container':showMembers}">
        <span v-for="member in members" :key="member[0]" class="member-name">{{member[1]}}</span>
        </div>
        <div v-if="ingroup" class="send-message-container">
        <el-input v-model="message" class="message-input" placeholder="Enter your message" />
        <div class="action-buttons">
        <el-button :icon="Folder" @click="viewFiles">Files</el-button>
        <el-button :disabled="!message" style="width:80px;" :icon="Search" @click="searchFiles">Search</el-button>
        <el-button  @click="getUsers"><img src="@/assets/user.png" class="user-img">Active</el-button>
        <el-button :disabled="!message" type="primary" @click="sendMessage" >Send</el-button>
        </div>
        </div>
        </div>
        <!-- Friend content -->
               <div v-if="activeFriend[0]" class="content-container">
        <div class="message-header">
        <div class="friend-name-container">
        <span >{{activeFriend[0]}}</span>
        </div>
        </div>
        <div class="message-content">
        <div class="message-item" v-for="message in messages" :key="message[0]">
        <div class="message-item-container">
        <span class="item-sender">{{message[1]}}:</span>
        <div v-if="message[2]['file']" class="item-package" @click="viewFriendFile(message[0],message[2].file)">
         <span style="width:80%" >{{message[2].file}}</span>
         <img class="file-img" src="@/assets/file.png">
        </div >
       <span  v-else-if="message[1]!=username" class="item-content" >{{message[2]}}</span>
        <span v-else class="item-content-self">{{message[2]}}</span>
        <span class="item-datetime">{{convertDate(message[3])}}</span>
         </div>
        </div>
        </div>
        <div class="send-message-container">
        <el-input v-model="message" class="message-input" placeholder="Enter your message" />
        <div class="action-buttons">
        <el-button @click="selectFile">Select</el-button>
        <el-button :disabled="!message" type="primary" @click="sendFriendMessage" >Send</el-button>
        </div>
        </div>
        </div>
        <!-- Friend content -->
         <div v-if="file.name || friendfile.name || activeFile[0]" class="file-container">
        <div class="file-header">
        <el-icon style="width:30px" size="20" @click="returnGroup"><ArrowLeft /></el-icon>
        <span style="width:90%;">{{file.name || friendfile.name || activeFile[0]}}</span>
        <el-button v-if="file.name || friendfile.name" @click="showFileDialog=true" :icon="Download">Save</el-button>
       <el-button v-if="activeFile[0]" @click="showUploadDialog=true" style="width:80px;height:30px;"  :icon="Upload">Upload</el-button>
        </div>
        <div class="file-content" v-if="file.name ">
        <el-input type="textarea" v-model="file.content" :rows="60" :cols="50" />
        </div>
        <div class="file-content" v-if="friendfile.name ">
        <el-input type="textarea" v-model="friendfile.content" :rows="60" :cols="50" />
        </div>
        <div class="file-content" v-if="activeFile[0]">
        <el-input type="textarea" v-model="activeFile[1]" :rows="60" :cols="50" />
        </div>
        </div>
        <!-- Select File Dialog -->
        <el-dialog v-model="showSelectDialog" title="Select File" width="600px">
        <div class="private-folder">
        <span>Private File:</span>
        <el-radio  class="file-radio" v-model="selectedFile" v-for="file in privateFiles" :key="file" :value="file">{{file}}</el-radio>
        </div>
        <template #footer>
        <el-button @click="showSelectDialog=false">Cancel</el-button>
        <el-button @click="sendSelectedFile">Send</el-button>
        </template>
        </el-dialog>
        <!-- Save File Dialog -->
        <el-dialog
v-model="showFileDialog"
title="Save File"
width="300px"
        >
        <el-radio-group v-model="fileType">
        <el-radio value="public">Public</el-radio>
        <el-radio value="private">Private</el-radio>
        </el-radio-group>
        <template #footer>
        <el-button @click="showFileDialog=false">Cancel</el-button>
        <el-button @click="saveFile(fileType)">Save</el-button>
        </template>
        </el-dialog>
        <!-- Upload File Dialog -->
        <el-dialog v-model="showUploadDialog" title="Upload File" width="400px">
        <el-upload ref="uploadRef" class="upload-bar" accept=".txt" @change="handleFileChange" :auto-upload="false"  :limit="1">
   <el-radio-group class="upload-radio-group" v-model="uploadFileType">
           <el-radio value="public">Public</el-radio>
        <el-radio value="private">Private</el-radio>
        </el-radio-group>
   <el-button class="select-file-button">Select File</el-button>
   </el-upload>

        
        <template #footer>
        <el-button @click="showUploadDialog=false">Cancel</el-button>
        <el-button  @click="uploadFile(uploadFileType)">Upload</el-button>
        </template>
        </el-dialog>
    </div>
</template>
<script setup>
import { ref,computed,onMounted,onBeforeUnmount } from 'vue';
import groupStore from '@/stores/group'
import fileStore from '@/stores/file'
import { ElMessage } from 'element-plus'
import { Folder,Notebook,Search,Download,ArrowLeft,Upload } from '@element-plus/icons-vue'
import friendStore from '@/stores/friend'
const FileStore = fileStore()
const username=sessionStorage.getItem('email')
const message=ref('')
const showSelectDialog=ref(false)
const showUploadDialog=ref(false)
const privateFiles=ref([])
const selectedFile=ref('')
const fetch=ref(false)
const file=ref({
    id:0,
    name:'',
    content:''
})
const uploadRef=ref(null)
const uploadFileType=ref('public')
const uploadfile=ref(null)
const handleFileChange=(file,newfile)=>{
  uploadfile.value=newfile[0].raw
  console.log(uploadfile.value)
}
const uploadFile=async(fileType)=>{
   if(uploadfile.value===null){
    ElMessage.error('Please select a file')
    return
   }
    showUploadDialog.value=false
    const formData=new FormData()
    formData.append('file',uploadfile.value)
    formData.append('fileType',fileType)
    const res=await FileStore.uploadFile(formData)
    if(res&&res.code==200){
        fetch.value=true
        ElMessage.success(res.message)
    }
    else{
        ElMessage.error(res.message)
    }
}
const friendfile=ref({
    id:0,
    name:'',
    content:''
})
const refresh=ref(false)
const fileType=ref('public')
const ingroup=ref(true)
const groupstatus=computed(()=>{
    return ingroup.value?'Exit':'Join'
})

const temp=ref(['','',''])
const showMembers=ref(false)
const members=ref([])
const showFileDialog=ref(false)
const FriendStore=friendStore()
const GroupStore = groupStore()
const activeFriend=ref('')
const activeGroup = ref(['','',''])
const activeIndex = ref('/home/messages');
const sendSelectedFile=async()=>{
    const res=await FriendStore.sendSelectedFile({email:activeFriend.value[0],file:selectedFile.value})
    showSelectDialog.value=false
    if(res&&res.code==200){
        getFriendMessages()
    }
    else{
        ElMessage.error(res.message)
    }
}
const sendFriendMessage=async()=>{
    if(message.value.length>500){
        ElMessage.error('Message length cannot exceed 500 words.')
        return
    }
    const res=await FriendStore.sendFriendMessage({email:activeFriend.value[0],message:message.value})
         message.value=''
    if(res&&res.code==200){
        getFriendMessages()
    }
    else{
        ElMessage.error(res.message)
    }
}
const selectFile=async()=>{
    const res=await FriendStore.getAllFiles()
    if(res&&res.code==200){
        privateFiles.value=res.data
    }
    else{
        ElMessage.error(res.message)
    }
    showSelectDialog.value=true
}
const updateFetch = (value) => {
    fetch.value = value
}
const updateRefresh = (value) => {
    refresh.value = value
}
const handleSelect = (key) => {
    activeIndex.value = key;
    if(key=='/home/files'){
        activeGroup.value=['','','']
        activeFriend.value=['','']
    }
    else if(key=='/home/friends'){
        activeGroup.value=['','','']
        activeFile.value=['','']
    }
    else if(key=='/home/groups'){
        activeFriend.value=['','']
        activeFile.value=['','']
    }
}
const activateFriend=(friend)=>{
    activeFriend.value=friend
    getFriendMessages()
}
const activeFile=ref([])
const activateFile=([file,content])=>{
activeFile.value=[file,content]
}
const friendtemp=ref(['',''])
const viewFriendFile=async(id,filename)=>{
    const res=await FriendStore.viewFriendFile({messageId:id})
    if(res){
        friendfile.value={id:id,name:filename,content:res}
        friendtemp.value=activeFriend.value
        activeFriend.value=['','']
    }
    else{
        ElMessage.error(res.message)
    }
}
const getFriendMessages=async()=>{
const res= await FriendStore.getFriendMessages({email:activeFriend.value[0]})
if(res&&res.code==200){
    messages.value=res.data
    for(const m of messages.value){
        if(m[2].includes('send file:')){
            const parts=m[2].split(':')
            if(parts.length>=3 && parts[2].includes('b')){
                m[2]={'file':parts[1]}
            }
        }
    }
}
else{
    ElMessage.error(res.message)
}
}
const activateGroup = (group) => {
    activeGroup.value = group
        getActiveStatus()
        getGroupMessages()
}
const messages = ref([])
const convertDate=(datetime)=>{
    const now=new Date(datetime)
    const year=now.getFullYear()
    const month=now.getMonth()+1
    const day=now.getDate()
    const hour=now.getHours().toString().padStart(2,'0')
    const minute=now.getMinutes().toString().padStart(2,'0')
    const second=now.getSeconds().toString().padStart(2,'0')
    return `${year}-${month}-${day} ${hour}:${minute}:${second}`
}
const getGroupMessages = async () => {
    const res=await GroupStore.getGroupMessages({groupId:activeGroup.value[0]})
    if(res&&res.code==200){
        messages.value = res.data
        for (const m of messages.value){
        const  msg=m[2]
        if (msg.includes('send file:')){
            const parts=msg.split(':')
            if(parts.length>=3 && parts[2].includes('b')){
                m[2]={'file':parts[1]}
            }
        }
    }
    }
    else{
        ElMessage.error(res.message)
    }
}
const sendMessage = async () => {
if (message.value.length>500){
    ElMessage.error('Message length cannot exceed 500 words.')
    return
}
    const res=await GroupStore.sendMessage({groupId:activeGroup.value[0],username:username,message:message.value})
    if(res&&res.code==200){
        message.value=''
        getGroupMessages()
    }
    else{
        ElMessage.error(res.message)
    }
}
const viewMembers = async() => {
    showMembers.value=!showMembers.value
    if(showMembers.value){
    const res=await GroupStore.getGroupMembers({groupId:activeGroup.value[0]})
    if(res&&res.code==200){
        members.value=res.data
    }
    else{
        ElMessage.error(res.message)
    }
    }
}
const getUsers = async() => {
    const res=await GroupStore.getGroupUsers({groupId:activeGroup.value[0]})
    if(res&&res.code==200){
        getGroupMessages()
    }
    else{
        ElMessage.error(res.message)
    }
}
const viewFiles = async() => {
    const res=await GroupStore.getGroupFiles({groupId:activeGroup.value[0]})
    if(res&&res.code==200){
      getGroupMessages()
    }
    else{
        ElMessage.error(res.message)
    }
     
}
const exitGroup = async() => {
    if(ingroup.value){
    const res=await GroupStore.exitGroup({groupId:activeGroup.value[0]})
    if(res && res.code==200){
        getGroupMessages()
        getActiveStatus()
    }
    else{
        ElMessage.error(res.message)
    }}else{
        const res=await GroupStore.intoGroup({groupId:activeGroup.value[0]})
        if(res&&res.code==200){
            getActiveStatus()
            getGroupMessages()
            
        }
        else{
            ElMessage.error(res.message)
        }
    }
}
const getActiveStatus=async()=>{
    const res=await GroupStore.getActiveStatus({groupId:activeGroup.value[0]})
    if(res&&res.code==200){
        ingroup.value=res.data
    }
    else{
        ElMessage.error(res.message)
    }
}
const searchFiles=async()=>{
    const res=await GroupStore.searchFiles({groupId:activeGroup.value[0],filename:message.value})
    message.value=''
    if(res&&res.code==200){
        getGroupMessages()
    }
    else{
        ElMessage.error(res.message)
    }
}
const viewFile = async(id,name) => {
    const res=await GroupStore.viewFile({messageId:id})
    if (res || res==''){
        file.value={id:id,name:name,content:res}
        temp.value= activeGroup.value
        activeGroup.value=['','','']
        console.log("fileres",file)
    }
}
const saveFile=async(fileType)=>{
    showFileDialog.value=false
    let res=''
    if(file.value.name){
  res=await GroupStore.saveFile({fileId:file.value.id,fileType:fileType})}
  else{
    res=await FriendStore.saveFile({fileId:friendfile.value.id,fileType:fileType})
  }
    if(res&&res.code==200){
        ElMessage.success('File saved successfully')
    }
    else{
        ElMessage.error(res.message)
    }
    
}
const returnGroup=()=>{
    if(file.value.name){
    activeGroup.value=temp.value
    file.value={id:0,name:'',content:''}}else if(friendfile.value.name){
        activeFriend.value=friendtemp.value
        friendfile.value={id:0,name:'',content:''}
    }
    else{
        activeFile.value=['','']
    }
}
let ws=null
onMounted(()=>{
ws=new WebSocket("ws://localhost:5000/api/ws")
ws.onopen=()=>{
    console.log("connected")
}
ws.onmessage=(event)=>{
    console.log("data",event.data)
    if(activeGroup.value[0]){
   getGroupMessages()}
   else if(activeFriend.value[0]){
    getFriendMessages()
   }
refresh.value=true
}


ws.onclose=()=>{
    console.log("disconnected")
}
ws.onerror=(event)=>{
    console.log("error",event)
}
})
onBeforeUnmount(()=>{
    ws.close()
    ws=null
})
</script>
<style scoped>
.home-container{
    width: 100%;
    height: 100vh;
    border: 1px solid #e0e0e0;
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
    background-color: #f0f2f5;
    border-radius: 10px;
    overflow: hidden;
    display: flex;
    flex-flow: row wrap;
}
.menu-container{
width:80px;
height:100%;
background-color: rgb(236, 245, 255);
display: flex;
flex-flow: column wrap;
}
.headline-container{
    width:30%;
    height:100%;
    display: flex;
    flex-flow: column wrap;
    background-color: rgb(236, 245, 255);
    border-right:1px solid #e0e0e0;
    overflow: hidden;
}
.content-container,.file-container{
    width:62%;
    height:100%;
    display: flex;
    flex-flow: column wrap;
    overflow: hidden;
    position: relative;
}
.el-menu-vertical{
    width:100%;
    height:93%;
}
.user-info{
    width:100%;
    height:7%;
    display: flex;
    flex-flow: row wrap;
    align-items: center;
    justify-content: center;
}
.user-img{
    width:25px;
    height:25px;
}
.menu-item{
    width:100%;
    height:15%;
    display: flex;
    flex-flow: column wrap;
    align-items: center;
    justify-content: center;
  }
.menu-img{
    width:20px;
    height:20px;
}
.message-header{
    width:100%;
    height:7%;
    display: flex;
    flex-flow: row wrap;
    align-items: center;
    border-bottom:1px solid #e0e0e0;
}
.message-content{
    width:100%;
    height:82%;
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
}
.message-item-container{
    height:10%;
    display: flex;
    flex-flow: row wrap;
    align-items: center;
    margin:3px;
}
.item-content{
    border:1px solid #e0e0e0;
    border-radius: 4px;
    background-color: rgb(236, 245, 255);
    padding:4px;
    min-width:10px;
    min-height:20px;
    font-size:15px;
    margin:0 5px;
}
.item-content-self{
    border:1px solid #e0e0e0;
    border-radius: 4px;
    background-color: rgba(143, 198, 255,0.7);
    padding:4px;
    font-size:15px;
    margin:0 5px;
     min-width:10px;
    min-height:20px;

}
.item-package{
    width:200px;
    height:40px;
    display:flex;
    flex-flow: row wrap;
  border:1px solid #e0e0e0;
    background-color: white;
    border-radius:3px;
    align-items: center;
    font-size:15px;
    padding:3px;
    margin:0 5px;
    }
.item-sender{
    font-size: 15px;
}
.item-datetime{
    font-size: 12px;
    color:rgba(0,0,0,0.6);
}
.send-message-container{
    width:95%;
    position: absolute;
    bottom:0;
border:1px solid #e0e0e0;
border-radius: 4px;
padding:10px;
margin:4px;
}
.message-input{
    border:none;
    background-color: transparent;
}
.send-button{
    width:10%;
}
.user-img{
    width:15px;
    height:15px;
}
.group-name-container,.friend-name-container{
    width:80%;
    height:100%;
    display: flex;
    flex-flow: row wrap;
    align-items: center;
}
.group-buttons{
    width:20%;
    height:100%;
    display: flex;
    flex-flow: row wrap;
    align-items: center;
}
.members-container{
    width:30%;
    height:78%;
    display: flex;
    flex-flow: column wrap;
    position: absolute;
    right:0;
    top:7%;
    border:1px solid #e0e0e0;
    border-radius: 4px;
    padding:10px;
    background-color: rgb(236, 245, 255);

}
.member-name{
    font-size: 14px;
    margin:2px;
    color:rgba(0,0,0,0.5)
}
.file-img{
    width:25px;
    height: 25px;
}
.file-header{
    width:100%;
    height:7%;
    border-bottom:1px solid #e0e0e0;
    display:flex;
    flex-flow:row nowrap;
    align-items: center;
}
.file-content{
    width:100%;
    height:90%;
    padding:10px;
    overflow-y: auto;
    overflow-x: hidden;
    background-color: white;

}
.public-folder,.private-folder{
    width:100%;
    height:50%;
    display:flex;
    flex-flow:column wrap;
    border-bottom:1px solid #e0e0e0;
}
.file-radio{
    margin:5px;
    font-size:15px;
    color:rgba(0,0,0,0.85);
    font-family: Arial, Helvetica, sans-serif;
}
.upload-bar{
    width:100%;
    height:100%;
    display:flex;
    flex-flow:column wrap;
}
.el-radio-group{
    width:60%;
}
.select-file-button{
    width:30%;
   margin:10px;
}
</style>