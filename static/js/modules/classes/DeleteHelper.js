class DeleteHelper {
    request = {}
    data = ''

    options = {
        delete: {
            paths: {
                table: 'image',
                extra_action: 'delete',
            },
            listen: '.delete-button',
            el: {},
        },
        ban_user: {
            paths: {
                api: '/accounts/api',
                user: 'user'
            },
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