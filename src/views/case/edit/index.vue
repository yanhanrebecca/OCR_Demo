<template>
  <div class="edit-container">
    <div class="edit-left">
      <!-- 按钮部分 -->
      <div class="button-container">
        <div class="top-buttons">
          <button @click="selectCheckImage">检材</button>
          <button @click="selectSampleImage">样本</button>
<!--          <button @click="cutIdentify">切分识别</button>-->
        </div>

        <div class="bottom-buttons">
          <button @click="uploadCheckImage" :disabled="!checkImage">上传检材</button>
          <button @click="uploadSampleImage" :disabled="!sampleImage">上传样本</button>
        </div>
      </div>

        <!-- 隐藏的文件输入框，用于选择检材和样本图片 -->
        <input
          type="file"
          name="image"
          ref="checkImageInput"
          @change="displayCheckImage"
          style="display: none"
        />
        <input
          type="file"
          name="image"
          ref="sampleImageInput"
          @change="displaySampleImage"
          style="display: none"
        />
      <!-- 图片预览部分 -->
      <div v-if="checkImage" class="image-preview">
        <h4>检材图片预览：</h4>
        <img :src="checkImagePreview" alt="检材" />
      </div>

      <div v-if="sampleImage" class="image-preview">
        <h4>样本图片预览：</h4>
        <img :src="sampleImagePreview" alt="样本" />
      </div>
    </div>


    <div class="edit-center">
      <!-- 1、检材、样本处理后的结果展示-->
      <!-- （1）、文件夹按钮 -->
      <div v-if="folders.length > 0">
        <h3>文件夹列表</h3>
        <ul>
          <li v-for="(folder, index) in folders" :key="index">
            <button @click="fetchImages(folder, index)">查看 {{ folder }}</button>
          </li>
        </ul>
      </div>
      <!-- （2）、图片展示 -->
      <div v-if="images.length > 0">
        <h3>图片列表</h3>
        <div v-for="(image, index) in images" :key="index">
          {{ image }}
          <img :src="image" :alt="'Image ' + index" style="max-width: 200px; height: auto;" />
        </div>
      </div>

      <!--  2、二维识别图片展示  -->
      <!--   （1）、创建按钮，点击能够显示图片   -->
      <div v-if="folders2D.length > 0">
        <h3>---------------------------------------------------------------</h3>
        <h3>二维识别结果</h3>
        <<ul>
          <li v-for="(folder2D, index) in folders2D" :key="index">
              <button @click="fetch2DImages(folder2D, index)">查看： {{ folder2D }}</button>
          </li>
        </ul>
      </div>
      <!--  （2）、展示二维处理后的图片  -->
      <div v-if="images2D.length > 0">
        <h3>图片二维识别</h3>
        <div v-for="(image2D, index) in images2D" :key="index">
          {{ image2D }}
          <img :src="image2D" :alt="'Image2D ' + index" style="max-width: 200px; height: auto;" />
        </div>
      </div>
    </div>


    <div class="edit-right">
      <div class="function-button-1">
        <button @click="image2DProcess">二维识别</button>
        <button @click="image3DProcess">三维识别</button>
      </div>
      <div class="function-button-2">
        <button @click="image4DProcess">四维识别</button>
        <button @click="imageColoring">着色</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute } from 'vue-router'
import { getFolderImage, getFolderName, get2DImage, upload2DImage, uploadImage } from "@/api/case";
import { ElLoading, ElMessage } from "element-plus";

const route = useRoute()

// 定义 caseId（可以动态获取）
let caseId = route.params.id as string
const uploadUrl = ref(`http://localhost:8080/uploaded/${caseId}/add`)

const checkImage = ref<File | null>(null) // 检材图片的 File 对象
const sampleImage = ref<File | null>(null) // 样本图片的 File 对象

const checkImagePreview = ref<string | undefined>(undefined) // 用于预览的 URL
const sampleImagePreview = ref<string | undefined>(undefined) // 用于预览的 URL

const checkImageInput = ref<HTMLInputElement | null>(null)
const sampleImageInput = ref<HTMLInputElement | null>(null)

