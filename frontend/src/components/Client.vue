<template>
    <div style="padding:30px;">
        <a-card title="客户管理" hoverable  style="height:100%" :bordered="false" >
            <a slot="extra" @click="visible = true">添加客户</a>
            <a-table :rowKey="record => record.id" :columns="columns" :data-source="cusData"
            :pagination="{ pageSize: 4 }">
                <!-- <a slot="name" slot-scope="text">{{ text }}</a> -->
                <!-- <span slot="customTitle"><a-icon type="smile-o" /> 客户名</span> -->
                <span slot="action" slot-scope="text, record">
                <!-- <a-button type="primary" @click="chartVisible = true,openDiolog()">查看收入 - {{ record.name }}</a-button> -->
                <!-- <a-divider type="vertical" /> -->
                <a-button type="danger" @click="del(record.id)">删除</a-button>
                </span>
            </a-table>
            <a-select placeholder="请选择客户" :value="selectedCus" style="width: 20%; float:right; z-index: 10" @change="handleCusChange">
              <a-select-option v-for="item in cusData" :key="item.id" :value="item.name">{{item.name}}</a-select-option>
            </a-select>
            <div ref="customersRef" style="height: 600px"></div>
        </a-card>
        <div>
          <!-- 客户添加 -->
        <a-modal v-model="visible"
         :footer="null"
         title="添加客户"
         @ok="visible = false"
         :width="500">
             <a-form :form="form" @submit="handleCusSubmit">
              <a-form-item >
                <span slot="label">
                  客户名&nbsp;
                </span>
                <a-input
                  v-decorator="[
                    'name',
                    {
                      rules: [{ required: true, message: '请输入客户名!', whitespace: true }],
                    },
                  ]"
                />
              </a-form-item>

              <a-form-item label="E-mail">
                <a-input
                  v-decorator="[
                    'email',
                    {
                      rules: [
                        {
                          type: 'email',
                          message: '无效邮箱地址!',
                        },
                        {
                          required: true,
                          message: '请输入邮箱!',
                        },
                      ],
                    },
                  ]"
                />
              </a-form-item>
              <a-form-item>
                <a-button block type="primary" html-type="submit">
                  添加
                </a-button>
              </a-form-item>
            </a-form>
        </a-modal>
        <!-- 曲线查看 -->
        <a-modal v-model="chartVisible"
         :footer="null"
         title="查看收入情况"
         @ok="chartVisible = false"
         :width="800">
         <div ref="customerRef" style="height: 600px"></div>
        </a-modal>
    </div>
    </div>
</template>

<script>
import { findAllCustomers, addCustomer } from '../api/api'

const columns = [
  {
    title: '客户名',
    dataIndex: 'name',
    key: 'name'
  },
  {
    title: '邮箱',
    dataIndex: 'email',
    key: 'email'
  },
  {
    title: '编辑',
    key: 'action',
    scopedSlots: { customRender: 'action' }
  }
]

const xValue = []

const yValue = []

