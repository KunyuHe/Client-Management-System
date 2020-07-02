<template>
<div class="main user-layout-recover">
  <h2>Password Recovery</h2>
  <a-form ref="formRecover" :form="form" id="formRecover">

    <a-form-item>
      <a-input size="large" type="text" placeholder="Email" v-decorator="['email', {rules: [{ required: true, type: 'email', message: 'Please enter a valid email address.' }], validateTrigger: ['change', 'blur']}]"></a-input>
    </a-form-item>

    <a-form-item>
      <a-button size="large" type="primary" htmlType="submit" class="recover-button" :loading="recoverBtn" @click.stop.prevent="handleSubmit" :disabled="recoverBtn">Send Email
      </a-button>
      <router-link class="login" :to="{ name: 'Login' }">Login to an existing account</router-link>
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
          console.log(values)
          const recoverParams = {
            ...values
          }
          console.log(recoverParams)
          recover(recoverParams)
            .then((res) => this.recoverSuccess(res))
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
          message: 'Email Sent',
          description: `${timeFix()}, please check you email and login with the correct password.`
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