// 响应式数据
const folders = ref([])  // 存放文件夹名
const images = ref([])   // 存放当前文件夹的图片路径
const folders2D = ref([]) // 存放二维识别后的文件夹名
const images2D = ref([]) // 存放二维识别后的图片路径

let temp:any
//页面加载直接执行
// onMounted(async ()=>{
  //获取当前案件对应文件夹列表
//   await fetchFolderName(caseId)
// })

/*  1、选择本机图片，并对图片进行剪切   */
//  （1）选择检材图片
const selectCheckImage = () => {
  checkImageInput.value?.click()
}
//  （2）展示检材图片
const displayCheckImage = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    checkImage.value = file
    checkImagePreview.value = URL.createObjectURL(file) // 生成预览 URL
  }
}
//  （3）选择样本图片
const selectSampleImage = () => {
  sampleImageInput.value?.click()
}
//  （4）展示样本图片
const displaySampleImage = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    sampleImage.value = file
    sampleImagePreview.value = URL.createObjectURL(file) // 生成预览 URL
  }
}
//  （5）点击按钮，上传检材图片的函数
const uploadCheckImage = async () => {
  if (!checkImage.value) {
    alert('请先选择检材图片')
    return
  }
  const formData = new FormData()
  formData.append('image', checkImage.value)
  try{
    const res =await uploadImage(caseId,formData)
    //提示上传成功
    ElMessage.success('检材图片上传成功')
    //清除缩略图
    checkImage.value = null

    // 上传成功后获取处理后的文件夹
    // await fetchFolderName(caseId)
  }catch (e) {
    //提示上传失败
    ElMessage.error('检材图片上传失败')
  }
}
//  （6）上传样本图片的函数
const uploadSampleImage = async () => {
  if (!sampleImage.value) {
    alert('请先选择样本图片')
    return
  }
  const formData = new FormData()
  formData.append('image', sampleImage.value)
  try{
    const res =await uploadImage(caseId,formData)
    temp = res
    //提示上传成功
    ElMessage.success('样本图片上传成功')
    //清除缩略图
    sampleImage.value = null
    // 上传成功后获取处理后的文件夹
    await fetchFolderName(caseId)
  }catch (e) {
    //提示上传失败
    ElMessage.error('样本图片上传失败')
  }
}
//  （7）从后端获取数据（获取文件夹名）
const fetchFolderName = async (caseId:any) => {
  try {
    // 调用 getFolderName 来获取数据
    const response = await getFolderName(caseId);
    // 返回的文件夹数组在 JSON 数据的 data 部分
    folders.value = response.data || [];
    // 返回文件夹名字
    // return folderName;
  }catch (error) {
    console.error('获取文件夹名失败:', error);
  }
};
//  （8）获取文件夹中的图片
const fetchImages = async (folder:any, index:any) => {
  // console.log(temp)
  const id = temp.data[index]
  try {
    // 调用 getFolderImage 来获取文件夹中的图片
    const response = await getFolderImage(id, caseId);
    console.log(response);
    // 返回的图片路径在 data 中
    let formateUrls = response.data.map(item => item.replace('localhost','192.168.2.168'))

    images.value = formateUrls || []
  } catch (error) {
    console.error('获取图片失败:', error);
  }
}

/*   2、剪切后图片的二维处理   */
//  （1）、将剪切后的图片传到后端，进行二维处理
const image2DProcess = async ()=>{
  try{
    const response = await upload2DImage(caseId);
    // 获取二维处理后的文件夹
    await fetch2DFolderName(caseId)
  }catch (error) {
    console.error('图片发送失败:', error);
  }
}
//  （2）、取出 JSON 中的 data 数据部分来作为文件夹的名字
const fetch2DFolderName = async (caseId:any) => {
  try {
    // 调用 getFolderName 来获取数据
    const response = await getFolderName(caseId);
    // 返回的文件夹数组在 JSON 数据的 data 部分
    folders2D.value = response.data || [];
    // 返回文件夹名字
    // return folderName;
  }catch (error) {
    console.error('获取文件夹名失败:', error);
  }
};
//  （3）、从文件夹中取出二维处理后图片
const fetch2DImages = async (folder2D:any, index:any) => {
  const id = temp.data[index]
  try {
    // 调用 getFolderImage 来获取文件夹中的图片
    const response = await get2DImage(caseId,id);
    console.log('***************************',caseId,id);
    // 返回的图片路径在 data 中
    let formateUrls = response.data.map(item => item.replace('localhost','192.168.2.168'))
    images2D.value = formateUrls || []
  } catch (error) {
    console.error('获取图片失败:', error);
  }项目
}


