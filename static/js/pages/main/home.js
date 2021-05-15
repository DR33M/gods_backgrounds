document.addEventListener("DOMContentLoaded", function () {
    let global_api = new GlobalApi()
    let image_get = new GetHelper()
    let image_patch = new PatchHelper()
    let user_actions = new UserActions()
    let pagination = new Pagination()
    let image_view = new ImageView(user_actions, number_of_columns, image_get, image_patch)

    let request, params
    let search_query = get_search_params()
    let initial_query = null

    if (search_query && search_query[image_get.query_name])
        initial_query = search_query[image_get.query_name]

    pagination.page = page
    pagination.update_total_pages(total_pages)
    pagination.update_html()

    let img_get_onchange = function () {
        set_search_params(global_api.last_path)
        image_view.onchange(request)
        pagination.onchange(request, image_view.response_text['total_pages'])
    }
    let img_pagination_onchange = function () {
        set_search_params(global_api.last_path)
        if (pagination.onchange(request, image_view.response_text['total_pages']))
            image_view.html.arrange(pagination.response_text['images'])
    }
    let img_patch_onchange = function () {
        image_view.onchange(request)
    }

    document.body.addEventListener('click', function (e) {
        if (image_get.listen(e.target, initial_query) && Object.keys(image_get.listening_elements).length)
        {
            pagination.first()
            image_get.request.queries['page'] = pagination.page
            params = global_api.get(image_get.request)
            params.onchange = img_get_onchange
        }
        else if (image_patch.listen(e.target))
        {
            params = global_api.patch(image_patch.request, image_patch.data)
            params.onchange = img_patch_onchange
        }
        else if ((pagination.listen(e.target)))
        {
            if (!image_get.el) {
                image_get.option = image_get.options.all_images
                image_get.initialize(initial_query)
                image_get.prepare()
            }

            image_get.request.queries['page'] = pagination.page
            params = global_api.get(image_get.request)
            params.onchange = img_pagination_onchange
        }
        else params = null


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
