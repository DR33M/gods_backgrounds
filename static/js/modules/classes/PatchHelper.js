class PatchHelper {
    request = {}
    data = ''

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
            table: this.option.table,
            field: this.option.field,
            pk: this.pk
        }
        if (this.el.dataset.data)
            this.data = this.el.dataset.data
    }
    listen(el) {
        let listening_elements = {}

        for (let key in this.options)
            if ((this.el = el.closest(this.options[key].listen))) {
                //console.log(this.el)
                if (this.el.dataset.pk) {
                    this.set_pk()
                    this.option = this.options[key]
                    this.prepare()
                    //console.log(this.path)
                    //console.log(this.data)

                    listening_elements[key] = this.el
                }
            }

        return listening_elements
    }
}