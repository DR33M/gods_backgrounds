class HttpRequestsHelper {
    xhr = new XMLHttpRequest();

    content_type = 'application/json; charset=utf-8'
    X_CSRF_Token = getCookie('csrftoken')

    set_request_readers() {
        this.xhr.setRequestHeader('Content-type', this.content_type);
        this.xhr.setRequestHeader('X-CSRFToken', this.X_CSRF_Token);
    }

    send(params) {
        let xhr = this.xhr

        xhr.open(params.method, params.path, params.async);
        this.set_request_readers();

        if (params.json_body)
            xhr.send(params.json_body);
        else xhr.send();

        if (params.onload)
            xhr.onload = params.onload
    }
}