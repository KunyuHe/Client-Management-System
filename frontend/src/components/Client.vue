<template>
<div style="padding:30px;">
  <a-card title="Client List" hoverable style="height:100%" :bordered="false">
    <a-input-search class="form-control" type="text" v-model="searchQuery" placeholder="Search Client by Name" slot="extra" enter-button />
    <a-table :rowKey="record => record.id" :columns="columns" :data-source="resultQuery" :pagination="{ pageSize: 10 }">
      <span slot="action" slot-scope="text, record">
        <a-col :span="2">
          <a-button type="primary" @click="showChart(record)">
            Check Income
          </a-button>
        </a-col>
        <a-col :offset="2" :span="2">
          <a-button type="primary" @click="draftVisible=true">
            Draft Email
          </a-button>
        </a-col>
      </span>
    </a-table>
  </a-card>

  <div>
    <a-modal :title="'Client ' + selectedClient + ' Income Time Series'" :visible.sync="chartVisible" @ok="chartVisible = false" @cancel="chartVisible = false" :height="800" :width="1300">
      <div ref="incomeSeries" :style="{height: '800px', width: '1200px'}"></div>
    </a-modal>

    <a-modal :visible.sync="draftVisible" :title="'Email Client '+ selectedClient" @ok="draftVisible = false" @cancel="draftVisible = false" :width="500">
      <a-form :form="form" @submit="handleCusSubmit">
        <a-form-item label="Subject">
          <a-input :placeholder="defaultSubject" v-decorator="['subject']"/>
        </a-form-item>

        <a-form-item label="Body">
          <a-textarea :placeholder="defaultBody" v-decorator="['body']" :rows="10"/>
        </a-form-item>

        <a-form-item>
          <a-button block type="primary" html-type="submit">
            Send Email
          </a-button>
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
  getIncomes
} from '../api/api'

const columns = [{
  title: 'Name',
  dataIndex: 'name',
  key: 'name'
},
{
  title: 'Email',
  dataIndex: 'email',
  key: 'email'
},
{
  title: 'Action',
  key: 'action',
  scopedSlots: {
    customRender: 'action'
  }
}]

const defaultBody = `尊敬的<客户名>:

用户<用户名>通过管理系统为您发送了估值表。请查收！

如有任何问题，请联系<用户邮箱>。

祝好，
客户管理系统（CMS）
`

const xValue = []

const yValue = []

export default {
  data () {
    return {
      headers: {
        Authorization: window.sessionStorage.getItem('Authorization')
      },
      currUser: { name: 'User', n_clients: 0 },
      clients: [],
      columns,
      searchQuery: null,
      selectedClient: '',
      chartVisible: false,
      draftVisible: false,
      defaultSubject: '估值表',
      defaultBody,
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
            this.selectedClient = record.name
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
                title: 'Save as Image'
              },
              dataZoom: {
                title: {
                  zoom: 'Area Zooming',
                  back: 'Restore Area Zooming'
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
            name: 'Date',
            type: 'category',
            axisLabel: {
              rotate: 90,
              interval: 'auto', // 类目间隔 设置为 1，表示(隔一个标签显示一个标签)
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
            name: 'Income (yuan)',
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
    }
  }
}
</script>

<style lang="less" scoped>

</style>
