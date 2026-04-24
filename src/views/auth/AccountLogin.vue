<template>
<div class="login-container">
<div class="left-container">
<img clas="left-img" src="@/assets/chat.png">
<h1>Your Chat System</h1>
</div>
<div class="right-container">
<h2>Welcome to Log in</h2>
<el-form class="form-container" ref="formRef" :model="form" :rules="rules" label-width="100px">
<el-form-item class="form-item" prop="email">
    <el-input type="email" v-model="form.email" placeholder="Email"></el-input>
</el-form-item>
<el-form-item class="form-item"  prop="password">
    <el-input type="password" v-model="form.password" placeholder="Password"></el-input>
</el-form-item>
<el-form-item class="form-item">
<el-button class="submit-button" @click="submitForm">Log in</el-button>
<div class="login">
<router-link class="login-text" to="/login">Log in with verification code</router-link>
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
    password:'',
})
const rules={
    email:[{required:true,type:'email',message:'Please input email',trigger:'blur'}],
    password:[{required:true,message:'Please input password',trigger:'blur'}],
}
const submitForm=async()=>{
  formRef.value.validate((valid)=>{
    if(!valid){
        ElMessage.error('Please input valid email');
        return false;
    }
  })

    try{
const res=await loginStore.accountLogin(form.value.email,form.value.password);
if(res&&res.code===200){
    ElMessage.success('Login successfully!');
    sessionStorage.setItem('email',res.data.email);
    router.push('/home');
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
.login{
    width:100%;
    height:20px;
    margin-top:10px;
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