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

    default_table = 'image'
    
    options = {
        author: {
            table: 'image',
            field: 'author',
            listen: 'qAuthor',
        },
        tags: {
            table: 'image',
            field: 'slug',
            listen: 'qTags', //for redirect, dataset.qWhere
        },
        colors: {
            table: 'image',
            field: 'colors',
            listen: 'qColors',
        },
        created_at: {
            table: 'image',
            field: 'created_at',
            listen: 'qDate',
        },
        downloads: {
            table: 'image',
            field: 'downloads',
            listen: 'qDownloads',
        },
        rating: {
            table: 'image',
            field: 'rating',
            listen: 'qRating',
        },
        width: {
            table: 'image',
            field: 'width',
            listen: 'qWidth',
        },
        height: {
            table: 'image',
            field: 'height',
            listen: 'qHeight',
        },
        ratio: {
            table: 'image',
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
        query[key] = false
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
                if (typeof query[key] === 'object' && !Array.isArray(query[key]) && Object.keys(query[key]).length)
                    if (unwanted)
                        this.cleaning(query[key], unwanted[key])
                else {
                    //console.log(query, unwanted[key])
                    //console.log(Object.keys(query[key]).length)
                    if (unwanted[key])
                        this.delete(query, key)
                }

                if (query.hasOwnProperty(key) && !Object.keys(query[key]).length)
                    this.delete(query, key)
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
        if (this.el.dataset.hasOwnProperty(this.option.listen))
            this.el = document.getElementsByClassName(this.el.dataset[this.option.listen])[0]
    }
    prepare() {
        this.redirect()
        this.make_query()
        //console.log(this.unwanted_queries)
        this.cleaning()

        console.log(this.query)
        if (Object.keys(this.query).length) {
            this.request['paths'] = {
                table: (this.option.table? this.option.table : this.default_table)
            }
            this.request['queries'][this.query_name] = this.query
        }
    }
    listen(el, initial_query=null) {
        let is_get = false

        for (let key in this.options) {
            //console.log(this.selector + this.options[key].listen)
            if ((this.el = el.closest(this.selector + this.options[key].listen))) {
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