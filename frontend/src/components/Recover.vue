<template>
<div class="main user-layout-recover">
  <a-form ref="formRecover" :form="form" id="formRecover">

    <a-form-item>
      <a-input
        size="large"
        type="text"
        placeholder="邮箱"
        v-decorator="['email',
                      {rules: [{ required: true,
                                 type: 'email',
                                 message: '请输入有效的邮箱地址！' }],
                       validateTrigger: ['change', 'blur']}]">
      </a-input>
    </a-form-item>

    <a-form-item>
      <a-button
        size="large"
        type="primary"
        htmlType="submit"
        class="recover-button"
        :loading="recoverBtn"
        :disabled="recoverBtn"
        @click.stop.prevent="handleSubmit"
      >
        发送邮件以找回密码
      </a-button>

      <router-link class="login" :to="{ name: 'Login' }">
        使用已有账号登录
      </router-link>
    </a-form-item>

  </a-form>
</div>
</template>

<script>
import {
  recover
} from '../api/api'
import {
  timeFix
} from '@/utils/util'

export default {
  name: 'Recover',
  components: {},
  mixins: [],
  data () {
    return {
      form: this.$form.createForm(this),
      state: {
        time: 60,
        progressColor: '#FF0000'
      },
      recoverBtn: false
    }
  },
  methods: {
    handleSubmit () {
      const {
        form: {
          validateFields
        },
        state
      } = this
      validateFields({
        force: true
      }, (err, values) => {
        if (!err) {
          const recoverParams = {
            ...values
          }
          recover(recoverParams)
            .then((res) => {
              if (res.data.code !== 0) {
                return this.$message.error(res.data.msg)
              } else {
                this.recoverSuccess(res)
              }
            })
            .catch(err => this.requestFailed(err))
            .finally(() => {
              state.loginBtn = false
            })
        } else {
          console.log(err, values)
        }
      })
    },

    recoverSuccess (res) {
      console.log(res)
      this.$router.push({
        path: '/hello/login'
      })
      setTimeout(() => {
        this.$notification.success({
          message: '找回密码邮件已发送',
          description: `${timeFix()}，请检查您的收件箱以取回登录密码！`
        })
      }, 1000)
      this.isLoginError = false
    },

    requestFailed (err) {
      this.$notification.error({
        message: 'Error',
        description: ((err.response || {}).data || {}).message || '服务器未响应！请稍后再试。',
        duration: 4
      })
      this.recoverBtn = false
    }
  }
}
</script>

<style lang="less">
.user-recover {
    &.error {
        color: #ff0000;
    }
    &.warning {
        color: #ff7e05;
    }
    &.success {
        color: #52c41a;
    }
}
.user-layout-recover {
    .ant-input-group-addon:first-child {
        background-color: #fff;
    }
}
</style>
<style lang="less" scoped>
.user-layout-recover {
    & > h3 {
        font-size: 16px;
        margin-bottom: 20px;
    }
    .recover-button {
        width: 50%;
        float: left;
    }
    .login {
        float: right;
        line-height: 40px;
    }
}
</style>
