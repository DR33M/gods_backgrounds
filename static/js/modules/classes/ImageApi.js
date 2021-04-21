class ImageApi {
    request = HttpRequestsHelper

    HTTP_200_OK = 200
    HTTP_202_ACCEPTED = 202

    image_pk = ''

    rating = {
        method: 'PUT',
        path: '/api/rating/',
        listening_element: '.upvote-button',
        disabled: 'voted',
    }
    downloads = {
        method: 'GET',
        path: '/api/downloads/',
        listening_element: '.download-button',
        disabled: 'downloaded',
    }
    find = {
        method: 'GET',
        path: '/api/find/?',
        listening_element: '.find-button',
    }
    sort = {
        method: 'GET',
        path: '/api/sort/?',
        date: {
            field: 'created_at',
            listening_element: '.sort-date-button',
        },
        downloads: {
            field: 'downloads',
            listening_element: '.sort-downloads-button',
        },
        rating: {
            field: 'rating',
            listening_element: '.sort-rating-button',
        },
        screen: {
            field: 'screen',
            fields: {
                width: {
                    name: 'width',
                    value: '1024',
                },
                height: {
                    name: 'height',
                    value: '1024',
                }
            },
            listening_element: '.sort-screen-button',
        },
    }

    set_image_pk(currEl) {
        this.image_pk = currEl.dataset.pk + '/'

        return Boolean(this.image_pk);
    }
    asc(field) {
        return '-' + field;
    }
    set_GET_parameter(key, value) {
        return key+'='+value+'&'
    }
    get_value(handler) {
        if (handler.tagName === 'INPUT')
            return handler.value
        return handler.innerText
    }
    update_counter(currEl) {
        let counter = document.getElementById(currEl.dataset.counter)

        if (counter) {
            let rating = Number(counter.innerText)
            if (rating)
                counter.innerText = rating + 1
            else counter.innerText = 1
        }
    }

    change_rating(currEl) {
        if (!currEl.classList.contains('.' + this.rating.disabled)) {
            let request = new this.request()
            let self = this

            if (this.set_image_pk(currEl) && !currEl.classList.contains(this.rating.disabled))
                request.send({
                    method: this.rating.method,
                    path: this.rating.path + this.image_pk,
                    async: true,
                    json_body: JSON.stringify({vote: 1}),
                    onload: function () {
                        currEl.classList.add(self.rating.disabled)
                        if (request.xhr.status === self.HTTP_202_ACCEPTED)
                            self.update_counter(currEl)
                        console.log(`Response ${request.xhr.status}: ${request.xhr.statusText}`)
                    }
                })
        }
    }
    change_downloads(currEl) {
        if (!currEl.classList.contains(this.downloads.disabled)) {
            let request = new this.request()
            let self = this

            if (this.set_image_pk(currEl) && !currEl.classList.contains(this.downloads.disabled))
                request.send({
                    method: this.downloads.method,
                    path: this.downloads.path + this.image_pk,
                    async: true,
                    onload: function () {
                        currEl.classList.add(self.downloads.disabled)
                        console.log(`Response ${request.xhr.status}: ${request.xhr.statusText}`)
                    }
            })
        }
    }
    find_by_key(currEl) {
        let request = new this.request()
        let key = ''

        if (currEl.dataset.keyHandler)
            key = this.get_value(document.getElementById(currEl.dataset.keyHandler))
        else key = currEl.innerText

        key = 'fit, girl, legs'
        key = key.replace(/[\s]{2}/g, ' ') //del more than one white-space symbols
        key = key.replace(/([\s]+[,]+[\s]+)|([\s]+[,]+)|[,]+[\s]+/g, ',') //del any white-space symbols after & before coma
        key = key.split(new RegExp(','))
        console.log(key)
        key = this.set_GET_parameter('key', encodeURI(JSON.stringify(key)))

        console.log(this.find.path + key)
        if (key)
            request.send({
                method: this.find.method,
                path: this.find.path + key,
                async: true,
                onload: function () {
                    console.log(`Response ${request.xhr.status}: ${request.xhr.statusText}`)
                    if (request.xhr.responseText)
                        console.log(JSON.parse(request.xhr.responseText))
                }
            })
    }
    sort_by_key(currEl, sort_name) {
        let request = new this.request()
        let self = this
        let order = currEl.dataset.order
        let start = currEl.dataset.start
        let end = currEl.dataset.end
        let key = ''

        if (start)
            key += this.set_GET_parameter('start', start)
        if (end)
            key += this.set_GET_parameter('end', end)
        if (order)
            key += this.set_GET_parameter('order', order)

        console.log(this.sort.path + 'field=' + sort_name.field + '&' + key)
        request.send({
            method: this.sort.method,
            path: this.sort.path + self.set_GET_parameter('field', sort_name.field) + key,
            async: true,
            onload: function () {
                console.log(`Response ${request.xhr.status}: ${request.xhr.statusText}`)
                if (request.xhr.responseText)
                    console.log(JSON.parse(request.xhr.responseText))
            }
        })
    }
    sort_by_keys(currEl, sort_name) {
        let request = new this.request()
        let fields = currEl.dataset.fields.split(' ')
        let data = [], value, key = ''

        for (let i = 0; i < fields.length; i++) {
            value = this.get_value(document.getElementById(fields[i]))
            data.push({
                name: fields[i],
                value: value
            })
        }

        key = this.set_GET_parameter('fields', encodeURI(JSON.stringify(data)))

        request.send({
            method: this.sort.method,
            path: this.sort.path + this.set_GET_parameter('field', sort_name.field) + key,
            async: true,
            onload: function () {
                console.log(`Response ${request.xhr.status}: ${request.xhr.statusText}`)
                if (request.xhr.responseText)
                    console.log(JSON.parse(request.xhr.responseText))
            }
        })
    }

    listener_logic(e) {
        let currEl

        if ((currEl = e.target.closest(this.rating.listening_element))) { this.change_rating(currEl) }
        else if ((currEl = e.target.closest(this.downloads.listening_element))) { this.change_downloads(currEl) }
        else if ((currEl = e.target.closest(this.find.listening_element))) { this.find_by_key(currEl) }
        else if ((currEl = e.target.closest(this.sort.date.listening_element))) {
            this.sort_by_key(currEl, this.sort.date)
        } else if ((currEl = e.target.closest(this.sort.downloads.listening_element))) {
            this.sort_by_key(currEl, this.sort.downloads)
        } else if ((currEl = e.target.closest(this.sort.rating.listening_element))) {
            this.sort_by_key(currEl, this.sort.rating)
        } else if ((currEl = e.target.closest(this.sort.screen.listening_element))) {
            this.sort_by_keys(currEl, this.sort.screen)
        }
    }
}