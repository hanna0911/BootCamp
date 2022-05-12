const CookieOperation={
    getCookie:(key,defaultValue)=>{
        var rgx = new RegExp("(?:^|(?:; ))"+key+"=([^;]*)")
        var result = document.cookie.match(rgx)
        if(result){
            return unescape(result[1])
        }else{
            return defaultValue
        }
    },
    setCookie:(key,value,expire_ms)=>{
        var exdate = new Date();
        exdate.setTime(exdate.getTime() + expire_ms);
        document.cookie = key + "=" + escape(value) + ((expire_ms == null) ? "" : ";expires=" + exdate.toGMTString());
    },
    delCookie:(key)=>{
        var currentValue = CookieOperation.getCookie(key);
        if(currentValue != null){
            var exdate = new Date();
            exdate.setTime(exdate.getTime() - 1);
            document.cookie = key + "=" + currentValue + ";expires=" + exdate.toGMTString();
        }
    }
}

export default CookieOperation