// TypeScript 版本，已移除 jQuery 和其他非标准 JavaScript 语言特性

export const goToAnchor = (id: string) => {
    const anchor = document.getElementById(id);
    if (anchor) {
        window.scrollTo({
            top: anchor.offsetTop,
            behavior: 'smooth',
        });
    }
}

export const getQueryObject = (url: string | null | undefined): Record<string, string> => {
    url = url ?? window.location.href;
    const search = url.substring(url.lastIndexOf('?') + 1);
    const obj: Record<string, string> = {};
    const reg = /([^?&=]+)=([^?&=]*)/g;

    search.replace(reg, (rs, $1, $2) => {
        const name = decodeURIComponent($1);
        let val = decodeURIComponent($2);
        // TypeScript 中，由于已经使用了decodeURIComponent，这里不需要再显式转换为字符串
        obj[name] = val;
        return rs; // 这行实际上可以移除，因为它对结果没有影响
    });

    return obj;
};


export const getQueryString = (name: string): string | undefined => {
    return getQueryObject(window.location.href)[name];
};

export const getLocal = (name: string): string | null => {
    return localStorage.getItem(name);
};

export const setLocal = (name: string, value: string) => {
    localStorage.setItem(name, value);
};

export const addDay = (days: number): Date => {
    const nowDate = new Date();
    nowDate.setDate(nowDate.getDate() + days);
    return nowDate;
};

export const addMonth = (months: number): Date => {
    const nowDate = new Date();
    nowDate.setMonth(nowDate.getMonth() + months);
    return nowDate;
};

// 修正：将 addYear 方法中的 getYear 更改为getFullYear
export const addYear = (years: number): Date => {
    const nowDate = new Date();
    nowDate.setFullYear(nowDate.getFullYear() + years);
    return nowDate;
};

export const dateFormat = (fmt: string, date: Date): string => {
    let ret;
    const opt: Record<string, string> = {
        "Y+": date.getFullYear().toString(),        // 年
        "m+": (date.getMonth() + 1).toString(),     // 月
        "d+": date.getDate().toString(),            // 日
        "H+": date.getHours().toString(),           // 时
        "M+": date.getMinutes().toString(),         // 分
        "S+": date.getSeconds().toString()          // 秒
    };

    for (const k in opt) {
        ret = new RegExp("(" + k + ")").exec(fmt);
        if (ret) {
            fmt = fmt.replace(ret[1], (ret[1].length === 1) ? opt[k] : opt[k].padStart(ret[1].length, "0"));
        }
    }

    return fmt;
};
