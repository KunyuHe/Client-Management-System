<template>
  <div class="main user-layout-register">
    <h2><span>User Registration</span></h2>
    <a-form ref="formRegister" :form="form" id="formRegister">

      <a-form-item>
        <a-input
          size="large"
          type="text"
          placeholder="User Name"
          v-decorator="['username', {rules: [{ required: true, message: 'Please enter username.' }], validateTrigger: ['blur']}]"
        ></a-input>
      </a-form-item>

      <a-form-item>
        <a-input
          size="large"
          type="text"
          placeholder="Email"
          v-decorator="['email', {rules: [{ required: true, type: 'email', message: 'Please enter email address.' }], validateTrigger: ['change', 'blur']}]"
        ></a-input>
      </a-form-item>

      <a-popover
        placement="rightTop"
        :trigger="['focus']"
        :getPopupContainer="(trigger) => trigger.parentElement"
        v-model="state.passwordLevelChecked">
        <template slot="content">
          <div :style="{ width: '240px' }" >
            <div :class="['user-register', passwordLevelClass]">Password strength：<span>{{ passwordLevelName }}</span></div>
            <a-progress :percent="state.percent" :showInfo="false" :strokeColor=" passwordLevelColor " />
            <div style="margin-top: 10px;">
              <span>Please enter at least 6 digits. Do not use easy-to-hack passwords.</span>
            </div>
          </div>
        </template>

        <a-form-item>
          <a-input
            size="large"
            type="password"
            @click="handlePasswordInputClick"
            autocomplete="false"
            placeholder="Password"
            v-decorator="['password', {rules: [{ required: true, message: 'Password length must be no less than 6. Case sensitive.'}, { validator: this.handlePasswordLevel }], validateTrigger: ['change', 'blur']}]"
          ></a-input>
        </a-form-item>
      </a-popover>

      <a-form-item>
        <a-input
          size="large"
          type="password"
          autocomplete="false"
          placeholder="Confirm Password"
          v-decorator="['password2', {rules: [{ required: true, message: 'Password length must be no less than 6. Case sensitive.' }, { validator: this.handlePasswordCheck }], validateTrigger: ['change', 'blur']}]"
        ></a-input>
      </a-form-item>

      <a-form-item>
        <a-input size="large" type="text" placeholder="Phone Number" v-decorator="['phone', {rules: [{ required: true, pattern: /^1[34578]\d{9}$/, message: 'Please enter correct phone number (mainland China).' }], validateTrigger: 'change'}]">
          <a-icon slot="prefix" type="mobile" :style="{ color: 'rgba(0,0,0,.25)' }"/>
        </a-input>
      </a-form-item>

      <a-form-item>
        <a-button
          size="large"
          type="primary"
          htmlType="submit"
          class="register-button"
          :loading="registerBtn"
          @click.stop.prevent="handleSubmit"
          :disabled="registerBtn">Register
        </a-button>

        <router-link class="login" :to="{ name: 'Login' }">Login with Existing Account</router-link>

      </a-form-item>

    </a-form>
  </div>
</template>

<script>
import md5 from 'md5'
import { timeFix } from '@/utils/util'
import { findByUsername, register } from '../api/api'

