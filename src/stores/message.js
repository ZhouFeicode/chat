import { defineStore } from 'pinia'
import axios from 'axios'
const messageStore = defineStore('messageStore',()=> {
    const getGroups = async () => {
        const res = await axios.get('http://localhost:5000/api/getGroups')
        return res.data
    }
    const getFriends = async () => {
        const res = await axios.get('http://localhost:5000/api/getFriends')
        return res.data
    }
    return {getGroups,getFriends}
})
export default messageStore