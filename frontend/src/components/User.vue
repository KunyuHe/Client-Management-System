<template>
    <div style="height:100%">
        <div style="padding:30px;">
            <a-card hoverable  :bordered="false" >
                <a-row :gutter="16">
                    <a-col class="gutter-row" :span="22">
                        <a-list :data-source="currUser">
                            <a-list-item slot="renderItem" slot-scope="item">
                                <a-list-item-meta :description="item.email">
                                <h2 slot="title" >{{ item.username }}</h2>
                                <a-avatar :size="100" slot="avatar" src="https://preview.pro.antdv.com/avatar2.jpg" />
                                </a-list-item-meta>
                                <div>
                                  <clock color="#001529" :time="time"></clock>
                                </div>
                            </a-list-item>
                        </a-list>
                    </a-col>
                    <a-col class="gutter-row" :span="2">
                    </a-col>
                </a-row>
            </a-card>
        </div>
        <div style="padding:0 30px 30px;">
            <a-card hoverable  title="发送估值表" style="height:100%" :bordered="false" >
              <a-row :gutter="16">
                <a-col :span="8">
                  <a-select placeholder="请选择客户" :value="selectedCus" style="width: 100%" @change="handleCusChange">
                    <a-select-option v-for="item in cusData" :key="item.id" :value="item.id">{{item.name}}</a-select-option>
                  </a-select>
                </a-col>
                <a-col :span="8">
                  <a-upload
                  :disabled="!isSelected"
                    accept = ".xlsx"
                    name="file"
                    :action="uploadUrl"
                    :headers="headers"
                    :data="{customer_id:selectedCus}"
                    @change="handleFileChange"
                  >
                    <a-button @click="mUpload"> <a-icon type="upload" /> 点击选择估值表（excel）</a-button>
                  </a-upload>
                </a-col>
                <a-col :span="8"></a-col>
              </a-row>
            </a-card>
        </div>
        <div id="remind" style="padding:0 30px 30px;">
            <a-card hoverable  title="客户提醒" style="height:100%" :bordered="false" >
                <a-timeline mode="alternate">
                  <a-timeline-item v-for="item in reminddata" :key="item.time">
                    <span style="color:#377cee;">{{item.time}}</span> <span>{{item.title}}</span>
                  </a-timeline-item>
                </a-timeline>
            </a-card>
        </div>
    </div>
</template>

<script>
import Clock from 'vue-clock2'
import { findAllCustomers, url } from '../api/api'

const reminddata = [
  {
    time: '2015-09-01',
    title: 'Ant Design Title 1'
  },
  {
    time: '2015-09-02',
    title: 'Ant Design Title 2'
  },
  {
    time: '2015-09-03',
    title: 'Ant Design Title 3'
  },
  {
    time: '2015-09-04',
    title: 'Ant Design Title 4'
  }
]
export default {
  components: { Clock },
  data () {
    return {
      uploadUrl: url + '/user/send',
      currUser: [],
      cusData: [],
      time: '8:10',
      reminddata,
      headers: {
        Authorization: window.sessionStorage.getItem('Authorization')
      },
      selectedCus: '请选择客户',
      isSelected: false,
      websock: null
    }
  },
  cteated () {
  },
  mounted () {
    this.handleRemind()
    this.findCus()
    window.setInterval(() => {
      setTimeout(this.fun, 0)
    }, 1000)
  },
  methods: {
    fun () {
      const date = new Date()
      let h = date.getHours()
      h = h < 10 ? ('0' + h) : h
      let m = date.getMinutes()
      m = m < 10 ? ('0' + m) : m
      let s = date.getSeconds()
      s = s < 10 ? ('0' + s) : s
      this.time = h + ':' + m + ':' + s
    },
    handleRemind () {
      this.$emit('listenToHome', 0)
    },
    handleCusChange (value) {
      this.selectedCus = value
      console.log('handleCusChange===', value, this.selectedCus)
      if (this.selectedCus !== '') this.isSelected = true
    },
    mUpload () {
      if (!this.isSelected) return this.$message.error('请选择客户')
    },
    handleFileChange () {
    },
    findCus () {
      findAllCustomers()
        .then((res) => {
          console.log(res)
          if (res.data.code === 0) {
            this.currUser.push(res.data.data)
            this.cusData = res.data.data.customers
          } else {
            return this.$message.error(res.data.msg)
          }
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style lang="less" scoped>

</style>
