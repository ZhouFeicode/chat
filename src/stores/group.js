import { defineStore } from 'pinia'
import axios from 'axios'
const groupStore = defineStore('groupStore',()=> {
    const getGroups = async (email) => {
        const res = await axios.get(`http://localhost:5000/api/group/list`,{params:email})
        return res.data
    }
    const createGroup = async ({email,name}) => {
        const res = await axios.post(`http://localhost:5000/api/group/create`,{email:email,name:name})
        return res.data
    }
    const joinGroup = async ({email,name}) => {
        const res = await axios.post(`http://localhost:5000/api/group/join`,{email:email,name:name})
        return res.data
    }
    const addFriend = async ({email,name}) => {
        const res = await axios.post(`http://localhost:5000/api/group/add`,{email:email,name:name})
        return res.data
    }
    const logout = async ({email}) => {
        const res = await axios.post(`http://localhost:5000/api/group/logout`,{email:email})
        return res.data
    }
    const getGroupMessages = async ({groupId}) => {
        const res = await axios.get(`http://localhost:5000/api/group/messages`,{params:{groupId:groupId}})
        return res.data
    }
    const sendMessage = async ({groupId,username,message}) => {
        const res = await axios.post(`http://localhost:5000/api/group/sendMessage`,{groupId:groupId,username:username,message:message})
        return res.data
    }
    const getGroupFiles = async ({groupId}) => {
        const res = await axios.get(`http://localhost:5000/api/group/files`,{params:{groupId:groupId}})
        return res.data
    }
    const getGroupUsers=async({groupId}) => {
        const res = await axios.get(`http://localhost:5000/api/group/users`,{params:{groupId:groupId}})
        return res.data
    }
    const getGroupMembers=async({groupId}) => {
        const res = await axios.get(`http://localhost:5000/api/group/members`,{params:{groupId:groupId}})
        return res.data
    }
    const exitGroup=async({groupId}) => {
        const res = await axios.post(`http://localhost:5000/api/group/exit`,{groupId:groupId})
        return res.data
    }
    const intoGroup=async({groupId}) => {
        const res = await axios.post(`http://localhost:5000/api/group/into`,{groupId:groupId})
        return res.data
    }
    const getActiveStatus=async({groupId})=>{
        const res=await axios.get(`http://localhost:5000/api/group/activeStatus`,{params:{groupId:groupId}})
        return res.data
    }
    const searchFiles=async({groupId,filename})=>{
        const res=await axios.get(`http://localhost:5000/api/group/searchFiles`,{params:{groupId:groupId,filename:filename}})
        return res.data
    }
    const viewFile=async({messageId})=>{
        const res=await axios.get(`http://localhost:5000/api/group/viewFile`,{params:{messageId:messageId}},{responseType:'blob'})
        return res.data
    }
    const saveFile=async({fileId,fileType})=>{
        const res=await axios.get(`http://localhost:5000/api/group/saveFile`,{fileId:fileId,fileType:fileType })
        return res.data
    }
    return {getGroups,createGroup,joinGroup,addFriend,logout,getGroupMessages,sendMessage,getGroupFiles,getGroupUsers,getGroupMembers,exitGroup,intoGroup,getActiveStatus,searchFiles,viewFile,saveFile}
})
export default groupStore