<script setup lang="ts">
import { ref, onMounted } from 'vue'
import SvgIcon from '@/components/icons/SvgIcon.vue'
import { Check, CircleCheck, CirclePlus, CirclePlusFilled, Plus } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const menuList = ref([
  {
    index: 0,
    name: '案件管理',
    path: '/manager' // 案件管理页面
  },
  {
    index: 1,
    name: '鉴定流程',
    path: '/manager2' // 笔迹鉴定页面
  },
  {
    index: 2,
    name: '鉴定结果',
    path: '/manager3' // 鉴定结果页面
  },
  {
    index: 3,
    name: '测试页面',
    path: '/test' // 用户管理页面
  }
])
const changeActive = (index: number) => {
  activeIndex.value = index
  router.push(menuList.value[index].path)
}
const activeIndex = ref(0)
onMounted(() => {
  // 开始直接选中第一项菜单
  changeActive(0)
})
</script>

<template>
  <div class="home-container">
    <div class="home-nav">
      <div class="home-logo">
        <span>文件笔迹智能鉴定系统</span>
      </div>
      <div class="home-menu">
        <!--导航栏内容-->
        <ul>
          <li
            v-for="(item, index) in menuList"
            :key="index"
            @click="changeActive(index)"
            :class="{ active: activeIndex === item.index }"
          >
            {{ item.name }}
          </li>
        </ul>
      </div>
      <div class="home-user">
        <!--  管理员/用户登录功能  -->
        <span><svg-icon name="nav-yonghuming" /></span>
        <!--  人物标志  -->
        <el-dropdown trigger="click">
          <span class="el-dropdown-link">
            admin<el-icon class="el-icon--right"><arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item :icon="Plus">Action 1</el-dropdown-item>
              <el-dropdown-item :icon="CirclePlusFilled"> Action 2</el-dropdown-item>
              <el-dropdown-item :icon="CirclePlus">Action 3</el-dropdown-item>
              <el-dropdown-item :icon="Check">Action 4</el-dropdown-item>
              <el-dropdown-item :icon="CircleCheck">Action 5</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
    <div class="home-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<style scoped lang="scss">
.home-container {
  user-select: none;
  width: 100%;
  background-color: #eff1f5;
  height: 100vh;
  display: flex;
  flex-direction: column;

  .home-nav {
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 100%;
    height: 60px;
    background-color: #0059cb;

    .home-logo {
      padding: 0 120px 0 30px;

      span {
        font-size: 24px;
        color: #fff;
      }
    }

    .home-menu {
      height: 100%;

      ul {
        display: flex;
        flex-direction: row;
        align-items: center;
        height: 100%;

        li {
          height: 100%;
          line-height: 60px;
          padding: 0 20px;
          font-size: 16px;
          color: #fff;
          cursor: pointer;
        }

        li:hover {
          background-color: #fff;
          color: #0059cb;
        }

        .active {
          background-color: rgb(56, 120, 213);
        }
      }
    }

    .home-user {
      display: flex;
      margin-left: auto;
      padding-right: 30px;
      align-items: center;

      span {
        font-size: 13px;
        color: #fff;
        padding-right: 10px;
      }

      /*向下箭头的样式*/
      .el-dropdown-link {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }

      .el-icon--right {
        margin-top: 0px;
      }
    }
  }

  .home-content {
    box-sizing: border-box;
    flex: 1;
    width: 100%;
  }
}
</style>