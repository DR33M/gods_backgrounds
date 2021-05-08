class GlobalApi {
    async = true
    methods = {
        get: 'GET',
        patch: 'PATCH',
    }

    prefix = '/api'

    params = {}

    last_full_path = ''
    last_path = ''
    last_params = {}

    get_async() {
        return this.async
    }
    get_path(request=null) {
        let path = ''
        if (request) {
            path += '/' + request.table
            if (request.field) {
                path += '/' + request.field
                path += '/' + request.pk
                path += '/'
            } else if (request.query_name) {
                path += '/?'
                path += request.query_name + '=' + encodeURI(JSON.stringify(request.query))
            }
            if (request.page_name)
                path += '&' + request.page_name + '=' + request.page
        }

        this.last_path = path
        this.last_full_path = path = this.prefix + path

        console.log(path)

        return path
    }
    get_data(data) {
        if (data)
            data = JSON.parse(data)

        return data
    }


    get(request) {
        this.params = {}

        this.params.method = this.methods.get
        this.params.async = this.get_async()
        this.params.path = this.get_path(request)

        console.log(this.params)
        return this.last_params = this.params
    }
    patch(path, data) {
        this.params = {}

        this.params.method = this.methods.patch
        this.params.async = this.get_async()
        this.params.path = this.get_path(path)
        this.params.data = this.get_data(data)

        console.log(this.params)
        return this.last_params = this.params
    }
}