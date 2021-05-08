document.addEventListener("DOMContentLoaded", function () {
    let userActions = new UserActions()
    let image_put = new PatchHelper()
    let request, el, params, event

    image_put.rating.onload = function() { rating_onload(this, image_put, request, el) }
    image_put.downloads.onload = function() { downloads_onload(this, image_put, request, el) }

    document.body.addEventListener('click', function (e) {
        params = false

        if ((event = image_put.listener_logic(e)))
            params = image_put.get_params(event.el, event.option)

        if (event)
            el = event.el

        if (params) {
            request = new HttpRequestsHelper()
            request.send(params)
        }

        userActions.modal_window(e)
    })

    arrange_images()
})