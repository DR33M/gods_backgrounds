class ImagePutApi {
    prefix = '/api'
    image_pk = ''

    async = true

    rating = {
        method: 'PUT',
        operation: 'rating',
        listening_element: '.upvote-button',
        disabled: 'voted',
        body: JSON.stringify({vote: 1}),
        onload: function () {}
    }
    downloads = {
        method: 'GET',
        operation: 'downloads',
        listening_element: '.download-button',
        disabled: 'downloaded',
        onload: function () {}
    }

    get_api_path(operation, image_pk='') {
        if (operation && image_pk)
            return this.prefix + '/' + operation  + '/' +  image_pk + '/';
    }
    set_image_pk(el) {
        this.image_pk = el.dataset.pk

        return Boolean(this.image_pk);
    }
    update_counter(el) {
        let counter = document.getElementById(el.dataset.counter)

        if (counter) {
            let value = counter.innerText
            if (value)
                counter.innerText = Number(value) + 1
            else counter.innerText = 1
        }
    }
    get_params(el, option) {
        if (!el.classList.contains(option.disabled))
            if (this.set_image_pk(el)) {
                let params = {
                    method: option.method,
                    path: this.get_api_path(option.operation, this.image_pk),
                    async: this.async,
                    onload: option.onload
                }

                if (option.body)
                    params['body'] = option.body

                return params
            }
        return false
    }

    listener_logic(e) {
        let el, event = false

        if ((el = e.target.closest(this.rating.listening_element)))
            event = {el: el, option: this.rating}
        else if ((el = e.target.closest(this.downloads.listening_element)))
            event = {el:el, option:this.downloads}

        return event
    }
}