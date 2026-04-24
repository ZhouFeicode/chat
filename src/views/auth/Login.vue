<template>
<div class="login-container">
<div class="left-container">
<img clas="left-img" src="@/assets/chat.png">
<h1>Your Chat System</h1>
</div>
<div class="right-container">
<h2>Welcome to Log in/Sign up</h2>
<el-form class="form-container" ref="formRef" :model="form" :rules="rules" label-width="100px">
<el-form-item class="form-item" prop="email">
    <el-input v-model="form.email" placeholder="Email"></el-input>
</el-form-item>
<el-form-item class="form-item"  prop="code">
    <el-input v-model="form.code" placeholder="Code">
    <template #append>
    <el-button :disabled="isSending" class="send-button" @click="sendCode">{{sender}}</el-button>
    </template>
    </el-input>
</el-form-item>
<el-form-item class="form-item">
<el-button class="submit-button" @click="submitForm">Log in/Sign up</el-button>
<div class="account-login">
<router-link class="login-text" to="/account-login">Log in with account</router-link>
</div>
<div class="account-login2">
<p class="login-text2">If no account, automatically create an account</p>
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
import { useRouter } from 'vue-router';
import emitter from '@/utils/mitt';
const router=useRouter();
const loginStore=LoginStore();
const formRef = ref(null);
const sender=ref('Send Code');
const form=ref({
    email:'',
    code:'',
})
const isSending=ref(false);
const validateCode=()=>{
    if( !/^\d{6,6}$/.test(form.value.code)){
       return false;
    }else{
        return true;
    }
}
const rules={
    email:[{required:true,type:'email',message:'Please input email',trigger:'blur'}],
}
let second=0;
let timer=null;
const sendCode=async()=>{
   formRef.value.validate((valid)=>{
    if(!valid){
        ElMessage.error('Please input valid email');
        return false;
    }
   })
   
    isSending.value=true;
    second=60;
    sender.value=second+"s later send code";
    timer=setInterval(()=>{
        if(second>0){
            second--;
            sender.value=second+"s later send code";
        }else{
            sender.value='Send Code';
            isSending.value=false;
            clearInterval(timer);
            timer=null;
        }
    },1000)
    const res=await loginStore.sendCode(form.value.email);
    console.log("res",res);
    if(res.code===200){
        ElMessage.success('Code sent successfully');
    }else{
        ElMessage.error('Code sending failed');
    }
}
const submitForm=async()=>{
  formRef.value.validate((valid)=>{
    if(!valid){
        ElMessage.error('Please input valid email');
        return false;
    }
  })
    if(!validateCode()){
        ElMessage.error('Please input valid code');
        return false;
    }
    try{
const res=await loginStore.login(form.value.email,form.value.code);
if(res&&res.code===200){
    ElMessage.success('Login successfully!');
    sessionStorage.setItem('email',res.data.email);
    router.push('/home');
}
else if(res&&res.code===201){
    ElMessage.success('Sign up successfully, please set password');
    router.push({path:'/set-password',query:{email:res.data.email}})
}
else{
    ElMessage.error('Login failed'+res?.message);
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