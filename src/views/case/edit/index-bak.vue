<template>
  <div class="edit-container">
    <div class="edit-left">
      <!-- 按钮部分 -->
      <div class="button-container">
        <div class="top-buttons">
          <button @click="selectCheckImage">检材</button>
          <button @click="selectSampleImage">样本</button>
          <button @click="cutIdentify">切分识别</button>
        </div>

        <div class="bottom-buttons">
          <button @click="uploadCheckImage" :disabled="!checkImage">上传检材</button>
          <button @click="uploadSampleImage" :disabled="!sampleImage">上传样本</button>
        </div>
      </div>
      <form :action="uploadUrl" method="post" enctype="multipart/form-data">
      <!-- 隐藏的文件输入框，用于选择检材和样本图片 -->
      <input type="file" name="image" ref="checkImageInput" @change="displayCheckImage" style="display:none" />
<!--      <input type="file" name="image" ref="sampleImageInput" @change="displaySampleImage" style="display:none" />-->
      </form>


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
      <!-- 识别结果部分 -->
      <div v-if="Object.keys(results).length">
        <h4>识别结果：</h4>
        <div class="folder-container">
          <div v-for="(images, folderName) in results" :key="folderName" class="folder-item">
            <h5 @click="toggleFolder(`${folderName}`)" class="folder-name">
              📁 {{ folderName }}
            </h5>
            <div v-if="openedFolders.includes(`${folderName}`)" class="images-in-folder">
              <div v-for="(image, index) in images" :key="index" class="result-item">
                <a :href="image" target="_blank">
                  <img :src="image" alt="识别结果" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <p>无识别结果，请点击切分识别。</p>
      </div>
    </div>

    <div class="edit-right">右</div>
  </div>
</template>



<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router'
const route= useRoute();
const caseId = route.params.id as string;
const uploadUrl=ref(`http://localhost:8080/uploaded/${caseId}/add`)
const checkImage = ref<File | null>(null); // 检材图片的 File 对象
const sampleImage = ref<File | null>(null); // 样本图片的 File 对象

const checkImagePreview = ref<string | undefined>(undefined);  // 用于预览的 URL
const sampleImagePreview = ref<string | undefined>(undefined);  // 用于预览的 URL

const results = ref<{ [key: string]: string[] }>({});
const openedFolders = ref<string[]>([]);

const checkImageInput = ref<HTMLInputElement | null>(null);
const sampleImageInput = ref<HTMLInputElement | null>(null);

// 选择检材图片
const selectCheckImage = () => {
  checkImageInput.value?.click();
};

// 展示检材图片
const displayCheckImage = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    checkImage.value = file;
    checkImagePreview.value = URL.createObjectURL(file); // 生成预览 URL
  }
};

// 选择样本图片
const selectSampleImage = () => {
  sampleImageInput.value?.click();
};

// 展示样本图片
const displaySampleImage = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    sampleImage.value = file;
    sampleImagePreview.value = URL.createObjectURL(file); // 生成预览 URL
  }
};

// 点击按钮，上传检材图片的函数
const uploadCheckImage = async () => {
  if (!checkImage.value) {
    alert('请先选择检材图片');
    return;
  }

  const formData = new FormData();
  formData.append('checkImage', checkImage.value);

  try {
    const response = await fetch(`http://localhost:8080/${checkImage.value}/add`, {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      console.log('检材图片上传成功');
    } else {
      console.error('检材图片上传失败:', response.statusText);
    }
  } catch (error) {
    console.error('检材图片上传出错:', error);
  }
};

// 上传样本图片的函数
const uploadSampleImage = async () => {
  if (!sampleImage.value) {
    alert('请先选择样本图片');
    return;
  }

  const formData = new FormData();
  formData.append('sampleImage', sampleImage.value);

  try {
    const response = await fetch('/api/upload-sample-image', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      console.log('样本图片上传成功');
    } else {
      console.error('样本图片上传失败:', response.statusText);
    }
  } catch (error) {
    console.error('样本图片上传出错:', error);
  }
};

// 切分识别的函数（只负责调用后端处理）
const cutIdentify = async () => {
  try {
    const response = await fetch('/api/cut-identify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({}),
    });

    if (response.ok) {
      const data = await response.json();
      results.value = data.results; // 假设返回识别结果
    } else {
      console.error('识别失败:', response.statusText);
    }
  } catch (error) {
    console.error('请求出错:', error);
  }
};

// 切换文件夹显示
const toggleFolder = (folderName: string) => {
  if (openedFolders.value.includes(folderName)) {
    openedFolders.value = openedFolders.value.filter(name => name !== folderName);
  } else {
    openedFolders.value.push(folderName);
  }
};
</script>


<style scoped lang="scss">
.edit-container {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: row;
  column-gap: 70px;

  .edit-left {
    width: 300px;
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
    width: 300px;
    background-color: blue;
  }
}
</style>

