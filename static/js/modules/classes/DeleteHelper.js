class DeleteHelper {
    request = {}
    data = ''

    listening_elements = {}

    options = {
        image_delete: {
            paths: {
                moderator_panel: 'moderator-panel',
            },
            listen: '.delete-button',
            el: {},
        },
        ban_user: {
            paths: {},
            api_path: '/accounts/api/user/',
            listen: '.ban-button',
            el: {},
        },
    }

    option = {}

    set_pk() {
        this.option.paths['pk'] = this.option.el.dataset.pk
    }
    set_data(data) {
        if (data)
            this.data = data
    }
    prepare() {
        this.request = {
            paths: this.option.paths
        }

        this.set_data(this.option.el.dataset.data)
    }
    listen(el) {
        let is_delete = false
        let option_el

        for (let key in this.options) {
            if ((option_el = el.closest(this.options[key].listen))) {
                this.option = this.options[key]
                this.option.el = option_el
                this.prepare()
                if (this.option.el.dataset.pk)
                    this.set_pk()

                is_delete = true
            }
        }

        return is_delete
    }
}