import Vue from 'vue'
import VueRouter from 'vue-router'
import Hello from '../components/Hello.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Recover from '../components/Recover.vue'
import Home from '../components/Home.vue'
import User from '../components/User.vue'
import Client from '../components/Client.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/hello'
  },
  {
    path: '/hello',
    redirect: '/hello/login',
    name: 'Hello',
    component: Hello,
    children: [
      {
        path: '/hello/login',
        name: 'Login',
        component: Login
      },
      {
        path: '/hello/register',
        name: 'Register',
        component: Register
      },
      {
        path: '/hello/recover',
        name: 'Recover',
        component: Recover
      }
    ]
  },
  {
    path: '/home',
    redirect: '/home/user',
    name: 'Home',
    component: Home,
    children: [
      {
        path: '/home/user',
        name: 'User',
        component: User
      },
      {
        path: '/home/client',
        name: 'Client',
        component: Client
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
