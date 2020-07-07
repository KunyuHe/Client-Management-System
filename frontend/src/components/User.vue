<template>
<div style="height:100%" class="main user-layout-user">
  <div style="padding:30px;">
    <a-card hoverable :bordered="false">
      <a-row :gutter="16">
        <a-col :span="8">
          <a-card hoverable :bordered="false">
            <a-card-meta title="Number of Clients">
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
    <a-card hoverable title="Document Processing" style="height:100%" :bordered="false">
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
                Click or drag file to this area to upload
              </p>
            </a-upload-dragger>
            <a-card-meta
              title="Files Uploaded"
              :description="fileCnt">
            </a-card-meta>
          </a-card>
        </a-col>

        <a-col :offset="8" :span="8">
          <a-card hoverable :bordered="false">
            <a-button
              type="primary"
              icon="download"
              :headers="headers"
              @click="handleDownload(fileName)">
              Download File
            </a-button>
          </a-card>
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
  getFile
} from '../api/api'

export default {
  components: {
    Clock
  },
  data () {
    return {
      currUser: { name: 'User', n_clients: 0 },
      headers: {
        Authorization: window.sessionStorage.getItem('Authorization')
      },
      uploadUrl: url + '/user/upload',
      fileCnt: 0,
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
          this.$message.success(`${info.file.name} uploaded successfully.`)
          this.fileCnt = res.data.cnt
          this.fileName = res.data.filename
        }
      } else if (info.file.status === 'error') {
        this.$message.error(`${info.file.name} upload failed.`)
      }
    },

    handleDownload (filename) {
      getFile()
        .then(res => {
          console.log("I'm here")
          console.log(res)
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
}
</style>
