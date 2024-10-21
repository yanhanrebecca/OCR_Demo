import {ref, computed} from 'vue'
import {defineStore} from 'pinia'

export const useAuthStore = defineStore('auth', () => {
    const token = ref(localStorage.getItem('Authorization') as string | null)
    const uid = ref(localStorage.getItem('uid') as string | null)
    const nickName = ref(localStorage.getItem('nickName') as string | null)
    const userPhoto = ref(localStorage.getItem('userPhoto') as string | null)
    const getToken = () => {
        return token.value
    }
    const setToken = (value: string) => {
        localStorage.setItem('Authorization', value)
        token.value = value
    }
    const removeToken = () => {
        localStorage.removeItem('Authorization')
        token.value = ''
    }
    const getUid = () => {
        return uid.value
    }
    const setUid = (value: string) => {
        localStorage.setItem('uid', value)
        uid.value = value
    }
    const removeUid = () => {
        localStorage.removeItem('uid')
        uid.value = ''
    }
    const getNickName = () => {
        return nickName.value
    }
    const setNickName = (value: string) => {
        localStorage.setItem('nickName', value)
        nickName.value = value
    }
    const removeNickName = () => {
        localStorage.removeItem('nickName')
        nickName.value = ''
    }
    //退出登录
    const logout = () => {
        removeToken()
        removeUid()
        removeNickName()
        removeUserPhoto()
    }
    const setUserPhoto = (value: string) => {
        localStorage.setItem('userPhoto', value)
        userPhoto.value = value
    }
    const getUserPhoto = () => {
        return userPhoto.value
    }
    const removeUserPhoto = () => {
        localStorage.removeItem('userPhoto')
        userPhoto.value = ''
    }
    return {
        token,
        uid,
        nickName,
        getToken,
        setToken,
        removeToken,
        getUid,
        setUid,
        removeUid,
        getNickName,
        setNickName,
        removeNickName,
        logout,
        userPhoto,
        setUserPhoto,
        getUserPhoto,
        removeUserPhoto
    }
})