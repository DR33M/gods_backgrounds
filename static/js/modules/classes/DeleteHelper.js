class DeleteHelper {
    request = {}
    listening_elements = {}

    options = {
        image_delete: {
            paths: {
                moderator_panel: 'moderator-panel',
            },
            listen: '.delete-button',
        },
    }

    pk = ''
    el = {}
    option = {}

    set_pk() {
        console.log(this.option)
        this.option.paths['pk'] = this.el.dataset.pk
    }
    prepare() {
        this.request = {
            paths: this.option.paths
        }
        if (this.el.dataset.data)
            this.data = this.el.dataset.data
    }
    listen(el) {
        let is_delete = false
        for (let key in this.options)
            if ((this.el = el.closest(this.options[key].listen))) {
                this.option = this.options[key]
                this.listening_elements[key] = this.el
                is_delete = true
                if (this.el.dataset.pk) {
                    this.set_pk()
                }
                this.prepare()
            }

        return is_delete
    }
}