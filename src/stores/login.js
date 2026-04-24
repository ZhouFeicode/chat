import axios from 'axios';
import { defineStore } from 'pinia';
const loginStore = defineStore('loginStore',()=> {
const sendCode=async(email)=>{
    try{
        const res=await axios.post('http://localhost:5000/api/sendCode',{email:email});
        return res.data;
    }catch(error){
        console.error(error);
    }
}
const login=async(email,code)=>{
    try{
        const res=await axios.post('http://localhost:5000/api/login',{email:email,code:code});
        return res.data;
    }catch(error){
        console.error(error);
    }
}
const setPassword=async(email,password)=>{
    try{
        const res=await axios.post('http://localhost:5000/api/setPassword',{email:email,password:password});
        return res.data;
    }catch(error){
        console.error(error);
    }
}
const accountLogin=async(email,password)=>{
    try{
        const res=await axios.post('http://localhost:5000/api/accountLogin',{email:email,password:password});
        return res.data;
    }catch(error){
        console.error(error);
    }
}
return {login,sendCode,setPassword,accountLogin};
})
export default loginStore;