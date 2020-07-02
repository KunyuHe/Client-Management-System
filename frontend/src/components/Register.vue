<template>
<div class="main user-layout-register">
  <h2><span>New User Registration</span></h2>
  <a-form ref="formRegister" :form="form" id="formRegister">
    <a-form-item>
      <a-input size="large" type="text" placeholder="Username" v-decorator="['name', {rules: [{ required: true, message: 'Please enter the username.' }], validateTrigger: ['blur']}]"></a-input>
    </a-form-item>

    <a-form-item>
      <a-input size="large" type="text" placeholder="Email" v-decorator="['email', {rules: [{ required: true, type: 'email', message: 'Please enter a valid email address.' }], validateTrigger: ['change', 'blur']}]"></a-input>
    </a-form-item>

    <a-form-item>
      <a-input-password size="large" @click="handlePasswordInputClick" placeholder="Password"
          v-decorator="['password', {rules: [{ required: true, message: 'At least 6 digits. Case sensitive.'}, { validator: this.handlePasswordLevel }], validateTrigger: ['change', 'blur']}]"></a-input-password>
    </a-form-item>

    <a-form-item>
      <a-input-password size="large" placeholder="Confirm Password" v-decorator="['password2', {rules: [{ required: true, message: 'Please enter the password again.' }, { validator: this.handlePasswordCheck }], validateTrigger: ['change', 'blur']}]">
      </a-input-password>
    </a-form-item>

    <a-form-item>
      <a-button size="large" type="primary" htmlType="submit" class="register-button" :loading="registerBtn" @click.stop.prevent="handleSubmit" :disabled="registerBtn">Register
      </a-button>
      <router-link class="login" :to="{ name: 'Login' }">Login to an existing account</router-link>
    </a-form-item>

  </a-form>
</div>
</template>

<script>
import {
  timeFix
} from '@/utils/util'
import {
  register
} from '../api/api'

const levelClass = {
  0: 'error',
  1: 'error',
  2: 'warning',
  3: 'success'
}
export default {
  name: 'Register',
  components: {},
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
        callback(new Error('Please include at least two out of following: letters, numbers, and symbols.'))
      }
    },
    handlePasswordCheck (rule, value, callback) {
      const password = this.form.getFieldValue('password')
      console.log('value', value)
      if (value === undefined) {
        callback(new Error('Please enter the password.'))
      }
      if (value && password && value.trim() !== password.trim()) {
        callback(new Error('Password entries do not match.'))
      }
      callback()
    },
    handlePasswordInputClick () {
      if (!this.isMobile()) {
        this.state.passwordLevelChecked = true
        return
      }
      this.state.passwordLevelChecked = false
    },
    handleSubmit () {
      console.log('Request submitted.')
      const {
        form: {
          validateFields
        },
        state
      } = this
      validateFields({
        force: true
      }, (err, values) => {
        console.log('Request validated.')
        if (!err) {
          state.passwordLevelChecked = false
          console.log(values)
          const registerParams = {
            ...values
          }
          delete registerParams.password2
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
      this.$router.push({
        path: '/hello/login'
      })
      setTimeout(() => {
        this.$notification.success({
          message: 'Welcome',
          description: `${timeFix()}, you are successfully registered!`
        })
      }, 1000)
      this.isLoginError = false
    },
    requestFailed (err) {
      this.$notification.error({
        message: 'Error',
        description: ((err.response || {}).data || {}).message || 'Your request was rejected. Please try again later.',
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
<style lang="less">
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
</style>
<style lang="less" scoped>
.user-layout-register {
    & > h3 {
        font-size: 16px;
        margin-bottom: 20px;
    }
    .register-button {
        width: 50%;
        float: left;
    }
    .login {
        float: right;
        line-height: 40px;
    }
}
</style>
