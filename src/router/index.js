import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/auth/Login.vue'
import SetPassword from '@/views/auth/SetPassword.vue'
import AccountLogin from '@/views/auth/AccountLogin.vue'
import Home from '@/views/pages/Home.vue'
import Messages from '@/views/component/Messages.vue'
import Friends from '@/views/component/Friends.vue'
import Groups from '@/views/component/Groups.vue'
const routes = [
  {
    path:'/',
    redirect:'/login'
  },
  {
  path:'/login',
  component:Login
},
{
  path:'/set-password',
  name:'set-password',
  component:SetPassword
},
{
  path:'/account-login',
  name:'account-login',
  component:AccountLogin
},
{
  path:'/home',
  name:'home',
  component:Home,
  children:[
    {
      path:'messages',
      name:'messages',
      component:Messages
    },
    {
      path:'friends',
      name:'friends',
      component:Friends
    },
    {
      path:'groups',
      name:'groups',
      component:Groups
    }
  ]
}
]
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

export default router
