import {defineStore} from "pinia";
import {ref} from "vue";
import {useRoute, useRouter} from "vue-router";

export const useNavbarStore = defineStore('navbar', () => {
    const router = useRouter();
    //获取当前路由的name
    const activeIndex = ref('/home')
    const setActiveIndex = (path: string) => {
        activeIndex.value = path
    }
    const getActiveIndex = () => {
        return activeIndex.value
    }
    return {
        activeIndex,
        setActiveIndex,
        getActiveIndex
    }
})