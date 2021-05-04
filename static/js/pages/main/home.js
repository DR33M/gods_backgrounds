document.addEventListener("DOMContentLoaded", function () {
    let global_api = new GlobalApi()
    let image_get = new GetHelper()
    let image_patch = new PatchHelper()
    let user_actions = new UserActions()

    let request, params, elements
    let search_query = get_search_params()
    let initial_query = null

    if (search_query && search_query[image_get.query_name])
        initial_query = search_query[image_get.query_name]

    let img_get_onchange = function () {
        image_GET_onload(request, elements, image_get, user_actions)
    }
    let img_patch_onchange = function () {
        image_PATCH_onload(request, elements, image_patch)
    }

    document.body.addEventListener('click', function (e) {
        params = null

        if ((elements = image_get.listen(e.target, initial_query)) && Object.keys(elements).length) {
            params = global_api.get(image_get.request)
            params.onchange = img_get_onchange
        } else if ((elements = image_patch.listen(e.target)) && Object.keys(elements).length) {
            params = global_api.patch(image_patch.request, image_patch.data)
            params.onchange = img_patch_onchange
        }

        if (params) {
            request = new HttpRequestsHelper()
            request.send(params, params.onchange)
        }

        user_actions.drop_list(e.target)
        user_actions.modal_window(e.target)
    })

    document.body.addEventListener('focusin', function (e) {
        user_actions.close(e.target)
    })
    document.body.addEventListener('focusout', function (e) {
        if (e.target.textContent !== '' && e.target.dataset.hasOwnProperty('where')) {
            e.target.dataset.where = get_clean_tags(e.target.textContent)
        } else user_actions.open(e.target)
    })

    arrange_images()
})