<template>
    <div class="groups-container">
    <div class="headline-header">
        <div class="email-info">
        <el-tooltip content="Click to log out" placement="top">
        <span class="user-name" @click="logout">{{email}}</span>
        </el-tooltip>
        <div class="add-icon-container">
        <img src="@/assets/add.png"  class="add-icon" @click="showAddBar=!showAddBar">
        </div>
         </div>
         <div class="add-bar-container" v-if="showAddBar">
        <div class="add-bar">
        <span class="add-bar-item" @click=createGroup>Create Group</span>
        <span class="add-bar-item" @click=joinGroup>Join Group</span>
        <span class="add-bar-item" @click=addFriend>Add Friend</span>
        </div>
         </div>
         </div>
          <el-dialog
        v-model="showDialog"
        :title="dialogTitle"
        width="40%"
        >
        <el-form ref="formRef" :model="form" :rules="rules">
        <el-form-item prop="name">
        <el-input v-model="form.name" placeholder="group/user name" />
        </el-form-item>
        </el-form>
        <template #footer>
        <el-button @click="showDialog = false">Cancel</el-button>
        <el-button type="primary" @click="handleSubmit">Submit</el-button>
        </template>
        </el-dialog>
       <div class="groups-list">
       <div class="group-item" v-for="group in groups" :key="group[0]">
       <span @click="emit('activateGroup',group)" class="group-name">{{group[2]}}:{{group[1]}}</span>
       </div>
       </div>
    </div>
</template>
<script setup>
import { ref } from 'vue'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const email = ref(sessionStorage.getItem('email'))
import { ElMessage } from 'element-plus'
import groupStore from '@/stores/group'
const groups = ref([])
const GroupStore = groupStore()
const showAddBar = ref(false)
const showDialog = ref(false)
const dialogTitle = ref('')
const form = ref({
    name:''
})
const emit = defineEmits(['activateGroup'])
const rules = ref({
    name:[{required:true,message:'Please input group/user name',trigger:'blur'}]
})
const formRef = ref(null)
const createGroup = () => {
    dialogTitle.value = 'Create Group'
    showDialog.value = true
    showAddBar.value = false
}
const joinGroup = () => {
    dialogTitle.value = 'Join Group'
    showDialog.value = true
    showAddBar.value = false
}
const addFriend = () => {
    dialogTitle.value = 'Add Friend'
    showDialog.value = true
    showAddBar.value = false
}
const handleSubmit =async () => {
    formRef.value.validate((valid) => {
        if(!valid){
            return false
        }
    })
    if (dialogTitle.value == 'Create Group'){
        const res = await GroupStore.createGroup({email:email.value,name:form.value.name})
        if(res&&res.code==200){
            ElMessage.success(res.message)
            showDialog.value = false
            getGroups()
            }
            else{
                ElMessage.error(res.message)
            } 
        }else if(dialogTitle.value == 'Join Group'){
            const res=await GroupStore.joinGroup({email:email.value,name:form.value.name})
            if(res&&res.code==200){
                ElMessage.success(res.message)
                showDialog.value = false
                getGroups()
            }
            else{
                ElMessage.error(res.message)
            }
        }else{
            const res=await GroupStore.addFriend({email:email.value,name:form.value.name})
            if(res&&res.code==200){
                ElMessage.success(res.message)
                showDialog.value = false
                getGroups()
            }
            else{
                ElMessage.error(res.message)
            }
        }
}
const logout = async() => {
    const res=await GroupStore.logout({email:email.value})
    if(res&&res.code==200){
        ElMessage.success(res.message)
    }
    else{
        ElMessage.error(res.message)
    }
    sessionStorage.removeItem('email')
    router.push('/login')
}
const getGroups = async () => {
    const res = await GroupStore.getGroups({email:email.value}) 
    if(res&&res.code==200){
    groups.value = res.data}
    else{
        ElMessage.error(res.message)
    }
}

onMounted(()=>{
    getGroups()
})

</script>
<style scoped>
.groups-container{
    width:100%;
    height:100%;
}
.groups-list{
    width:100%;
    height:90%;
    display:flex;
    flex-direction: column;
}
.group-item{
    width:100%;
    height:40px;
    display:flex;
    align-items: center;
    justify-content: left;
    padding:0 10px;
    border-bottom:1px solid #e0e0e0;
    cursor: pointer;
}
.group-name{
    font-size:16px;
    color:rgb(0,0,0,0.7);
}
</style>