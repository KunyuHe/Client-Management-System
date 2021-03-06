<template>
<div class="main">
  <a-form
    id="formLogin"
    class="user-layout-login"
    ref="formLogin"
    :form="form"
    @submit="handleSubmit">
    <a-alert
      v-if="isLoginError"
      type="error"
      showIcon
      style="margin-bottom: 24px;" message="Wrong username or password!" />
    <a-form-item>
      <a-input
        size="large"
        type="text"
        placeholder="用户名"
        v-decorator="['name',
                      {rules: [{ required: true,
                                 message: '请输入用户名！' },
                               { validator: handleUsernameOrEmail }],
                       validateTrigger: 'change'}]"
      >
        <a-icon slot="prefix" type="user" :style="{ color: 'rgba(0,0,0,.25)' }" />
      </a-input>
    </a-form-item>

    <a-form-item>
      <a-input
        size="large"
        type="password"
        autocomplete="false"
        placeholder="密码"
        v-decorator="['password',
                      {rules: [{ required: true,
                                 message: '请输入密码！' }],
                       validateTrigger: 'blur'}]"
      >
        <a-icon slot="prefix" type="lock" :style="{ color: 'rgba(0,0,0,.25)' }" />
      </a-input>
    </a-form-item>

    <a-form-item style="margin-top:24px">
      <a-button
        size="large"
        type="primary"
        htmlType="submit"
        class="login-button"
        :loading="state.loginBtn"
        :disabled="state.loginBtn"
      >
        登录
      </a-button>
    </a-form-item>

    <div class="user-login-other">
      <router-link :to="{ name: 'Recover', params: { username: username} }">
        忘记密码?
      </router-link>
      <router-link :to="{ name: 'Register' }">
        注册
      </router-link>
    </div>
  </a-form>

</div>
</template>

<script>
import {
  timeFix
} from '@/utils/util'
import {
  login
} from '../api/api'

export default {
  components: {},
  data () {
    return {
      isLoginError: false,
      form: this.$form.createForm(this),
      username: '',
      state: {
        time: 60,
        loginBtn: false
      }
    }
  },
  created () {},
  methods: {
    // handler
    handleUsernameOrEmail (rule, value, callback) {
      const {
        state
      } = this
      const regex = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/
      if (regex.test(value)) {
        state.loginType = 0
      } else {
        this.username = value
        state.loginType = 1
      }
      callback()
    },
    handleSubmit (e) {
      e.preventDefault()
      const {
        form: {
          validateFields
        },
        state
      } = this

      state.loginBtn = true

      validateFields({
        force: true
      }, (err, values) => {
        if (!err) {
          const loginParams = {
            ...values
          }
          login(loginParams)
            .then((res) => this.loginSuccess(res))
            .catch(err => this.requestFailed(err))
            .finally(() => {
              state.loginBtn = false
            })
        } else {
          setTimeout(() => {
            state.loginBtn = false
          }, 600)
        }
      })
    },
    loginSuccess (res) {
      if (res.data.code === 0) {
        const token = res.data.data.access_token
        const username = res.data.data.user.name
        window.sessionStorage.setItem('Authorization', token)
        this.$router.push({
          path: '/home'
        })
        // 延迟 1 秒显示欢迎信息
        setTimeout(() => {
          this.$notification.success({
            message: username,
            description: `${timeFix()}，欢迎回来！`
          })
        }, 1000)
        this.isLoginError = false
      } else {
        this.$notification.error({
          message: '登录失败',
          description: res.data.msg
        })
      }
    },
    requestFailed (err) {
      this.isLoginError = true
      this.$notification.error({
        message: 'Error',
        description: ((err.response || {}).data || {}).message || '服务器未响应！请稍后再试。',
        duration: 4
      })
    }
  }
}
</script>

<style lang="less" scoped>
button.login-button {
    padding: 0 15px;
    font-size: 16px;
    height: 40px;
    width: 100%;
}

.user-login-other {
    display: flex;
    justify-content: space-between;
    // text-align: left;
    margin-top: 24px;
    line-height: 22px;
    .forge-password {
        font-size: 14px;
    }
}
</style>
