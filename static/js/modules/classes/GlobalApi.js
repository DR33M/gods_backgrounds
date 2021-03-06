class GlobalApi {
    async = true
    methods = {
        get: 'GET',
        patch: 'PATCH',
        delete: 'DELETE',
    }
    current_method = ''

    prefix = '/api'

    params = {}

    last_full_path = ''
    last_path = ''
    last_params = {}

    get_async() {
        return this.async
    }
    get_path(request=null, path=[]) {
        if (request) {
            for (let key in request.paths) {
                path.push('/')
                path.push(request.paths[key])
            }
            if (this.current_method === this.methods.get && request.queries) {
                path.push('?')
                let keys = Object.keys(request.queries)
                for (let i = 0; i < keys.length; i++) {
                    path.push((i !== 0 ? '&' : '') + keys[i])
                    path.push('=')
                    //console.log(request.queries['q'])
                    path.push(encodeURI(JSON.stringify(request.queries[keys[i]])))
                }
            } else if (this.current_method !== this.methods.get)
                path.push('/')
        }

        this.last_path = path.join('')
        this.last_full_path = path = (request.api? request.api : this.prefix) + this.last_path

        //console.log(path)
        //console.log(request)

        return path
    }
    get_data(data) {
        if (data)
            data = JSON.parse(data)

        return data
    }


    get(request) {
        this.params = {}

        this.params.method = this.current_method = this.methods.get
        this.params.async = this.get_async()
        this.params.path = this.get_path(request)

        //console.log(request)
        return this.last_params = this.params
    }
    patch(path, data) {
        this.params = {}

        this.params.method = this.current_method = this.methods.patch
        this.params.async = this.get_async()
        this.params.path = this.get_path(path)
        this.params.data = this.get_data(data)

        //console.log(this.params)
        return this.last_params = this.params
    }
    delete(path) {
        this.params = {}

        this.params.method = this.current_method = this.methods.delete
        this.params.async = this.get_async()
        this.params.path = this.get_path(path)

        //console.log(this.params)
        return this.last_params = this.params
    }
}