class PatchHelper {
    request = {}
    data = ''

    listening_elements = {}

    options = {
        rating: {
            paths: {
                table: 'image',
                field: 'rating',
            },
            listen: '.rating-button',
        },
        downloads: {
            paths: {
                table: 'image',
                field: 'downloads',
            },
            listen: '.download',
        }
    }
    
    pk = ''
    el = {}
    option = {}

    set_pk() {
        this.option.paths['pk'] = this.el.dataset.pk
    }
    set_data(data) {
        if (data)
            this.data = this.el.dataset.data
    }
    prepare() {
        this.request = {
            paths: this.option.paths
        }

        this.set_data(this.el.dataset.data)
    }
    listen(el) {
        let is_patch = false

        for (let key in this.options)
            if ((this.el = el.closest(this.options[key].listen))) {
                this.option = this.options[key]
                this.prepare()
                if (this.el.dataset.pk)
                    this.set_pk()

                is_patch = true
            }

        return is_patch
    }
}