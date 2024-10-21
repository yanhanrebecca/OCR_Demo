import request from '@/utils/request'

/*  1、案例处理  */
//  （1）、获取案例列表
export function list() {
  return request.get('/case/list');
}
//  （2）、删除案例
export function del(id: number) {
  return request.delete(`/case/delete/${id}`);
}
//  （3）、添加案例
export function add(data: any) {
  return request.post('/case/add', data);
}


/*  2、对图片进行剪切  */
//  （1）、上传图片
export function uploadImage(caseId:any,data: any) {
  return request.post(`/uploaded/${caseId}/add`, data,{headers: { 'Content-Type': 'multipart/form-data' }});
}
//  （2）、获取返回的文件夹名字
export function getFolderName(caseId:any) {
  return request.get(`/casefile/${caseId}/load`);
}
//  （3）、获取文件夹中的图片
export function getFolderImage(caseFileId:any,caseId:any) {
  return request.get(`/crop/${caseId}/${caseFileId}/load`);
}


/*  3、图片的二维处理  */
//  （1）、选取图片发往后端，进行二维处理
export function upload2DImage(caseId:any) {
  return request.post(`/two/add/${caseId}`);
}
//  （2）、从后端获取二维处理过的图片
export function get2DImage(caseId:any,caseFileId:any){
  return request.get(`/two/load/${caseId}/${caseFileId}`);
}

