<template>
  <div class="case-item">
    <!-- 显示案件的测试图片 -->
    <div class="case-image">
      <img :src="test" alt="案件图片" />
    </div>

    <!-- 根据案件的类型显示不同的图标和案件名称 -->
    <div v-if="item.type == 0" class="case-type">
      <img :src="ajgl_jpeg" alt="jpeg图标" />
      {{ item.title }}
    </div>
    <div v-if="item.type == 1" class="case-type">
      <img :src="ajgl_png" alt="png图标" />
      {{ item.title }}
    </div>
    <div v-else class="case-type">
      <img :src="ajgl_word" alt="word图标" />
      {{ item.title }}
    </div>

    <!-- 编辑和删除按钮 -->
    <div class="case-actions">
      <span class="edit" @click="handleEdit(item.id)">编辑</span>
      <span class="divider"></span>
      <span class="delete" @click="handleDelete(item.id)">删除</span>
    </div>
  </div>
</template>

<script lang="ts" setup>
//import { defineProps } from 'vue'
import test from '@/assets/images/test.jpg'
import ajgl_jpeg from '@/assets/images/ajgl-jpeg@2x.png'
import ajgl_png from '@/assets/images/ajgl-png@2x.png'
import ajgl_word from '@/assets/images/ajgl-word@2x.png'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { del } from '@/api/case'
// 使用 Vue Router
const router = useRouter()
// 定义 props 用来接收案件数据和图片资源
const props = defineProps<{
  item: {
    id: number
    title: string
    description: string
    type: number
  }
}>()

// 处理编辑操作
const handleEdit = (id:any) => {
  router.push(`/edit/${id}`)
}

// 处理删除操作
const handleDelete = (id:any) => {
  //elementui确认是否删除
  ElMessageBox.confirm('确定删除该案件吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      // 删除操作
      console.log('删除案件', id)
      try {
        const res = await del(id)
        ElMessage({
          type: 'success',
          message: '删除成功!'
        })
      }catch (e) {
        ElMessage({
          type: 'warning',
          message: '删除失败!'
        })
      }

    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '已取消删除'
      })
    })
}
</script>

<style scoped>
/* 设置案件显示的样式 */
.case-item {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 20px;
  margin: 10px;
  width: 200px;
  text-align: center;
}

.case-image img {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.case-type {
  margin-top: 10px;
  font-size: 16px;
}

.case-type img {
  width: 20px;
  height: 20px;
  margin-right: 10px;
}

.case-actions {
  margin-top: 10px;
}

.edit,
.delete {
  cursor: pointer;
  color: blue;
}

.divider {
  display: inline-block;
  width: 1px;
  height: 20px;
  background-color: #ccc;
  margin: 0 10px;
}
</style>
