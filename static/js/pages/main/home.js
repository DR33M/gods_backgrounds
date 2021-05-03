document.addEventListener("DOMContentLoaded", function () {
    let sort = new ImageQueryApi()
    let image_put = new ImagePutApi()
    let user_actions = new UserActions()

    let request, el, params, event

    sort.onload = function() {sort_onload(this, sort)}
    image_put.rating.onload = function() { rating_onload(this, image_put, request, el) }
    image_put.downloads.onload = function() { downloads_onload(this, image_put, request, el) }
    
    document.body.addEventListener('click', function (e) {
        params = false

        if ((event = image_put.listener_logic(e))) {
            params = image_put.get_params(event.el, event.option)
        } else if((event = sort.listener_logic(e))) {
            params = sort.get_params(event.el, event.option)
            change_order(event.el)
        }

        if (event)
            el = event.el

        if (params) {
            request = new HttpRequestsHelper()
            request.send(params)
        }

        user_actions.drop_list(e)
    })

    arrange_images()
})