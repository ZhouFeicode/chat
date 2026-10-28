import { defineStore } from 'pinia'
import axios from 'axios'
const friendStore=('friendStore',()=>{
    const logout=async({email})=>{
        const res=await axios.post('http://localhost:5000/api/group/logout',{email:email})
        return res.data
    }
    const getFriends=async({email})=>{
        const res=await axios.get(`http://localhost:5000/api/friend/list`,{params:{email:email}})
        return res.data
    }
    const getRequests=async({email})=>{
        const res=await axios.get(`http://localhost:5000/api/friend/requests`,{params:{email:email}})
        return res.data
    }
    const acceptRequest=async({email,request})=>{
        const res=await axios.post(`http://localhost:5000/api/friend/accept`,{email:email,request:request})
        return res.data
    }
    const getFriendMessages=async({email})=>{
        const res=await axios.get(`http://localhost:5000/api/friend/messages`,{params:{email:email}})
        return res.data
    }
    const getAllFiles=async()=>{
        const res=await axios.get(`http://localhost:5000/api/file/all`)
        return res.data
    }
    const sendSelectedFile=async({email,file})=>{
        const res=await axios.post(`http://localhost:5000/api/file/send`,{email:email,file:file})
        return res.data
    }
    const sendFriendMessage=async({email,message})=>{
        const res=await axios.post(`http://localhost:5000/api/friend/message`,{email:email,message:message})
        return res.data
    }
    const viewFriendFile=async({messageId})=>{
        const res=await axios.get(`http://localhost:5000/api/file/view`,{params:{messageId:messageId}})
        return res.data
    }
    const saveFile=async({fileId,fileType})=>{
        const res=await axios.post(`http://localhost:5000/api/friend/saveFile`,{fileId:fileId,fileType:fileType})
        return res.data
    }
    return{logout,getFriends,getRequests,acceptRequest,getFriendMessages,getAllFiles,sendSelectedFile,sendFriendMessage,viewFriendFile,saveFile}
})
export default friendStore
