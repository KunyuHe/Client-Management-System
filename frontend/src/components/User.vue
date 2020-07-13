<template>
<div style="height:100%" class="main user-layout-user">
  <div style="padding:30px;">
    <a-card hoverable title='用户信息' :bordered="false">
      <a-row :gutter="16">
        <a-col :span="8">
          <a-card hoverable :bordered="false">
            <a-card-meta title="客户数量">
              <a-avatar slot="avatar" shape="square" :size="90" :style="{ backgroundColor: '#00245D', fontSize: '30px'}">{{ currUser.name }}
              </a-avatar>
              <a-statistic slot="description" :value="currUser.n_clients" class="demo-class" />
            </a-card-meta>
          </a-card>
        </a-col>
        <a-col :offset="8" :span="8">
          <clock class="clock"></clock>
        </a-col>
      </a-row>
    </a-card>
  </div>

  <div style="padding:0 30px 30px;">
    <a-card hoverable title="文件处理" style="height:100%" :bordered="false">
      <a-row :gutter="16">
        <a-col :span="8">
          <a-card hoverable :bordered="false">
            <a-upload-dragger
              name="file"
              slot="cover"
              accept = ".xlsx"
              :multiple="true"
              :action="uploadUrl"
              :headers="headers"
              @change="handleChange">
              <p class="ant-upload-drag-icon">
                <a-icon type="inbox" />
              </p>
              <p class="ant-upload-text">
                点击或者拖拽上传Excel文件
              </p>
            </a-upload-dragger>
            <a-card-meta
              title="已经上传的文件总数"
              :description="fileCnt">
            </a-card-meta>
          </a-card>
        </a-col>

        <a-col :span="8">
          <a-form :form="form">
            <a-form-item>
              <a-textarea placeholder="请输入要插入的文本" v-decorator="['text']" :rows="6" />
            </a-form-item>

            <a-form-item>
              <a-button
                type="primary"
                htmlType="submit"
                class="process-button"
                @click.stop.prevent="handleProcess"
              >
                处理文件
              </a-button>

              <a-button
                type="primary"
                class="download-button"
                @click.stop.prevent="handleDownload"
              >
                下载文件
              </a-button>
            </a-form-item>

          </a-form>
        </a-col>

      </a-row>
    </a-card>
  </div>
</div>
</template>

<script>
import Clock from 'vue-clock2'
import {
  userInfo,
  url,
  processFile,
  getFile
} from '../api/api'

export default {
  components: {
    Clock
  },
  data () {
    return {
      form: this.$form.createForm(this),
      currUser: { name: '用户', n_clients: 0 },
      headers: {
        Authorization: window.sessionStorage.getItem('Authorization')
      },
      websock: null,
      uploadUrl: url + '/user/upload',
      fileCnt: '上传文件后显示',
      fileName: '',
      downloadUrl: url + '/user/download'
    }
  },
  created () {
    this.findUser()
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

    handleChange (info) {
      if (info.file.status === 'done') {
        const res = info.file.response
        if (res.code !== 0) {
          this.$message.error(res.msg)
        } else {
          this.$message.success(`${info.file.name}上传成功！`)
          this.fileCnt = res.data.cnt
          this.fileName = res.data.filename
        }
      } else if (info.file.status === 'uploading') {
        this.$message.loading(`${info.file.name}上传中，请稍候。`)
      }
    },

    handleProcess () {
      const data = { filename: this.fileName, text: this.form.getFieldValue('text') }
      processFile(data)
        .then((res) => {
          if (res.data.code === 0) {
            this.form.resetFields()
            return this.$message.success('文件处理成功！')
          } else {
            return this.$message.error(res.data.msg)
          }
        })
        .catch(err => {
          console.log(err)
        })
    },

    handleDownload () {
      const params = { filename: this.fileName }
      getFile(params)
        .then(res => {
          const data = res.data
          const blob = new Blob([data], { type: 'application/vnd.ms-excel' })
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = 'download.xlsx'
          link.click()
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style lang="less" scoped>
.user-layout-user {
    & > h3 {
        font-size: 16px;
        margin-bottom: 20px;
    }
    .clock {
        float: right;
    }
    .process-button {
        float: left;
        width: 40%;
    }
    .download-button {
        float: right;
        width: 40%;
    }
}
</style>
