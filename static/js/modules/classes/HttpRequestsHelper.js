class HttpRequestsHelper {
    HTTP_200_OK = 200
    HTTP_202_ACCEPTED = 202
    HTTP_404_NOT_FOUND = 404
    HTTP_429_TOO_MANY_REQUESTS = 429

    content_type = 'application/json; charset=utf-8'
    X_CSRF_Token = get_cookie('csrftoken')

    constructor(extra_data=null) {
        this.xhr = new XMLHttpRequest()
        if (extra_data)
            this.xhr.extra_data = extra_data
    }

    set_request_readers() {
        this.xhr.setRequestHeader('Content-type', this.content_type)
        this.xhr.setRequestHeader('X-CSRFToken', this.X_CSRF_Token)
    }

    send(params, onchange) {
        let xhr = this.xhr

        xhr.open(params.method, params.path, params.async)
        this.set_request_readers()

        if (onchange)
            xhr.onreadystatechange = onchange
        else xhr.onreadystatechange = function() {
            if (xhr.readyState !== 4) return

            console.log('HTTP response', xhr.status, xhr.statusText)
        };

        if (params.data)
            xhr.send(JSON.stringify(params.data))
        else xhr.send()
    }
}