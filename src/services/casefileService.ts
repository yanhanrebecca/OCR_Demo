// import api from './api';
//
// // 定义上传图片的函数
// export const uploadImage = async (caseId: number, file: File): Promise<any> => {
//   const formData = new FormData();
//   formData.append('file', file);
//
//   try {
//     const response = await api.post(`/casefile/${caseId}/results`, formData, {
//       headers: {
//         'Content-Type': 'multipart/form-data',
//       },
//     });
//     return response.data;  // 返回后端的响应数据
//   } catch (error) {
//     console.error('Error uploading file', error);
//     throw error;
//   }
// };
