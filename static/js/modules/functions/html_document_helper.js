function get_cookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}
function set_search_params(path) {
    window.history.replaceState(null, null, path)
}
function set_search_params_uniq(path) {
    path = path.split('/')
    path.filter(function (value, index, self) {
        return self.indexOf(value) === index
    })
    path = path.join('/')

    set_search_params(path)
}
function insert_search_param(key, value) {
    key = encodeURIComponent(key)
    value = encodeURIComponent(value)

    let kvp = window.location.search.substr(1).split('&')
    let i=0

    for(; i < kvp.length; i++) {
        if (kvp[i].startsWith(key + '=')) {
            let pair = kvp[i].split('=')
            pair[1] = value
            kvp[i] = pair.join('=')
            break
        }
    }

    if(i >= kvp.length){
        kvp[kvp.length] = [key,value].join('=')
    }
    window.history.replaceState(null, null, '/?' + kvp.join('&'))
}
function get_search_params() {
    if (!window.location.search)
        return

    let tmp, params={}, search_str = window.location.search.substr(1).split("&")

    for (let i = 0; i < search_str.length; i++) {
        tmp = search_str[i].split("=")
        try {
            params[tmp[0]] = JSON.parse(decodeURIComponent(tmp[1]))
        } catch (e) {
            params[tmp[0]] = (decodeURIComponent(tmp[1]))
            console.log(e + ', you are dumb')
        }
    }

    return params
}
function find_search_param(name) {
    let result = null, tmp = []

    location.search
        .substr(1)
        .split("&")
        .forEach(function (item) {
            tmp = item.split("=")
            if (tmp[0] === name) result = decodeURIComponent(tmp[1])
        })

    return result
}