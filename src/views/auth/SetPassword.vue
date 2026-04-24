<template>
<div class="login-container">
<div class="left-container">
<img clas="left-img" src="@/assets/chat.png">
<h1>Your Chat System</h1>
</div>
<div class="right-container">
<h2>Welcome to Log in/Sign up</h2>
<el-form class="form-container" ref="formRef" :model="form" :rules="rules" label-width="100px">
<el-form-item class="form-item" prop="password">
    <el-input type="password" v-model="form.password" placeholder="Password"></el-input>
</el-form-item>
<el-form-item class="form-item"  prop="password2">
    <el-input type="password"  v-model="form.password2" placeholder="Confirm Password">
    </el-input>
</el-form-item>
<el-form-item class="form-item">
<el-button class="submit-button" @click="setpassword">Set Password</el-button>
<div class="account-login">
<router-link class="login-text" to="/account-login">Log in with account</router-link>
</div>
</el-form-item>
</el-form>
</div>
</div>
</template>
<script setup>
import { ref } from 'vue';
import LoginStore from '@/stores/login';
import { ElMessage } from 'element-plus';
import { useRoute } from 'vue-router';
import emitter from '@/utils/mitt';
import { onMounted,onBeforeUnmount } from 'vue';
const route=useRoute();
const loginStore=LoginStore();
const formRef = ref(null);
const form=ref({
  password:'',
  password2:''
})
const rules={
    password:[{required:true,message:'Please input password',trigger:'blur'}],
    password2:[{required:true,message:'Please input confirm password',trigger:'blur'}],
}

const setpassword=async()=>{
  formRef.value.validate((valid)=>{
    if(!valid){
        ElMessage.error('Please input valid password');
        return false;
    }
  })
   if(form.value.password!==form.value.password2){
    ElMessage.error('Password and confirm password do not match');
    return false;
   }
   if(!route.query.email){
    ElMessage.error('Email is required');
    return false;
   }
    try{
const res=await loginStore.setPassword(route.query.email,form.value.password);
if(res.code===200){
    ElMessage.success('Setting password successfully!');
}
else{
    ElMessage.error('Setting password failed');
}
    }catch(error){
        console.error(error);
    }
}

</script>

<style scoped>
.login-container{
    font-family: 'Arial', sans-serif;
}
.account-login,.account-login2{
    width:100%;
    height:20px;
    margin-top:10px;
}
.account-login2{
    display: flex;
    justify-content: center;
}
.form-item{
    width:60%;
height:40px;
border-radius:5px;
margin-left:-10%;
}
.submit-button{
    width:100%;
    height:40px;
    border-radius:5px;
    background-color: rgb(64, 158, 255);
    color: white;
}
.login-container{
width: 100%;
height:100vh;
display: flex;
flex-flow: row wrap;
border-radius:10px;
box-shadow: 2px 2px 10px 0 rgba(0,0,0,0.2);
overflow: hidden;
}
.left-container{
    width: 50%;
    height: 100%;
   background-color: rgb(230, 238, 255);
   display: flex;
   flex-flow: column wrap;
   align-items: center;
   justify-content: center;
}
.left-img{
    width:80px;
    height: 80px;
}
.right-container{
width:50%;
height:100%;
display: flex;
flex-flow: column wrap;
align-items: center;
justify-content: center;
}
.form-container{
    width:100%;
    height:70%;
    display: flex;
    flex-flow: column wrap;
    align-items: center;
    margin-top:20px;
}
.login-text,.login-text2{
    font-size:14px;
    color:rgb(155, 155, 155);
    text-decoration: none;
}
.login-text:hover{
    color:rgb(64, 158, 255);
}
</style>