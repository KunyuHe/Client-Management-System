<template>
  <a-layout id="home">
    <a-layout-sider v-model="collapsed" :trigger="null" collapsible>
      <div class="logo">
        <img src="../assets/logo_min.png" width="55px" alt="">
        <h1 v-if="!collapsed">System</h1>
      </div>
      <a-menu theme="dark" mode="inline" :selectedKeys="activePath" :default-selected-keys="activePath">
        <a-menu-item v-for="item in userMenus" :key="item.index" @click="saveIndex(item.index)">
          <a-icon :type="item.icon" />
          <span>{{item.title}}</span>
          <router-link :to="{path:item.url}"/>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header style="background: #fff; padding: 0 15px 0 0; display:flex; justify-content: space-between; align-items: center;" >
        <a-icon
          class="trigger"
          :type="collapsed ? 'menu-unfold' : 'menu-fold'"
          @click="() => (collapsed = !collapsed)"
        />
        <a-dropdown placement="bottomCenter">
          <span style="margin-right:24px">
            <a-badge :count="remindCount"><a-avatar shape="square" icon="user"/></a-badge>
          </span>
          <a-menu slot="overlay">
            <a-menu-item>
              <router-link @click="saveIndex (1)" :to="{path:'/home/user'}">
                个人信息
              </router-link>
            </a-menu-item>
            <a-menu-item>
              <a-badge :dot="isHave"><a href="#remind" @click="openNotification(), isHave = false">提醒</a></a-badge>
            </a-menu-item>
            <a-menu-item>
              <a  @click="logout">注销</a>
            </a-menu-item>
          </a-menu>
        </a-dropdown>
      </a-layout-header>
      <a-layout-content>
      <router-view v-on:listenToHome="listenFromUser"/>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>
<script>
const activePath = ['1']
export default {
  data () {
    return {
      remindCount: 1,
      isHave: false,
      collapsed: false,
      activePath,
      currMenu: '',
      userMenus: [
        { index: 1, icon: 'user', url: '/home/user', title: '个人中心' },
        { index: 2, icon: 'usergroup-delete', url: '/home/customer', title: '客户管理' }
      ],
      receiveData: null
    }
  },
  created () {
  },
  mounted () {
    const index = window.sessionStorage.getItem('index')
    this.saveIndex(index)
    this.$socket.emit('hi', { subscribe: true }) // 在这里触发connect事件
  },
  sockets: { // 通过vue实例对象sockets实现组件中的事件监听
    connect: function () { // socket的connect事件
      console.log('socket connected from Page--------------')
    },
    hi (data) { // 后端按主题名推送的消息数据
      this.remindCount = 1
      this.isHave = true
      this.receiveData = data
      this.openNotification()
      console.log(data)
    }
  },
  methods: {
    listenFromUser (data) {
      this.remindCount = data
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
      if (this.remindCount > 0) {
        this.$notification.success({
          message: '新消息',
          description:
          this.receiveData,
          style: {
            border: '1px solid green'
          },
          duration: 0
        })
      } else {
        this.$notification.warning({
          message: '无新消息！',
          duration: 1
        })
      }
    }
  },
  destroyed () {
    this.websock.close() // 离开路由之后断开websocket连接
  }
}
</script>

<style lang="less" scoped>
#home{
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
  h1{
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
.ant-layout{
  height: 100%;
}
.ant-layout-content{
  height: 100%;
}
</style>
