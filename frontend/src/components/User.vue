<style lang="less" scoped>
.user-layout-user {
    & > h3 {
        font-size: 16px;
        margin-bottom: 20px;
    }
    .clock {
        float: right;
    }
}
</style>

<template>
<div style="height:100%" class="main user-layout-user">
  <div style="padding:30px;">
    <a-card hoverable :bordered="false">
      <a-row :gutter="16">
        <a-col :span="16">
          <a-col :span="5">
            <a-avatar shape="square" :size="150" :style="{ backgroundColor: '#00245D', fontSize: '50px', verticalAlign: 'middle' }">{{ currUser.name }}
            </a-avatar>
          </a-col>
          <a-col :span="8">
            <a-statistic title="Email" :value="currUser.email" class="demo-class">
            </a-statistic>
            <a-statistic title="Number of Clients" :value="currUser.n_clients" class="demo-class">
            </a-statistic>
          </a-col>
        </a-col>
        <a-col :span="8">
          <clock class="clock"></clock>
        </a-col>
      </a-row>
    </a-card>
  </div>
</div>
</template>

<script>
import Clock from 'vue-clock2'
import {
  userInfo
} from '../api/api'

export default {
  components: {
    Clock
  },
  data () {
    return {
      currUser: null,
      headers: {
        Authorization: window.sessionStorage.getItem('Authorization')
      }
    }
  },
  mounted () {
    userInfo()
      .then((res) => {
        console.log(res)
        if (res.data.code === 0) {
          console.log(res.data.data)
          this.currUser = res.data.data
        } else {
          return this.$message.error(res.data.msg)
        }
      })
      .catch(err => {
        console.log(err)
      })
  },
  method: {}
}
</script>
