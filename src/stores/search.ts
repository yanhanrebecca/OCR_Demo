import {defineStore} from "pinia";
import {computed, ref} from "vue";

export const useSearchStore = defineStore('search', () => {
    const keyword = ref('')

    function getSerachKey() {
        return keyword.value
    }

    function setSerachKey(key: string) {
        keyword.value = key
    }

    return {
        keyword,
        getSerachKey,
        setSerachKey
    }
})
