import { defineStore } from 'pinia'
import axios from 'axios'
const fileStore = defineStore('fileStore',()=> {
    const getFiles = async () => {
        const res = await axios.get('http://localhost:5000/api/files')
        return res.data
    }
    const uploadFile = async (formData) => {
        const res = await axios.post('http://localhost:5000/api/file/upload',formData)
        return res.data
    }
    const getFileContent = async (file,fileType) => {
        const res = await axios.get(`http://localhost:5000/api/file/content`,{params:{file:file,fileType:fileType}})
        return res.data
    }
    const logout=async({email})=>{
        const res=await axios.post('http://localhost:5000/api/group/logout',{email:email})
        return res.data
    }
    return {getFiles,uploadFile,getFileContent,logout}
})
export default fileStore