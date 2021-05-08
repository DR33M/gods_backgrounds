class PatchHelper {
    request = {}
    data = ''

    listening_elements = {}

    options = {
        rating: {
            table: 'image',
            field: 'rating',
            listen: '.rating-button',
        },
        downloads: {
            table: 'image',
            field: 'downloads',
            listen: '.download',
        }
    }
    
    pk = ''
    el = {}
    option = {}

    set_pk() {
        this.pk = this.el.dataset.pk
    }
    prepare() {
        this.request = {
            paths: {
                table: this.option.table,
                field: this.option.field,
                pk: this.pk
            },
        }
        if (this.el.dataset.data)
            this.data = this.el.dataset.data
    }
    listen(el) {
        let is_patch = false

        for (let key in this.options)
            if ((this.el = el.closest(this.options[key].listen))) {
                //console.log(this.el)
                if (this.el.dataset.pk) {
                    this.set_pk()
                    this.option = this.options[key]
                    this.prepare()
                    //console.log(this.path)
                    //console.log(this.data)

                    this.listening_elements[key] = this.el
                    is_patch = true
                }
            }

        return this.listening_elements
    }
}