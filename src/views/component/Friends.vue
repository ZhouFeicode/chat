<template>
    <div class="friends-container">
        <div class="user-info">
        <span class="user-name">{{email}}</span>
        <img src="@/assets/add.png"  class="add-icon" @click="addFriend">
        </div>
        <h1>friend</h1>
        <div class="friends-list">
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue'
const email = ref(sessionStorage.getItem('email'))
const addFriend = () => {
    console.log('addFriend')
}
</script>
<style scoped>
.friends-container{
    width:100%;
    height:100%;
}
</style>