function get_cookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}
function set_search_params() {
    //window.history.replaceState(null, null, sort.query_path)
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