document.addEventListener("DOMContentLoaded", function () {
    let global_api = new GlobalApi()
    let image_patch = new PatchHelper()
    let user_actions = new UserActions()
    let image_view = new ImageView(user_actions, number_of_columns, null, image_patch)

    let request, params

    let img_patch_onchange = function () {
        image_view.onchange(request)
    }

    document.body.addEventListener('click', function (e) {
        if (image_patch.listen(e.target)) {
            params = global_api.patch(image_patch.request, image_patch.data)
            params.onchange = img_patch_onchange
        } else params = null

        if (params) {
            request = new HttpRequestsHelper()
            request.send(params, params.onchange)
        }

        user_actions.modal_window(e.target)
    })

    document.body.addEventListener('focusin', function (e) {
        if (e.target.textContent === '')
            user_actions.el_visibility(e.target)
    })
    document.body.addEventListener('focusout', function (e) {
        if (e.target.textContent !== '' && e.target.dataset.hasOwnProperty('where')) {
            e.target.dataset.where = image_view.search.get_slug(e.target.textContent)
        } else user_actions.el_visibility(e.target)
    })

    image_view.html.arrange(images_list)
})