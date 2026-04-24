<template>
    <div class="messages-container">
        <div class="user-info">
        <span class="user-name">{{email}}</span>
          <img src="@/assets/add.png"  class="add-icon" @click="addMessage">
        </div>
        <div class="messages-list">

        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue' 
const email = ref(sessionStorage.getItem('email'))
    const addMessage = () => {
    console.log('addMessage')
}
</script>
<style scoped>
.messages-container{
    width:100%;
    height:100%;
}

</style>