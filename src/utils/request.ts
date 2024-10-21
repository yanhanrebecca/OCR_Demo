import axios, {type AxiosInstance} from 'axios';
import {ElMessage} from 'element-plus';
// import { useAuthStore } from '@/utils/auth';

const axiosInstance: AxiosInstance = axios.create({
    baseURL: '/api',
    timeout: 60000,
    headers: {
        'Content-Type': 'application/json'
    }
});

axiosInstance.interceptors.response.use(
  (response) => {
      if (response.status !== 200) {
          ElMessage.error('服务端异常！');
          return Promise.reject(response);
      }
      const {code, message} = response.data;
      console.log(typeof response.data, response.data)
      if (typeof response.data === 'object') {
          if (code !== 20000) {
              if (message) {
                  ElMessage.error(message);
              }
              // 登录已过期
              if (code === 'A0230') {
                  // 移除 token
                  // const authStore = useAuthStore();
                  // authStore.removeToken();
                  // authStore.removeNickName();
                  // authStore.removeUid();
                  // router.push({ path: '/login' });
              }
              return Promise.reject(response.data);
          }
      }
      return response.data;
  },
  (error) => {
      ElMessage.error('网络异常！');
      return Promise.reject(error);
  }
);

export default axiosInstance;