export default {
  data () {
    return {
      form: this.$form.createForm(this),
      currUser: null,
      cusData: [],
      selectedCus: '请选择客户',
      allIncomeSeries: [['date', 'value', 'product']],
      columns,
      visible: false,
      chartVisible: false,
      xValue,
      yValue
    }
  },
  mounted () {
    // this.$nextTick(function () {
    this.initEcharts()
    // })
    this.findCus()
  },
  methods: {
    initEcharts () {
      var customerCharts = this.$echarts.init(this.$refs.customersRef)
      var option = {
        // backgroundColor: '#f8f8f8',
        title: {
          text: '客户收入情况',
          left: 'left'
        },
        tooltip: {
          trigger: 'axis', // axis , item
          axisPointer: {
            type: 'line', // 'line' | 'cross' | 'shadow' | 'none
            lineStyle: {
              color: '#c9caca',
              width: 1,
              type: 'dotted'
            }
          },
          x: 'left',
          textStyle: {
            fontSize: 14
          }
        },
        legend: {
        },
        // dataset: {
        //   source: this.allIncomeSeries
        // },
        grid: {
          top: '12%',
          right: '5%',
          bottom: '15%',
          left: '7%'
        },
        xAxis: {
          type: 'category',
          axisLabel: {
            // rotate: 45,
            interval: 0, // 类目间隔 设置为 1，表示(隔一个标签显示一个标签)
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
              color: 'rgba(102,102,102,.1)', // 纵向网格线颜色
              width: 1,
              type: 'dashed'
            }
          },
          axisTick: {
            show: true // 坐标轴小标记
          },
          data: this.xValue // 载入横坐标数据
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
          splitNumber: 4, // y轴刻度设置(值越大刻度越小)
          axisLine: {
            lineStyle: {
              color: '#ccc',
              width: 1
            }
          },
          splitLine: {
            show: true,
            lineStyle: {
              color: 'rgba(102,102,102,.1)', // 横向网格线颜色
              width: 1,
              type: 'dashed'
            }
          }
        },
        // color: ['#b61e33', 'rgb(255, 160, 25)', 'rgb(17, 191, 199)', 'rgba(77, 80, 84, 0.7)'], //自定义颜色
        series: [
          {
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
          }
        ]
      }
      customerCharts.setOption(option)
    },
    handleCusChange (value) {
      this.selectedCus = value
      for (let index = 0; index < this.cusData.length; index++) {
        const customer = this.cusData[index]
        if (value === customer.name) {
          console.log(customer)
          this.xValue = []
          this.yValue = []
          for (let index = 0; index < customer.incomes.length; index++) {
            const income = customer.incomes[index]
            this.xValue.push(income.date)
            this.yValue.push(income.value)
          }
          console.log(this.xValue)
        }
      }
      this.initEcharts()
    },
    openEchart () {
      var customerChart = this.$echarts.init(this.$refs.customerRef)
      var option = {
        title: {
          text: '客户收入曲线',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        toolbox: {
          show: true,
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['00:00', '01:15', '02:30', '03:45', '05:00', '06:15', '07:30', '08:45', '10:00', '11:15', '12:30', '13:45', '15:00', '16:15', '17:30', '18:45', '20:00', '21:15', '22:30', '23:45']
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value} W'
          },
          axisPointer: {
            snap: true
          }
        },
        visualMap: {
          show: false,
          dimension: 0,
          pieces: [{
            gt: 0,
            lte: 20,
            color: 'green'
          }]
        },
        series: [
          {
            name: '客户1',
            type: 'line',
            smooth: true,
            data: [300, 280, 250, 260, 270, 300, 550, 500, 400, 390, 380, 390, 400, 500, 600, 750, 800, 700, 600, 400]
          },
          {
            name: '客户2',
            type: 'line',
            smooth: true,
            data: [100, 250, 250, 160, 270, 300, 170, 300, 420, 370, 320, 300, 440, 540, 360, 780, 880, 780, 680, 480]
          }
        ]
      }
      // 使用刚指定的配置项和数据显示图表。
      customerChart.setOption(option)
    },
    openDiolog () {
      this.$nextTick(function () {
        this.openEchart()
      })
    },
    handleCusSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          const params = { ...values }
          // eslint-disable-next-line no-debugger
          // debugger
          console.log(params)
          addCustomer(params)
            .then((res) => {
              console.log(res)
              if (res.data.code === 0) {
                this.findCus()
                this.visible = false
                this.form.resetFields()
                return this.$message.success(res.data.msg)
              } else {
                return this.$message.error(res.data.msg)
              }
            })
            .catch(err => {
              console.log(err)
            })
        }
      })
    },
    del (cus) {
      console.log(cus)
    },
    findCus () {
      findAllCustomers()
        .then((res) => {
          console.log(res)
          if (res.data.code === 0) {
            this.currUser = res.data.data
            this.cusData = res.data.data.customers
            var firstCus = ''
            for (let index = 0; index < this.cusData.length; index++) {
              const element = this.cusData[index]
              if (firstCus === '') {
                firstCus = element.name
              }
            }
            console.log(firstCus)
            this.handleCusChange(firstCus)
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
