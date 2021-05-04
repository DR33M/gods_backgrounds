class GlobalApi {
    async = true
    methods = {
        get: 'GET',
        patch: 'PATCH',
    }

    prefix = '/api'

    get_async() {
        return this.async
    }
    get_path(request=null) {
        let path = ''
        if (request) {
            path += this.prefix
            path += '/' + request.table
            if (request.field) {
                path += '/' + request.field
                path += '/' + request.pk
                path += '/'
            } else if (request.query_name) {
                path += '/?'
                path += request.query_name + '=' + encodeURI(JSON.stringify(request.query))
            }
        }

        return path
    }
    get_data(data) {
        if (data)
            data = JSON.parse(data)

        return data
    }


    get(path) {
        let params = {}

        params.method = this.methods.get
        params.async = this.get_async()
        params.path = this.get_path(path)

        console.log(params)
        return params
    }
    patch(path, data) {
        let params = {}

        params.method = this.methods.patch
        params.async = this.get_async()
        params.path = this.get_path(path)
        params.data = this.get_data(data)

        console.log(params)
        return params
    }
}