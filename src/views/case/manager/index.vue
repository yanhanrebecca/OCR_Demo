<template>
  <div class="manager-container">
    <div class="manager-search">
      <el-input placeholder="请输入文件名称搜索">
        <template #prefix>
          <el-icon>
            <search />
          </el-icon>
        </template>
      </el-input>
    </div>

    <!-- 这个区域展示案件以及新建案件按钮 -->
    <div class="manager-content">
      <!-- 新建案件框，和案件框大小保持一致 -->
      <div class="case-item add-case" @click="createNewCase">
        <i>+</i>
        <span>新建案件</span>
      </div>

      <!-- 显示现有案件 -->
      <CaseItem v-for="item in caseList" :key="item" :item="item" />
    </div>
    <!--添加一个表单对话框-->
    <el-dialog v-model="dialogFormVisible" title="Shipping address" width="500">
      <el-form :model="form">
        <el-form-item label="Promotion name" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Zones" :label-width="formLabelWidth">
          <el-select v-model="form.region" placeholder="Please select a zone">
            <el-option label="Zone No.1" value="shanghai" />
            <el-option label="Zone No.2" value="beijing" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogFormVisible = false">关闭</el-button>
          <el-button type="primary" @click="dialogFormVisible = false"> 添加 </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import CaseItem from '@/views/case/manager/case-item.vue'
import { list } from '@/api/case'
// 使用 Vue Router
const router = useRouter()
//等我一下
// 创建案件列表
const caseList = ref([
  // { id: 1, name: '案件名称1', type: 0 },
  // { id: 2, name: '案件名称2', type: 1 },
  // { id: 3, name: '案件名称3', type: 2 }
  // {
  //   "id": -1294606334,
  //   "title": "案件1",
  //   "description": "案件1",
  //   "createdAt": null
  // },
  // {
  //   "id": 1930739714,
  //   "title": "案件2",
  //   "description": "案件2",
  //   "createdAt": "2024-09-25T18:35:09.449923"
  // }
])
//设置对话框属性
const dialogFormVisible = ref(false)
// 创建表单数据
const form = ref({
  name: '',
  region: '',
  date1: '',
  date2: '',
  delivery: false,
  type: [],
  resource: '',
  desc: ''
})
const formLabelWidth = '140px'

// 点击案件项，跳转到案件详情页面
const goToCaseDetail = (id: number) => {
  router.push(`/case/${id}`)
}

// 跳转到新建案件的页面
const createNewCase = () => {
  // router.push('/create')
  dialogFormVisible.value = true
}
const getCaseList = async () => {
  const res = await list()
  caseList.value = res.data
  console.log(res)
}
onMounted(async () => {
  await getCaseList()
})
</script>

<style scoped>
.manager-container {
  padding: 20px;
}

.manager-search {
  margin-bottom: 20px;
}

.manager-content {
  display: flex;
  flex-wrap: wrap;
}

/* 案件项以及新建案件项的样式 */
.case-item {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 20px;
  margin: 10px;
  width: 200px;
  height: 250px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  text-align: center;
  cursor: pointer;
}

.case-item i {
  font-size: 40px;
  color: blue;
}

.case-item span {
  margin-top: 10px;
  font-size: 18px;
  color: black;
}

/* 特别针对新建案件框设置的样式 */
.add-case {
  background-color: #f0f0f0;
}

.add-case:hover {
  background-color: #e0e0e0;
}
</style>
