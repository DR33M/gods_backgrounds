document.addEventListener("DOMContentLoaded", function () {
    let global_api = new GlobalApi()
    let delete_helper = new DeleteHelper()
    let image_patch = new PatchHelper()
    let user_actions = new UserActions()
    let image_detail_view = new ImageDetailHTML()
    let image_upload = new ImageUpdateHTML()

    let get_request = {
        paths: {
            url: 'moderator-panel',
        },
    }

    let request, params

    let render = function () {
        if (request.xhr.status === request.HTTP_404_NOT_FOUND)
            window.location.replace(cabinet_link);
        if (request.xhr.responseText)
            image_detail_view.render(JSON.parse(request.xhr.responseText))
    }

    let img_get_onchange = function () {
        if (request.xhr.readyState === 4) {
            image_upload.tag_error(image_detail_view.image.tags_error.el, request.xhr.responseText)
            params = global_api.get(get_request)
            params.onchange = render
            if (params) {
                request = new HttpRequestsHelper()
                request.send(params, params.onchange)
            }
            params = null
        }
    }

    document.body.addEventListener('click', function (e) {
        if (delete_helper.listen(e.target) && Object.keys(image_patch.listening_elements).length) {
            params = global_api.delete(delete_helper.request)
            params.onchange = img_get_onchange
        } else if (image_patch.listen(e.target)) {
            params = global_api.patch(image_patch.request, image_detail_view.parse_image_tags())
            params.onchange = img_get_onchange
        } else params = null

        if (params) {
            request = new HttpRequestsHelper()
            request.send(params, params.onchange)
        }

        user_actions.modal_window(e.target)
    })

    image_detail_view.render(image_data)
})