const levelNames = {
  0: 'Low',
  1: 'Low',
  2: 'Medium',
  3: 'Strong'
}
const levelClass = {
  0: 'error',
  1: 'error',
  2: 'warning',
  3: 'success'
}
const levelColor = {
  0: '#ff0000',
  1: '#ff0000',
  2: '#ff7e05',
  3: '#52c41a'
}
export default {
  name: 'Register',
  components: {
  },
  mixins: [],
  data () {
    return {
      form: this.$form.createForm(this),

      state: {
        time: 60,
        passwordLevel: 0,
        passwordLevelChecked: false,
        percent: 10,
        progressColor: '#FF0000'
      },
      registerBtn: false
    }
  },
  computed: {
    passwordLevelClass () {
      return levelClass[this.state.passwordLevel]
    },
    passwordLevelName () {
      return levelNames[this.state.passwordLevel]
    },
    passwordLevelColor () {
      return levelColor[this.state.passwordLevel]
    }
  },
  methods: {
    handlePasswordLevel (rule, value, callback) {
      let level = 0

      // 判断这个字符串中有没有数字
      if (/[0-9]/.test(value)) {
        level++
      }
      // 判断字符串中有没有字母
      if (/[a-zA-Z]/.test(value)) {
        level++
      }
      // 判断字符串中有没有特殊符号
      if (/[^0-9a-zA-Z_]/.test(value)) {
        level++
      }
      this.state.passwordLevel = level
      this.state.percent = level * 30
      if (level >= 2) {
        if (level >= 3) {
          this.state.percent = 100
        }
        callback()
      } else {
        if (level === 0) {
          this.state.percent = 10
        }
        callback(new Error('Your password is not strong enough.'))
      }
    },

    handlePasswordCheck (rule, value, callback) {
      const password = this.form.getFieldValue('password')
      // console.log('value', value)
      if (value === undefined) {
        callback(new Error('Please enter a valid password.'))
      }
      if (value && password && value.trim() !== password.trim()) {
        callback(new Error('Password entry mismatch.'))
      }
      callback()
    },

    handleUsernameCheck (rule, value, callback) {
      // console.log('handleUsernameCheck, rule:', rule)
      // console.log('handleUsernameCheck, value', value)
      // console.log('handleUsernameCheck, callback', callback)
      // if (value === '') callback(new Error('Username cannot be empty!'))
      const params = {
        name: value
      }
      findByUsername(params)
        .then(function (res) {
          console.log(res)
          if (value === 'admin') { callback(new Error('Username already in use!')) }
        })
        .catch(function (error) {
          console.log(error)
          callback(new Error('Connection to database failed!'))
        })
    },

    handlePasswordInputClick () {
    //   if (!this.isMobile()) {
    //     this.state.passwordLevelChecked = true
    //     return
    //   }
      this.state.passwordLevelChecked = false
    },

    handleSubmit () {
      console.log('Submitted.')
      const { form: { validateFields }, state } = this
      validateFields({ force: true }, (err, values) => {
        console.log('Validated.')
        if (!err) {
          state.passwordLevelChecked = false
          console.log(values)
          const registerParams = { ...values }
          delete registerParams.password2
          registerParams.password = md5(values.password)
          console.log(registerParams)
          register(registerParams)
            .then((res) => this.registerSuccess(res))
            .catch(err => this.requestFailed(err))
            .finally(() => {
              state.loginBtn = false
            })
        } else {
          console.log(err, values)
        }
      })
    },
    registerSuccess (res) {
      console.log(res)
      this.$router.push({ path: '/hello/login' })
      // 延迟 1 秒显示欢迎信息
      setTimeout(() => {
        this.$notification.success({
          message: 'Welcome!',
          description: `${timeFix()}. You are successfully registered!`
        })
      }, 1000)
      this.isLoginError = false
    },
    requestFailed (err) {
      this.$notification.error({
        message: 'Error',
        description: ((err.response || {}).data || {}).message || 'Your request was rejected. Try again later.',
        duration: 4
      })
      this.registerBtn = false
    }
  },
  watch: {
    'state.passwordLevel' (val) {
      console.log(val)
    }
  }
}
</script>
<style lang="less" scoped>
  .user-register {

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

  .user-layout-register {
    .ant-input-group-addon:first-child {
      background-color: #fff;
    }
  }
  .user-layout-register {

    & > h3 {
      font-size: 16px;
      margin-bottom: 20px;
    }

    .getCaptcha {
      display: block;
      width: 100%;
      height: 40px;
    }

    .register-button {
        float: left;
      width: 50%;
    }

    .login {
      float: right;
      line-height: 40px;
    }
  }
</style>
