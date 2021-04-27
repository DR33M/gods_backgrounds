document.addEventListener("DOMContentLoaded", function () {
    let sort = new ImageSortApi()
    let image_put = new ImagePutApi()
    let user_actions = new UserActions()

    let request, el, params, event

    sort.onload = function () {
        if (this.responseText) {
            window.history.replaceState(null, null, sort.query_path)
            prepare_place()
            add_images(JSON.parse(this.responseText))
            arrange_images()
        }
    }
    image_put.rating.onload = function () {
        el.classList.add(image_put.rating.disabled)
        if (this.status === request.HTTP_202_ACCEPTED)
            image_put.update_counter(el)
    }
    image_put.downloads.onload = function () {
        el.classList.add(image_put.downloads.disabled)
        if (this.status === request.HTTP_202_ACCEPTED)
            image_put.update_counter(el)
    }
    
    document.body.addEventListener('click', function (e) {
        params = false

        if ((event = image_put.listener_logic(e))) {
            params = image_put.get_params(event.el, event.option)
        } else if((event = sort.listener_logic(e))) {
            params = sort.get_params(event.el, event.option)
        }

        if (event) {
            el = event.el
            change_order(el)
        }

        if (params) {
            request = new HttpRequestsHelper()
            request.send(params)
        }

        user_actions.drop_list(e)
    })

    arrange_images()
})