// 剪切图片的三维处理
const image3DProcess = async ()=>{}

// 剪切图片的四维处理
const image4DProcess = async ()=>{}

// 着色
const imageColoring = async ()=>{}


// 切分识别的函数（只负责调用后端处理）
// const cutIdentify = async () => {
//   try {
//     const response = await fetch('/api/cut-identify', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify({})
//     })
//
//     if (response.ok) {
//       const data = await response.json()
//       results.value = data.results // 假设返回识别结果
//     } else {
//       console.error('识别失败:', response.statusText)
//     }
//   } catch (error) {
//     console.error('请求出错:', error)
//   }
// }


// 切换文件夹显示
// const toggleFolder = (folderName: string) => {
//   if (openedFolders.value.includes(folderName)) {
//     openedFolders.value = openedFolders.value.filter((name) => name !== folderName)
//   } else {
//     openedFolders.value.push(folderName)
//   }
// }

</script>

<style scoped lang="scss">
.edit-container {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: row;
  column-gap: 30px;

  .edit-left {
    width: 350px;
    background-color: white;

    .button-container {
      display: flex;
      flex-direction: column; /* 垂直排列两行按钮 */

      .top-buttons {
        display: flex;
        justify-content: space-between; /* 让三个按钮均匀分布 */
        margin-bottom: 10px;

        button {
          flex: 1;
          margin: 0 5px;
          padding: 10px;
          font-size: 16px;
          background-color: white;
          border: 1px solid #ccc;
          cursor: pointer;

          &:hover {
            background-color: #f0f0f0;
          }
        }
      }

      .bottom-buttons {
        display: flex;
        justify-content: space-between; /* 让两个按钮在一行中均匀分布 */
        margin-bottom: 10px;

        button {
          flex: 1;
          margin: 0 5px;
          padding: 10px;
          font-size: 16px;
          background-color: white;
          border: 1px solid #ccc;
          cursor: pointer;

          &:hover {
            background-color: #f0f0f0;
          }
        }
      }
    }

    .image-preview {
      margin-top: 10px;

      img {
        max-width: 100%;
        height: auto;
        border: 1px solid #ccc;
        border-radius: 5px;
      }
    }
  }

  .edit-center {
    ul {
      list-style: none;
      padding: 0;
    }

    li {
      margin-bottom: 10px;
    }

    button {
      margin-right: 10px;
    }

    img {
      border: 1px solid #ccc;
      padding: 10px;
      margin-top: 10px;
    }

    flex: 1;
    background-color: white;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;

    .folder-container {
      margin-top: 10px;

      .folder-item {
        margin-top: 10px;

        .folder-name {
          cursor: pointer;
          font-weight: bold;
          margin-bottom: 5px;
        }

        .images-in-folder {
          display: flex;
          flex-wrap: wrap;

          .result-item {
            margin: 5px;

            img {
              max-width: 100px;
              height: auto;
              border: 1px solid #ccc;
              border-radius: 5px;
            }
          }
        }
      }
    }
  }

  .edit-right {
    width: 350px;
    background-color: white;

    .function-button-1{
      display: flex;
      justify-content: space-between; /* 让2个按钮均匀分布 */
      margin-bottom: 10px;

      button {
        flex: 1;
        margin: 0 5px;
        padding: 10px;
        font-size: 16px;
        background-color: white;
        border: 1px solid #ccc;
        cursor: pointer;

        &:hover {
          background-color: #f0f0f0;
        }
      }
    }

    .function-button-2{
        display: flex;
        justify-content: space-between; /* 让2个按钮均匀分布 */
        margin-bottom: 10px;

        button {
          flex: 1;
          margin: 0 5px;
          padding: 10px;
          font-size: 16px;
          background-color: white;
          border: 1px solid #ccc;
          cursor: pointer;

          &:hover {
            background-color: #f0f0f0;
          }
        }
    }
  }
}
</style>
