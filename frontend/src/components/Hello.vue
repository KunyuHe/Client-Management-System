<template>
  <div class="hello">
    <a-layout>
      <a-layout-header></a-layout-header>
      <a-layout-content>
        <div class="helloBox">
            <div style="padding-bottom:50px">
                <img src="../assets/logo.png" alt="logo">
                <span class="title">客户管理系统（CMS）</span>
            </div>
          <router-view />
        </div>
      </a-layout-content>
      <a-layout-footer>客户管理系统（CMS）<br/>&copy;2020 中信证券股权衍生品业务线</a-layout-footer>
    </a-layout>
  </div>
</template>

<style lang="less" scoped>
.hello {
  height: 100%;
  .ant-layout {
    height: 100%;
    .ant-layout-header {
      background: rgb(240, 242, 245) !important;
    }
    .ant-layout-content {
      height: 100%;
      .helloBox {
        width: 400px;
        position: relative;
        left: 50%;
        top: 40%;
        transform: translate(-50%, -50%);
            img{
                vertical-align: top;
                padding-right: 20px;
                height: 60px;
        }
        .title{
            display: inline-block;
            height: 60px;
            line-height: 60px;
            font-size: 30px;
            font-family: Avenir,Helvetica Neue,Arial,Helvetica,sans-serif;
            font-weight: 600;
        }
      }
    }
  }
}
</style>
