class GetHelper {
    selector = '.'

    without = {
        delimiter: ':',
        all: '*'
    }

    request = {
        paths: {},
        queries: {}
    }

    initial_query = {}
    query = {}
    unwanted_queries = {}
    query_name = 'q'

    operations = {
        where: 'where',
        in: 'in',
        lessThan: 'less_than',
        moreThan: 'more_than',
        order: 'order'
    }

    listening_elements = {}
    
    options = {
        mp_get: {
            paths: {
                table: 'image',
                extra_action: 'mp_get',
            },
        },
        all_images: {
            paths: {
                table: 'image',
                extra_action: 'get',
            },
        },
        author: {
            paths: {
                table: 'image',
                extra_action: 'get',
            },
            field: 'author',
            listen: 'qAuthor',
        },
        tags: {
            paths: {
                table: 'image',
                extra_action: 'get',
            },
            field: 'slug',
            listen: 'qTags', //for redirect, dataset.qWhere
        },
        colors: {
            paths: {
                table: 'image',
                extra_action: 'get',
            },
            field: 'colors',
            listen: 'qColors',
        },
        created_at: {
            paths: {
                table: 'image',
                extra_action: 'get',
            },
            field: 'created_at',
            listen: 'qDate',
        },
        downloads: {
            paths: {
                table: 'image',
                extra_action: 'get',
            },
            field: 'downloads',
            listen: 'qDownloads',
        },
        rating: {
            paths: {
                table: 'image',
                extra_action: 'get',
            },
            field: 'rating',
            listen: 'qRating',
        },
        width: {
            paths: {
                table: 'image',
                extra_action: 'get',
            },
            field: 'width',
            listen: 'qWidth',
        },
        height: {
            paths: {
                table: 'image',
                extra_action: 'get',
            },
            field: 'height',
            listen: 'qHeight',
        },
        ratio: {
            paths: {
                table: 'image',
                extra_action: 'get',
            },
            field: 'ratio',
            listen: 'qRatio',
        }
    }

    el = {}
    option = {}
    operation_key = ''
    value = ''

    make_abstract_query() {
        let query = {}

        for (let key in this.operations)
            query[this.operations[key]] = {}

        return query
    }
    initialize(initial_query) {
        if (!Object.keys(this.query).length)
            this.query = this.make_abstract_query()
        this.unwanted_queries = this.make_abstract_query()

        if (typeof initial_query === 'object' && (this.initial_query = initial_query))
            for (let key in initial_query)
                if (this.query.hasOwnProperty(key))
                    this.query[key] = initial_query[key]
    }
    make_unwanted_queries() {
        if (this.el.dataset.withoutOptions) {
            let without_option
            let without_options = this.el.dataset.withoutOptions.split(' ')

            for (let i = 0; i < without_options.length; i++) {
                without_option = without_options[i].split(this.without.delimiter) // example: data-without-options="downloads:*" will be ['downloads', '*']
                //console.log(without_option[1])
                //console.log(this.unwanted_queries[without_option[1]])
                if (without_option[1] === this.without.all) {
                    for (let key in this.unwanted_queries)
                        this.unwanted_queries[key][without_option[0]] = true
                } else if (without_option[1] && this.unwanted_queries[without_option[1]]) {
                    this.unwanted_queries[without_option[1]][without_option[0]] = true
                }
            }
        }
    }
    delete(query, key) {
        query[key] = null
        delete query[key]
    }
    cleaning(query = null, unwanted=null) {
        if (!query) {
            query = this.query
            unwanted = this.unwanted_queries
        }

        //delete if empty or unwanted
        if (Object.keys(query).length)
            for (let key in query) {
                //console.log(key)
                if (typeof query[key] === 'object') {
                    this.cleaning(query[key], unwanted[key]) //recursion

                    if (!Object.keys(query[key]).length) {
                        this.delete(query, key)
                    }
                } else if (unwanted && unwanted[key]) { //if unwanted[operation][option] == true
                    this.delete(query, key)
                }
            }
    }
    set_field() {
        if (this.value) {
            if (!this.query.hasOwnProperty(this.operations[this.operation_key]))
                this.query[this.operations[this.operation_key]] = {}

            //console.log(this.operations[this.operation_key])
            this.query[this.operations[this.operation_key]][this.option.field] = this.value
        }
    }
    set_value() {
        this.value = null

        if (this.el.tagName === 'INPUT' && this.el.value)
            this.value = this.el.value
        else if (this.el.dataset.hasOwnProperty(this.operation_key))
            if (this.el.dataset[this.operation_key] === 'self')
                this.value = this.el.innerHTML
            else if (this.el.dataset[this.operation_key] !== '')
                this.value = this.el.dataset[this.operation_key]

        //console.log(this.value)
    }
    make_query() {
        if (this.el)
            for (let key in this.operations)
                if (this.el.dataset.hasOwnProperty(key)) {
                    this.operation_key = key

                    //console.log(this.operation_key)
                    this.set_value()
                    this.set_field()
                }
    }
    redirect() {
        if (this.el && this.el.dataset.hasOwnProperty(this.option.listen))
            this.el = document.getElementsByClassName(this.el.dataset[this.option.listen])[0]
    }
    prepare() {
        this.redirect()
        this.make_query()
        //console.log(this.unwanted_queries)
        this.cleaning()

        //console.log(this.query)
        if (this.option)
            this.request['paths'] = this.option.paths
        if (Object.keys(this.query).length)
            this.request['queries'][this.query_name] = this.query
    }
    flush_listening_elements() {
        this.listening_elements = {}
    }
    listen(el, initial_query=null) {
        let is_get = false

        for (let key in this.options) {
            //console.log(this.selector + this.options[key].listen)
            if (this.options[key].hasOwnProperty('listen') && (this.el = el.closest(this.selector + this.options[key].listen))) {
                //console.log(this.el)
                this.option = this.options[key]
                this.initialize(initial_query)
                this.make_unwanted_queries()
                this.prepare()

                this.listening_elements[key] = this.el
                is_get = true
            }
        }

        return is_get
    }
}