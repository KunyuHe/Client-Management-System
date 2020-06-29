<template>
    <div>
        <h1>用户{{username}}找回密码</h1>
        <p>待开发</p>
    </div>
</template>

<script>
export default {
  data () {
    return {
      username: ''
    }
  },
  created () {
    this.username = this.$route.query.username
  }
}
</script>
