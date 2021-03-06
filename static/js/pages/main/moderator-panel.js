document.addEventListener("DOMContentLoaded", function () {
    function main() {
        let global_api = new GlobalApi()
        let delete_helper = new DeleteHelper()
        let image_get = new GetHelper()
        let image_patch = new PatchHelper()
        let user_actions = new UserActions()
        let image_detail_view = new ImageDetailHTML()
        let messages = new Messages('.js-messages')

        let request, params

        let render = function () {
            if (request.xhr.status === request.HTTP_404_NOT_FOUND)
                window.location.replace(cabinet_link)
            if (request.xhr.responseText)
                image_detail_view.render(JSON.parse(request.xhr.responseText))
        }

        let img_get_onchange = function () {
            if (request.xhr.readyState === 4) {
                if (request.xhr.responseText)
                    messages.add_message(JSON.parse(request.xhr.responseText))
                params = global_api.get(image_get.options.mp_get)
                params.onchange = render
                send_request(params)
            }
        }

        function send_request(params) {
            if (params) {
                request = new HttpRequestsHelper()
                request.send(params, params.onchange)
            }
        }

        document.body.addEventListener('click', function (e) {
            if (delete_helper.listen(e.target)) {
                params = global_api.delete(delete_helper.request)
                params.onchange = img_get_onchange
            } else if (image_patch.listen(e.target)) {
                params = global_api.patch(image_patch.request, image_detail_view.parse_image_tags())
                params.onchange = img_get_onchange
            } else params = null

            send_request(params)

            user_actions.modal_window(e.target)
        })

        image_detail_view.render(image_data)
    }

    if (typeof image_data !== 'undefined' &&
        typeof cabinet_link !== 'undefined')
        main()
})
