class PatchHelper {
    request = {}
    data = ''

    disabled_class = 'disabled'

    options = {
        approve_image: {
            paths: {
                table: 'image',
                extra_action: 'mp_approve',
            },
            listen: '.approve-button',
            el: {},
        },
        rating: {
            paths: {
                table: 'image',
                extra_action: 'change_rating',
            },
            listen: '.rating-button',
            el: {},
        },
        downloads: {
            paths: {
                table: 'image',
                extra_action: 'add_download',
            },
            listen: '.download',
            el: {},
        }
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
        let is_patch = false
        let option_el

        for (let key in this.options) {
            if ((option_el = el.closest(this.options[key].listen)) && !option_el.classList.contains(this.disabled_class)) {
                this.option = this.options[key]
                this.option.el = option_el
                this.prepare()
                if (this.option.el.dataset.pk)
                    this.set_pk()

                is_patch = true
            }
        }

        return is_patch
    }
}