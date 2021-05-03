class ImageQueryApi {
    async = true
    http_request_path = '/api'

    abstract_query = {
        'where': {},
        'in': {},
        'more_than': {},
        'less_than': {},
        'order': {},
    }
    query = {}
    encoded_query = ''
    starting_query = {}
    query_name = 'q'
    query_header = '/?' + this.query_name + '='
    query_path = ''

    operations = {
        'where': function (self, el, option) {
            if (el.dataset.keysHandler) {
                let value = self.get_keys(el.dataset.keysHandler)
                if (value) {
                    value = self.format_value(el, value)
                    value.sort(function(a, b){
                        if(a < b) return -1
                        if(a > b) return 1
                        return 0
                    })
                    value = value.join('-')
                    self.set_field('where', option, value)
                    self.starting_query.where = self.query['where']
                }
            }
        },
        'in': function (self, el, option) {
            if (el.dataset.keysHandler) {
                let value = self.get_keys(el.dataset.keysHandler)
                if (value) {
                    value = self.format_value(el, value)
                    self.set_field('in', option, value)
                    self.starting_query.in = self.query['in']
                }
            }
        },
        'less_than': function (self, el, option) {
            if (el.dataset.lessThan) {
                let value = self.format_value(el, el.dataset.lessThan)
                self.set_field('less_than', option, value)
            }
        },
        'more_than': function (self, el, option) {
            if (el.dataset.moreThan) {
                let value = self.format_value(el, el.dataset.moreThan)
                self.set_field('more_than', option, value)
            }
        },
        'order': function (self, el, option) {
            if (el.dataset.order) {
                let order = self.format_value(el, el.dataset.order)
                self.set_field('order', option, order)
            } else self.set_field('order', option, ' ')
        },
    }

    path = '/images'
    method = 'GET'
    tag = {
        operations: [
            this.operations["where"],
        ],
        fields: ['slug',],
        listening_element: '.q-where',
    }
    color = {
        operations: [
            this.operations["where"],
        ],
        fields: ['color',],
        listening_element: '.q-where',
    }
    date = {
        operations: [
            this.operations["less_than"],
            this.operations["more_than"],
            this.operations["order"]
        ],
        fields: ['created_at',],
        listening_element: '.q-date',
        order: 'created_at'
    }
    downloads = {
        operations: [this.operations["order"]],
        fields: ['downloads',],
        listening_element: '.q-downloads',
        order: 'downloads'
    }
    rating = {
        operations: [this.operations["order"]],
        fields: ['rating',],
        listening_element: '.q-rating',
        order: 'rating'
    }
    screen = {
        operations: [this.operations["more_than"]],
        fields: ['width', 'height',],
        listening_element: '.q-screen',
    }
    ratio = {
        operations: [this.operations["more_than"], this.operations["less_than"]],
        fields: ['ratio',],
        listening_element: '.q-ratio',
    }

    constructor() {
        let data = this.find_GET_parameter(this.query_name)

        if (data)
            try {
                this.starting_query = JSON.parse(decodeURIComponent(data))
            } catch (e) {
                console.log(e + ', you are dumb')
            }
    }

    onload() {
        console.log(this.status) //this = XMLHttpRequest
    }

    get_keys(key_handler) {
        key_handler = document.getElementsByClassName(key_handler)[0]
        let value = false


        if (key_handler.tagName === 'INPUT' && key_handler.value)
            value = key_handler.value
        else if (key_handler.dataset.keys)
            value = key_handler.dataset.keys
        else if (key_handler.innerHTML)
            value = key_handler.innerHTML

        if (typeof value === 'string') {
            let tmp = value.split(',')
            value = []

            for (let i = 0; i < tmp.length; i++) {
                tmp[i] = tmp[i].toLowerCase()
                tmp[i] = tmp[i].replace(/([a-zA-Z0-9])\s([a-zA-Z0-9])/g, "$1-$2")
                tmp[i] = tmp[i].replace(/\s/g, '')
                if (tmp[i] && !tmp[i].match(/[\!\#\$\%\&\'\*\+\/\=\\\?\^\_\`\{\|\}\~\"\,\:\;\<\>\@\[\]]+/g))
                    value.push(tmp[i])
            }
        }

        return value
    }
    format_value(el, value) {
        let clean_value = value

        if (value === 'self')
            clean_value = el.innerHTML

        return clean_value
    }
    set_field(operation, option, value) {
        for (let i = 0; i < option.fields.length; i++)
            this.query[operation][option.fields[i]] = value
    }

    choose_operation(el, option) {
        let els = []

        if (el.dataset.qRedirect) {
            let elsClasses = el.dataset.qRedirect.split(' ')

            for (let i = 0; i < elsClasses.length; i++)
                els.push(document.getElementsByClassName(elsClasses[i])[0])
        }


        for (let i = 0; i < option.operations.length; i++) {
            if (els.length) {
                for (let j = 0; j < els.length; j++)
                    option.operations[i](this, els[j], option)
            } else {
                option.operations[i](this, el, option)
            }
        }
    }

    find_GET_parameter(name) {
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
    delete_empty(obj) {
        if (Object.keys(obj).length)
            for (let key in obj) {
                if (typeof obj[key] === 'object')
                     this.delete_empty(obj[key])

                if (!Object.keys(obj[key]).length) {
                    obj[key] = false
                    delete obj[key]
                }
            }

        return obj
    }
    merge_queries() {
        for (let key in this.starting_query)
            this.query[key] = this.starting_query[key]
    }
    set_search_parameters(el, option) {
        this.query = JSON.parse(JSON.stringify(this.abstract_query))
        this.merge_queries()
        this.choose_operation(el, option)
        this.query = this.delete_empty(this.query)

        this.encoded_query = encodeURI(JSON.stringify(this.query))
        this.query_path = this.query_header + this.encoded_query
    }
    get_params(el, option) {
        this.set_search_parameters(el, option)
        console.log(this.query)
        if (Object.keys(this.query).length)
            return {
                method: this.method,
                path: this.http_request_path + this.path + this.query_path,
                async: this.async,
                onload: this.onload
            }

        return false
    }

    listener_logic(e) {
        let el, event = false

        if ((el = e.target.closest(this.tag.listening_element)))
            event = {el: el, option: this.tag}
        else if ((el = e.target.closest(this.color.listening_element)))
            event = {el: el, option: this.color}
        else if ((el = e.target.closest(this.date.listening_element)))
            event = {el:el, option:this.date}
        else if ((el = e.target.closest(this.downloads.listening_element)))
            event = {el:el, option:this.downloads}
        else if ((el = e.target.closest(this.rating.listening_element)))
            event = {el:el, option:this.rating}
        else if ((el = e.target.closest(this.screen.listening_element)))
            event = {el:el, option:this.screen}
        else if ((el = e.target.closest(this.ratio.listening_element)))
            event = {el:el, option:this.ratio}

        return event
    }
}