<template>
    <div class="messages-container">
           <div class="headline-header">
        <div class="email-info">
        <el-tooltip content="Click to log out" placement="top">
        <span class="user-name" @click="logout">{{email}}</span>
        </el-tooltip>
        </div>
    </div>
    <div class="public-list">
    <span class="list-item-label">Public Files:</span>
    <div class="list-item">
    <span @click="activateFile(file,'public')" v-for="file in publicFiles" :key="file" class="list-item-content">{{file}}</span>
    </div>
    </div>
    <div class="private-list">
    <span class="list-item-label">Private Files:</span>
    <div class="list-item">
    <span @click="activateFile(file,'private')" v-for="file in privateFiles" :key="file" class="list-item-content">{{file}}</span>
    </div>
    </div>
    </div>
</template>
<script setup>
import { ref,onMounted,defineEmits,watch,defineProps } from 'vue' 
import fileStore from '@/stores/file'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
const router=useRouter()
const FileStore = fileStore()
const email = ref(sessionStorage.getItem('email'))
const emit=defineEmits(['activateFile','updateFetch'])
const publicFiles = ref([])
const privateFiles = ref([])
const activateFile =async (file,fileType) => {
    const res=await FileStore.getFileContent(file,fileType)
    if(res || res===''){
        emit('activateFile',[file,res])
    }
    else{
        ElMessage.error(res.message)
    }
  
}
const getFiles=async()=>{
    const res=await FileStore.getFiles()
    if(res.code==200){
        publicFiles.value = res.data.publicFiles
        privateFiles.value = res.data.privateFiles
        console.log(res)
    }
    else{
        ElMessage.error(res.message)
    }
}
const props=defineProps(['fetch'])
const logout=async()=>{
    const res=await FileStore.logout({email:email.value})
    if(res){
        router.push('/login')
        ElMessage.success('Logged out successfully')
    }
    else{
        ElMessage.error(res.message)
    }
}
watch(()=>props.fetch,()=>{
    if(props.fetch){
        getFiles()
        emit('updateFetch',false)
    }
})
onMounted(()=>{
    getFiles()
})
</script>
<style scoped>
.messages-container{
    width:100%;
    height:100%;
}
.public-list{
    width:100%;
    height:50%;
    border-bottom: 1px solid #e0e0e0;
}
.private-list{
    width:100%;
    height:40%;
}
.list-item-label{
    font-size: 16px;
    color: rgba(0,0,0,0.75);
}
.list-item{

    display: flex;
    flex-flow: column wrap;
    width: 100%;
height: 100%;
overflow-y:auto ;
overflow-x:hidden;
}
.list-item-content{
    font-size: 14px;
    color: rgba(0,0,0,0.8);
    cursor: pointer;
    margin: 2px;
    height:7%;
    width:100%;
    border-bottom: 1px solid #e0e0e0;
}
</style>