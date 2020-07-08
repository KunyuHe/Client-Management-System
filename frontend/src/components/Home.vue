<template>
<a-layout id="home">
  <a-layout-sider v-model="collapsed" :trigger="null" collapsible>
    <div class="logo">
      <img src="../assets/logo_min.png" width="40px" alt="">
      <h1 v-if="!collapsed">CMS</h1>
    </div>

    <a-menu theme="dark" mode="inline" :selectedKeys="activePath" :default-selected-keys="activePath">
      <a-menu-item v-for="item in userMenus" :key="item.index" @click="saveIndex(item.index)">
        <a-icon :type="item.icon" />
        <span>{{item.title}}</span>
        <router-link :to="{path:item.url}" />
      </a-menu-item>
    </a-menu>
  </a-layout-sider>

  <a-layout>
    <a-layout-header style="background: #fff; padding: 0 15px 0 0; display:flex; justify-content: space-between; align-items: center;">
      <a-icon class="trigger" :type="collapsed ? 'menu-unfold' : 'menu-fold'" @click="() => (collapsed = !collapsed)" />

      <a-dropdown placement="bottomCenter">
        <span style="margin-right:24px">
          <a-avatar shape="square" icon="user" :style="{backgroundColor: '#00245D'}" />
        </span>

        <a-menu slot="overlay">
          <a-menu-item>
            <router-link @click="saveIndex(1)" :to="{path:'/home/user'}">
              用户中心
            </router-link>
          </a-menu-item>
          <a-menu-item>
            <a href="#remind" @click="openNotification()">
              交易需求提醒
            </a>
          </a-menu-item>
          <a-menu-item>
            <a @click="logout">
              退出登录
            </a>
          </a-menu-item>
        </a-menu>
      </a-dropdown>

    </a-layout-header>
    <a-layout-content>
      <router-view />
    </a-layout-content>
  </a-layout>
</a-layout>
</template>

<script>
import {
  userInfo
} from '../api/api'

const activePath = ['1']

export default {
  data () {
    return {
      collapsed: false,
      activePath,
      currMenu: '',
      userMenus: [{
        index: 1,
        icon: 'user',
        url: '/home/user',
        title: '用户中心'
      },
      {
        index: 2,
        icon: 'usergroup-delete',
        url: '/home/client',
        title: '客户管理'
      }
      ],
      notification: null,
      currUser: null
    }
  },

  watch: {
    currUser: {
      handler (newVal, oldVal) {
        this.$socket.emit('join', {
          user: this.currUser
        })
      },
      deep: true
    }
  },

  created () {
    this.findUser()
  },

  mounted () {
    const index = window.sessionStorage.getItem('index')
    this.saveIndex(index)
    this.$socket.emit('hi', {
      subscribe: true
    })
  },

  sockets: { // 通过vue实例对象sockets实现组件中的事件监听
    connect () { // socket的connect事件
    },

    hi (data) { // 后端按主题名推送的消息数据
      this.notification = data
      this.openNotification()
    }
  },

  methods: {
    findUser () {
      userInfo()
        .then((res) => {
          if (res.data.code === 0) {
            this.currUser = res.data.data
          } else {
            return this.$message.error(res.data.msg)
          }
        })
        .catch(err => {
          console.log(err)
        })
    },

    saveIndex (index) {
      window.sessionStorage.setItem('index', index)
      this.activePath = []
      this.activePath.push(index)
    },

    logout () {
      window.sessionStorage.clear()
      this.$router.push('/hello/login')
    },

    openNotification () {
      if (this.notification !== null) {
        this.$notification.info({
          message: '交易需求提醒',
          description: this.notification,
          style: {
            border: '3px solid lightblue'
          },
          duration: 0
        })
      } else {
        this.$notification.warning({
          message: '暂无新的交易需求！',
          duration: 3
        })
        this.notification = null
      }
    }
  },
  destroyed () {
    this.$socket.emit('leave', {
      user: this.currUser
    })
    this.$socket.emit('disconnect')
  }
}
</script>

<style lang="less" scoped>
#home {
    text-align: left;
    .trigger {
        font-size: 18px;
        line-height: 64px;
        padding: 0 24px;
        cursor: pointer;
        transition: color 0.3s;
    }
    .trigger:hover {
        color: #1890ff;
    }
    .logo {
        height: 32px;
        margin: 14px;
        h1 {
            display: inline;
            color: #fff;
            font-size: 20px;
            margin: 0 0 0 12px;
            font-family: Avenir,Helvetica Neue,Arial,Helvetica,sans-serif;
            font-weight: 600;
            vertical-align: middle;
        }
    }
}
.ant-layout {
    height: 100%;
}
.ant-layout-content {
    height: 100%;
}
</style>
