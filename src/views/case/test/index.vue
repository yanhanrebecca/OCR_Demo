<template>
  <div v-if="folder">
    <h3>{{ folder.folderName }}</h3>
    <button @click="toggleShowContent">查看内容</button>

    <div v-if="showContent">
      <ul>
        <li v-for="image in folder.images" :key="image">
          <img :src="getImageUrl(image)" :alt="image" @click="viewImage(image)" class="thumbnail" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ElLoading } from 'element-plus'
// 用于存储后端返回的数据
const folder = ref(null);
const showContent = ref(false);

// 从后端API获取图片数据
const fetchImagesFolder = async () => {
  try {
    const response = await fetch('/api/get-images-folder');
    if (response.ok) {
      folder.value = await response.json();
    } else {
      console.error('Error fetching folder data');
    }
  } catch (error) {
    console.error('Fetch error:', error);
  }
};

// 构造图片的URL
const getImageUrl = (image) => {
  return `/path_to_folder/${folder.value.folderName}/${image}`;
};

// 切换显示图片内容
const toggleShowContent = () => {
  showContent.value = !showContent.value;
};

// 查看单个图片（此处可以扩展成查看大图功能）
const viewImage = (image) => {
  console.log(`查看图片: ${image}`);
};

// 组件加载时从后端获取数据
onMounted(() => {
  ElLoading.service({fullscreen:true})
  fetchImagesFolder();
});
</script>

<style scoped>
.thumbnail {
  width: 150px;
  height: 150px;
  object-fit: cover;
  margin: 10px;
  cursor: pointer;
}
</style>
