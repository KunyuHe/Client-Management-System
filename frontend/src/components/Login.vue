<template>
  <div class="main">
    <a-form
      id="formLogin"
      class="user-layout-login"
      ref="formLogin"
      :form="form"
      @submit="handleSubmit"
    >
        <a-alert v-if="isLoginError" type="error" showIcon style="margin-bottom: 24px;" message="Wrong username or password!" />
          <a-form-item>
            <a-input
              size="large"
              type="text"
              placeholder="Username or Email Address"
              v-decorator="[
                'username',
                {rules: [{ required: true, message: 'Please enter the username or email address!' }, { validator: handleUsernameOrEmail }], validateTrigger: 'change'}
              ]"
            >
              <a-icon slot="prefix" type="user" :style="{ color: 'rgba(0,0,0,.25)' }"/>
            </a-input>
          </a-form-item>

          <a-form-item>
            <a-input
              size="large"
              type="password"
              autocomplete="false"
              placeholder="Password"
              v-decorator="[
                'password',
                {rules: [{ required: true, message: 'Please enter the password!' }], validateTrigger: 'blur'}
              ]"
            >
              <a-icon slot="prefix" type="lock" :style="{ color: 'rgba(0,0,0,.25)' }"/>
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
        >Login</a-button>
      </a-form-item>

      <div class="user-login-other">
          <router-link
          :to="{ name: 'Recover', params: { username: username} }"
        >Forgot password?</router-link>
        <router-link :to="{ name: 'Register' }">Register</router-link>
      </div>
    </a-form>

  </div>
</template>

<script>
import md5 from 'md5'
import { timeFix } from '@/utils/util'
import { login } from '../api/api'

export default {
  components: {
  },
  data () {
    return {
      isLoginError: false,
      form: this.$form.createForm(this),
      username: '',
      state: {
        time: 60,
        loginBtn: false,
        // login type: 0 email, 1 username, 2 telephone
        loginType: 0
      }
    }
  },
  created () {
  },
  methods: {
    // handler
    handleUsernameOrEmail (rule, value, callback) {
      const { state } = this
      const regex = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/
      if (regex.test(value)) {
        state.loginType = 0
      } else {
        this.username = value
        console.log(value)
        state.loginType = 1
      }
      callback()
    },
    handleSubmit (e) {
      e.preventDefault()
      const {
        form: { validateFields },
        state
      } = this

      state.loginBtn = true

      validateFields({ force: true }, (err, values) => {
        if (!err) {
          console.log('login form', values)
          const loginParams = { ...values }
          delete loginParams.username
          loginParams.username = values.username
          loginParams.password = md5(values.password)
          console.log(loginParams)
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
      console.log(res)
      if (res.data.code === 0) {
        const token = res.data.data.access_token
        window.sessionStorage.setItem('Authorization', token)
        this.$router.push({ path: '/home' })
        // 延迟 1 秒显示欢迎信息
        setTimeout(() => {
          this.$notification.success({
            message: '欢迎',
            description: `${timeFix()}，欢迎回来`
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
        message: '错误',
        description: ((err.response || {}).data || {}).message || '请求出现错误，请稍后再试',
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
