class ImagePutApi {
    prefix = '/api'
    image_pk = ''

    async = true

    rating = {
        method: 'PUT',
        operation: 'rating',
        listening_element: '.rating-button',
        disabled: 'voted',
        upvote: 'upvote',
        vote: 1,
        onload: function () {}
    }
    downloads = {
        method: 'GET',
        operation: 'downloads',
        listening_element: '.download',
        disabled: 'downloaded',
        onload: function () {}
    }


    get_api_path(operation, image_pk='') {
        if (operation && image_pk)
            return this.prefix + '/' + operation + '/' + image_pk + '/';
    }
    set_image_pk(el) {
        this.image_pk = el.dataset.pk

        return Boolean(this.image_pk);
    }
    update_counter(el, count) {
        let counter = document.getElementById(el.dataset.counter)

        if (counter)
            counter.innerText = count
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

                params['body'] = JSON.stringify({vote: option.vote})
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