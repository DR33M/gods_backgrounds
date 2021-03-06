document.addEventListener("DOMContentLoaded", function () {
    function main() {
        let global_api = new GlobalApi()
        let image_get = new GetHelper()
        let image_patch = new PatchHelper()
        let user_actions = new UserActions()
        let pagination = new Pagination()
        let image_view = new ImageView(user_actions, number_of_columns, image_get, image_patch)

        let request, params

        let pathname = window.location.pathname.split('/').filter(function (el) {
            return el.length != 0
        })
        let view = pathname[0]
        let username = pathname[1]
        let user_id = Number(document.getElementsByClassName('user_id')[0].dataset.userId)
        pathname = '/' + view + '/' + username

        let initial_query = {
            in: {
                'author': [user_id,]
            }
        }

        pagination.page = page
        pagination.update_total_pages(total_pages)
        pagination.update_html()

        let img_get_onchange = function () {
            image_view.onchange(request)
            pagination.first()
            pagination.onchange(request, image_view.response_text['total_pages'])
            set_search_params_uniq(pathname + global_api.last_path)
        }
        let img_pagination_onchange = function () {
            if (pagination.onchange(request, image_view.response_text['total_pages'])) {
                set_search_params_uniq(pathname + global_api.last_path)
                image_view.html.arrange(pagination.response_text['images'])
            }
        }
        let img_patch_onchange = function () {
            image_view.onchange(request)
        }

        document.body.addEventListener('click', function (e) {
            if (image_get.listen(e.target, initial_query) && Object.keys(image_get.listening_elements).length) {
                pagination.first()
                image_get.request.queries['page'] = pagination.page
                params = global_api.get(image_get.request)
                params.onchange = img_get_onchange
            } else if (image_patch.listen(e.target)) {
                params = global_api.patch(image_patch.request, image_patch.data)
                params.onchange = img_patch_onchange
            } else if ((pagination.listen(e.target))) {
                if (!image_get.el) {
                    image_get.option = image_get.options.all_images
                    image_get.initialize(initial_query)
                    image_get.prepare()
                }
                image_get.request.queries['page'] = pagination.page
                params = global_api.get(image_get.request)
                params.onchange = img_pagination_onchange
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
    }

    if (typeof total_pages !== 'undefined' &&
        typeof number_of_columns !== 'undefined' &&
        typeof images_list !== 'undefined' &&
        typeof page !== 'undefined')
        main()
})