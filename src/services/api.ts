// import axios from 'axios';
//
// // 创建一个 Axios 实例，方便管理 baseURL 和其他配置
// const api = axios.create({
//   baseURL: 'http://localhost:8080',  // 根据后端的实际 URL 配置
//   timeout: 10000,  // 请求超时时间，单位是毫秒
//   headers: {
//     'Content-Type': 'application/json',
//   },
// });
//
// // 拦截器：可以在请求或响应被处理之前进行一些操作
// api.interceptors.request.use(
//   config => {
//     // 在请求之前进行操作，例如附加 Token 等
//     return config;
//   },
//   error => {
//     return Promise.reject(error);
//   }
// );

// api.interceptors.response.use(
//   response => {
//     return response;
//   },
//   error => {
//     // 处理错误响应，例如 token 过期处理等
//     return Promise.reject(error);
//   }
// );
//
// export default api;
