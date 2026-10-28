<template>
    <div class="friends-container">
    <div class="headline-header">
        <div class="email-info">
        <el-tooltip content="Click to log out" placement="top">
        <span class="user-name" @click="logout">{{email}}</span>
        </el-tooltip>
        </div>
    </div>
    <div class="friends-list">
    <div @click="emit('activateFriend',friend)" class="friend-item" v-for="friend in friends" :key="friend[0]">
    <span class="list-item">{{friend[0]}}</span>
    <span class="list-item-status">{{friend[1]}}</span>
    </div>
    </div>
    <div class="request-list">
    <div class="request-item" v-for="request in requests" :key="request[0]">
    <span  class="list-item">{{request}}</span>
    <el-button type="primary" @click="acceptRequest(request)">Accept</el-button>
    </div>
    </div>
    </div>
</template>
<script setup>
import { ref,onMounted,watch } from 'vue'
import { useRouter } from 'vue-router'
import friendStore from '@/stores/friend'
import {ElMessage} from 'element-plus'
const emit=defineEmits(['activateFriend','updateRefresh'])
const FriendStore = friendStore()
const router=useRouter()
const email = ref(sessionStorage.getItem('email'))
const logout = async() => {
    const res=await FriendStore.logout({email:email.value})
    if(res.code==200){
    sessionStorage.removeItem('email')
    router.push('/login')
    }
    else{
        ElMessage.error(res.message)
    }
}
const friends=ref([])
const requests=ref([])
const getFriends=async()=>{
    const res=await FriendStore.getFriends({email:email.value})
    if(res.code==200){
        friends.value=res.data
        console.log("friends",friends.value)
    }
    else{
        ElMessage.error(res.message)
    }
}
const getRequests=async()=>{
    const res=await FriendStore.getRequests({email:email.value})
    if(res.code==200){
        requests.value=res.data
        console.log("requests",requests.value)
    }
    else{
        ElMessage.error(res.message)
    }
}
const acceptRequest=async(request)=>{
    const res=await FriendStore.acceptRequest({email:email.value,request:request})
    if(res.code==200){
        ElMessage.success(res.message)
        await getRequests()
        await getFriends()
    }
    else{
        ElMessage.error(res.message)
    }   
}
const props=defineProps(['refresh'])
watch(()=>props.refresh,(newVal)=>{
    if(newVal){
         getFriends()
         getRequests()
        emit('updateRefresh',false)
    }
})
onMounted(async()=>{
    await getFriends()
    await getRequests()
})
</script>
<style scoped>
.friends-container{
    width:100%;
    height:100%;
}
.friends-list{
    width:100%;
    height:70%;
border-bottom:1px solid #e0e0e0;
}
.request-list{
    width:100%;
    height:30%;
}
.friend-item{
    width:100%;
    height: 5%;
    padding:5px;
    border-bottom:1px solid #e0e0e0;
    display: flex;
    flex-flow: row nowrap;
    cursor:pointer;
}
.request-item{
    width:100%;
    height: 12%;
    padding:5px;
    border-bottom:1px solid #e0e0e0;
    display: flex;
    flex-flow: row nowrap;
}

.list-item{
 font-size:15px;
 color:rgba(0,0,0,0.7);
 width:70%;
}
.list-item-status{
    font-size:15px;
    color:blue;
}
</style>