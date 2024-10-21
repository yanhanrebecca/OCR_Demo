<script setup lang="ts">
  import left from '@/assets/images/left@2x.png'
  import SvgIcon from '@/components/icons/SvgIcon.vue'
  import { useRouter } from 'vue-router'
  var router = useRouter()
  const goHome = () => {
    router.push('/home')
  }
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-intro">
        <img :src="left" alt="登录背景" />
      </div>
      <div class="login-form">
        <div class="form-title">
          <span>文件笔迹智能鉴定系统</span>
        </div>
        <div class="form-tag">
          <div></div>
          <span>身份认证</span>
          <div></div>
        </div>
        <div class="form-input">
          <el-form>
            <el-form-item>
              <el-input placeholder="请输入账号">
                <template #prefix>
                  <svg-icon name="dl-yonghuming"/>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-input placeholder="请输入密码">
                <template #prefix>
                  <svg-icon name="dl-mima"/>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-checkbox label="记住密码" name="type"></el-checkbox>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="large" @click="goHome">登录</el-button>
            </el-form-item>
          </el-form>

        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
//  设置背景图片
.login-container {
  /* 设置容器为弹性盒子布局，平均分布元素在水平方向和垂直方向上 */
  display: flex;
  /* 平均分布元素在水平方向上 */
  justify-content: space-evenly;
  /* 平均分布元素在垂直方向上 */
  align-items: center;
  /* 设置容器高度为视口高度 */
  height: 100vh;
  /* 设置背景图片，不重复，并覆盖整个容器 */
  background: url('@/assets/images/dl-bg@2x.png') no-repeat;
  background-size: cover;
  .login-card {
    //卡片效果
    /*设置阴影*/
    box-shadow: 2px 5px 4px rgba(227, 237, 251);
    /*设置圆角*/
    border-radius: 15px;
    /*设置背景颜色*/
    background-color: #ffffff;
    /*设置布局方式*/
    display: flex;
    /*设置卡片高度*/
    height: 75%;
    /*设置卡片宽度*/
    width: 80%;
    .login-intro {
      flex: 1;
      /*设置圆角角度*/
      border-radius: 50px;
      img {
        width: 100%;
        height: 100%;
        display: block; /* 新增这一行，设置图片为块级元素，独占一行 */
      }
    }
    .login-form {
      flex: 1;
      display: flex;
      /*设置布局方向*/
      flex-direction: column;
      justify-content: flex-start;
      /*设置水平对齐方式*/
      align-items: center;
      .form-title {
        padding: 30px 0;
        font-size: 30px;
        color: #0059cb;
      }
      .form-tag {
        display: flex;
        flex-direction: row;
        align-items: center;
        > div {
          width: 120px;
          height: 2px;
          background-color: black;
          margin: 10px 30px;
        }
        padding: 0 0 50px 0;
        font-size: 20px;
        color: #011f3a;
        font-weight: 550;
      }
      .form-input {
        display: flex;
        flex-direction: column;
        align-items: center;
        :deep(.el-input__wrapper) {
          //background-color: transparent;/*覆盖原背景颜色，设置成透明 */
          border-radius: 95px;
          border: 0;
          height: 50px;
          width: 450px;
        }
        //设置按钮大小
        :deep(.el-button) {
          width: 100%;
          height: 50px;
          border-radius: 95px;
          font-size: 20px;
          font-weight: 550;
          color: #ffffff;
          background-color: #0059cb;
          border: 0;
          margin: 30px 0 0 0;
        }
        //设置按钮hover样式
        :deep(.el-button:hover) {
          background-color: #004099;
        }
      }
    }
  }
}
</style>
