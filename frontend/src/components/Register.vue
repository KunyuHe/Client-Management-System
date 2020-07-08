<template>
<div class="main user-layout-register">
  <a-form ref="formRegister" :form="form" id="formRegister">
    <a-form-item>
      <a-input
        size="large"
        type="text"
        placeholder="用户名"
        v-decorator="['name',
                      {rules: [{ required: true,
                                 message: '请输入用户名！' }],
                      validateTrigger: ['blur']}]">
      </a-input>
    </a-form-item>

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
      <a-input-password
        size="large"
        placeholder="密码"
        @click="handlePasswordInputClick"
        v-decorator="['password',
                      {rules: [{ required: true,
                                 message: '至少6位，区分大小写！'},
                               { validator: this.handlePasswordLevel }],
                      validateTrigger: ['change', 'blur']}]">
      </a-input-password>
    </a-form-item>

    <a-form-item>
      <a-input-password
      size="large"
      placeholder="确认密码"
      v-decorator="['password2',
                    {rules: [{ required: true,
                               message: '请再次输入密码！' },
                             { validator: this.handlePasswordCheck }],
                     validateTrigger: ['change', 'blur']}
                   ]">
      </a-input-password>
    </a-form-item>

    <a-form-item>
      <a-button
        size="large"
        type="primary"
        htmlType="submit"
        class="register-button"
        :loading="registerBtn"
        :disabled="registerBtn"
        @click.stop.prevent="handleSubmit"
      >
        注册
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
      if (/[0-9]/.test(value)) {
        level++
      }
      if (/[a-zA-Z]/.test(value)) {
        level++
      }
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
        callback(new Error('请至少包括以下中的两种：字母，数字和符号。'))
      }
    },

    handlePasswordCheck (rule, value, callback) {
      const password = this.form.getFieldValue('password')
      if (value === undefined) {
        callback(new Error('Please enter the password.'))
      }
      if (value && password && value.trim() !== password.trim()) {
        callback(new Error('Password entries do not match.'))
      }
      callback()
    },

    handlePasswordInputClick () {
      this.state.passwordLevelChecked = false
    },

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
          state.passwordLevelChecked = false
          const registerParams = {
            ...values
          }
          delete registerParams.password2
          register(registerParams)
            .then((res) => {
              if (res.data.code !== 0) {
                return this.$message.error(res.data.msg)
              } else {
                this.registerSuccess(res)
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

    registerSuccess (res) {
      this.$router.push({
        path: '/hello/login'
      })
      setTimeout(() => {
        this.$notification.success({
          message: '欢迎',
          description: `${timeFix()}，您已成功注册！`
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
      this.registerBtn = false
    }
  },
  watch: {
    'state.passwordLevel' (val) {
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
