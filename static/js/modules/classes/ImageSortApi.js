class ImageSortApi {
    async = true
    http_request_path = '/api'

    abstract_query = {
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
        'in': function (self, el, option) {
            if (el.dataset.keysHandler) {
                let value = self.get_keys(el.dataset.keysHandler)
                if (value) {
                    let tags = self.format_value(el, value)
                    self.set_field('in', option, tags)
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
            } else self.set_field('order', option, '')
        },
    }

    path = '/images'
    method = 'GET'
    tag = {
        operations: [
            this.operations["in"],
        ],
        fields: ['tags__slug',],
        listening_element: '.sort-in',
    }
    color = {
        operations: [
            this.operations["in"],
        ],
        fields: ['color',],
        listening_element: '.sort-in',
    }
    date = {
        operations: [
            this.operations["less_than"],
            this.operations["more_than"],
            this.operations["order"]
        ],
        fields: ['created_at',],
        listening_element: '.sort-date',
        order: 'created_at'
    }
    downloads = {
        operations: [this.operations["order"]],
        fields: ['downloads',],
        listening_element: '.sort-downloads',
        order: 'downloads'
    }
    rating = {
        operations: [this.operations["order"]],
        fields: ['rating',],
        listening_element: '.sort-rating',
        order: 'rating'
    }
    screen = {
        operations: [this.operations["more_than"]],
        fields: ['width', 'height',],
        listening_element: '.sort-screen',
    }
    ratio = {
        operations: [this.operations["more_than"], this.operations["less_than"]],
        fields: ['ratio',],
        listening_element: '.sort-ratio',
    }

    constructor() {
        let data = this.find_GET_parameter(this.query_name)

        if (data)
            try {
                this.starting_query = JSON.parse(decodeURIComponent(data))
            } catch (e) {
                console.log(e + ' You are dumb')
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
            value = value.split(',')
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

        if (el.dataset.sortRedirect) {
            let elsClasses = el.dataset.sortRedirect.split(' ')

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
    delete_empty() {
        for (let key in this.query) {
            if (Object.keys(this.query[key]).length === 0) {
                this.query[key] = false
                delete this.query[key]
            }
        }
    }
    merge_queries() {
        for (let key in this.starting_query)
            this.query[key] = this.starting_query[key]
    }
    set_search_parameters(el, option) {
        this.query = JSON.parse(JSON.stringify(this.abstract_query));
        this.merge_queries()
        this.choose_operation(el, option)

        this.encoded_query = encodeURI(JSON.stringify(this.query))
        this.query_path = this.query_header + this.encoded_query
    }
    get_params(el, option) {
        this.set_search_parameters(el, option)
        this.delete_empty()
        console.log(this.query)
        return {
            method: this.method,
            path: this.http_request_path + this.path + this.query_path,
            async: this.async,
            onload: this.onload
        }
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