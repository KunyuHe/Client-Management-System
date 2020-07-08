<template>
<div style="padding:30px;">
  <a-card title="客户列表" hoverable style="height:100%" :bordered="false">
    <a-input-search class="form-control" type="text" v-model="searchQuery" placeholder="按名称搜索客户" slot="extra" enter-button />
    <a-table :rowKey="record => record.id" :columns="columns" :data-source="resultQuery" :pagination="{ pageSize: 10 }">
      <span slot="action" slot-scope="text, record">
        <a-col :span="2">
          <a-button type="danger" @click="selectedClient = record, showChart(record)">
            查看客户收入曲线
          </a-button>
        </a-col>
        <a-col :offset="3" :span="2">
          <a-button type="primary" @click="selectedClient = record, draftVisible = true">
            向客户发送估值表
          </a-button>
        </a-col>
      </span>
    </a-table>
  </a-card>

  <div>
    <a-modal :title="`客户${selectedClient.name}收入曲线`" :visible.sync="chartVisible" @ok="chartVisible = false" @cancel="chartVisible = false" :height="800" :width="1300">
      <div ref="incomeSeries" :style="{height: '800px', width: '1200px'}"></div>
    </a-modal>

    <a-modal :visible.sync="draftVisible" :title="`向客户${selectedClient.name}发送估值表`" @cancel="draftVisible = false, clearForm()" @ok="draftVisible = false, clearForm()" :width="500">
      <a-form :form="form">
        <a-form-item label="主题">
          <a-input :placeholder="defaultSubject" v-decorator="['subject']"/>
        </a-form-item>

        <a-form-item label="正文">
          <a-textarea :placeholder="defaultBody" v-decorator="['body']" :rows="8"/>
        </a-form-item>

        <a-form-item label="添加附件并发送邮件">
          <a-upload-dragger
            name="file"
            accept = ".xlsx"
            :multiple="false"
            :headers="headers"
            :data="{id: selectedClient.id, subject: subject, body: body}"
            :action="emailUrl"
            @change="handleChange">
            <p class="ant-upload-drag-icon">
              <a-icon type="inbox" />
            </p>
            <p class="ant-upload-text">
              点击或者拖拽上传估值表并发送邮件
            </p>
          </a-upload-dragger>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>

</div>
</template>

<script>
import {
  userInfo,
  getClients,
  getIncomes,
  url
} from '../api/api'

const columns = [{
  title: '名称',
  dataIndex: 'name',
  key: 'name'
},
{
  title: '邮箱',
  dataIndex: 'email',
  key: 'email'
},
{
  title: '',
  key: 'action',
  scopedSlots: {
    customRender: 'action'
  }
}]

const xValue = []

const yValue = []

export default {
  data () {
    return {
      form: this.$form.createForm(this),
      headers: {
        Authorization: window.sessionStorage.getItem('Authorization')
      },
      currUser: { name: 'User', n_clients: 0 },
      clients: [],
      columns,
      searchQuery: null,
      selectedClient: { name: '' },
      chartVisible: false,
      draftVisible: false,
      defaultSubject: '估值表',
      emailUrl: url + '/client/email',
      xValue,
      yValue
    }
  },
  computed: {
    resultQuery () {
      if (this.searchQuery) {
        return this.clients.filter((item) => {
          return this.searchQuery.toLowerCase().split(' ').every(v => item.name.toLowerCase().includes(v))
        })
      } else {
        return this.clients
      }
    },

    defaultBody () {
      return `尊敬的${this.selectedClient.name}:

用户${this.currUser.name}通过管理系统为您发送了估值表。请查收！

如有任何问题，请联系${this.currUser.email}。

祝好，
客户管理系统（CMS)`
    },

    subject () {
      const formSubject = this.form.getFieldValue('subject')
      if (typeof formSubject === 'undefined') {
        return this.defaultSubject
      } else {
        return formSubject
      }
    },

    body () {
      const formBody = this.form.getFieldValue('body')
      if (typeof formBody === 'undefined') {
        return this.defaultBody
      } else {
        return formBody
      }
    }
  },
  watch: {
    yValue: {
      handler (newVal, oldVal) {
        this.openEchart()
      },
      deep: true
    }
  },
  mounted () {
    this.findUser()
    this.findClients()
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

    findClients () {
      getClients()
        .then((res) => {
          if (res.data.code === 0) {
            this.clients = res.data.data
          } else {
            return this.$message.error(res.data.msg)
          }
        })
        .catch(err => {
          console.log(err)
        })
    },

    checkIncomes (record) {
      const clientParams = {
        id: record.id
      }
      getIncomes(clientParams)
        .then((res) => {
          console.log(res)
          if (res.data.code === 0) {
            this.xValue = res.data.data.date
            this.yValue = res.data.data.value
          } else {
            return this.$message.error(res.data.msg)
          }
        })
        .catch(err => {
          console.log(err)
        })
    },

    openEchart () {
      this.$nextTick(() => {
        const incomeTS = this.$echarts.init(this.$refs.incomeSeries)
        const option = {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'line',
              lineStyle: {
                color: '#c9caca',
                width: 1,
                type: 'dotted'
              }
            }
          },
          toolbox: {
            show: true,
            feature: {
              saveAsImage: {
              },
              dataView: {
              },
              magicType: {
                type: ['line', 'bar']
              },
              dataZoom: {
                title: {
                  zoom: '选定方形区域缩放'
                }
              }
            }
          },
          grid: {
            top: '12%',
            right: '5%',
            bottom: '15%',
            left: '7%'
          },
          xAxis: {
            name: '日期',
            type: 'category',
            axisLabel: {
              rotate: 90,
              interval: 'auto',
              textStyle: {
                color: '#333',
                fontSize: 12
              }
            },
            axisLine: {
              lineStyle: {
                color: '#ccc',
                width: 1
              }
            },
            splitLine: {
              show: true,
              lineStyle: {
                color: 'rgba(102,102,102,.1)',
                width: 1,
                type: 'dashed'
              }
            },
            axisTick: {
              show: false
            },
            data: this.xValue
          },
          yAxis: {
            name: '收入（元）',
            type: 'value',
            axisLabel: {
              show: true,
              textStyle: {
                color: '#333',
                fontSize: 12
              },
              formatter: '{value}'
            },
            splitNumber: 4,
            axisLine: {
              lineStyle: {
                color: '#ccc',
                width: 1
              }
            },
            splitLine: {
              show: true,
              lineStyle: {
                color: 'rgba(102,102,102,.1)',
                width: 1,
                type: 'dashed'
              }
            }
          },
          series: [{
            type: 'line',
            symbol: 'circle',
            symbolSize: 6,
            smooth: true,
            lineStyle: {
              normal: {
                width: 2
              }
            },
            data: this.yValue
          }]
        }
        incomeTS.setOption(option)
      })
    },

    showChart (record) {
      this.checkIncomes(record)
      this.chartVisible = true
      this.openEchart()
    },

    handleChange (info) {
      if (info.file.status === 'done') {
        const res = info.file.response
        if (res.code !== 0) {
          this.$message.error(res.msg)
        } else {
          this.$message.success('Email successfully sent.')
          this.draftVisible = false
          this.clearForm()
        }
      } else if (info.file.status === 'uploading') {
        this.$message.loading('Sending email. Please wait.')
      }
    },

    clearForm () {
      this.form.resetFields()
    }
  }
}
</script>

<style lang="less" scoped>

</style>
