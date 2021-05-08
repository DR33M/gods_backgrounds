class Pagination {
    class_selector = '.'

    page = 1
    total_pages = 0
    first_page = 1
    last_page = 0
    step = 1

    class_names = {
        disabled: 'disabled',
    }

    html = {
        first: {
          class: 'pages-first',
          el: '',
          exec: this.first
        },
        previous: {
          class: 'pages-previous',
          el: '',
          exec: this.previous
        },
        current_page: {
          class: 'pages-current',
          el: '',
        },
        total_pages: {
          class: 'pages-total',
          el: '',
        },
        next: {
          class: 'pages-next',
          el: '',
          exec: this.next
        },
        last: {
          class: 'pages-last',
          el: '',
          exec: this.last
        },
    }

    constructor() {
        for (let key in this.html)
            this.html[key].el = document.getElementsByClassName(this.html[key].class)[0]
    }
    update_html() {
        if (this.page === this.first_page)
            this.html.first.el.classList.add(this.class_names.disabled)
        else this.html.first.el.classList.remove(this.class_names.disabled)

        if (this.page - this.step < this.first_page)
            this.html.previous.el.classList.add(this.class_names.disabled)
        else this.html.previous.el.classList.remove(this.class_names.disabled)

        this.html.current_page.el.innerHTML = this.page
        this.html.total_pages.el.innerHTML = this.total_pages

        if (this.page + this.step > this.last_page)
            this.html.next.el.classList.add(this.class_names.disabled)
        else this.html.next.el.classList.remove(this.class_names.disabled)

        if (this.page === this.last_page)
            this.html.last.el.classList.add(this.class_names.disabled)
        else this.html.last.el.classList.remove(this.class_names.disabled)
    }
    first(self) {
        self.page = self.first_page
        self.update_html()
    }
    previous(self) {
        if (self.page - self.step < self.first_page)
            return

        self.page = self.page - self.step
        self.update_html()
    }
    next(self) {
        if (self.page + self.step > self.last_page)
            return

        self.page = self.page + self.step
        self.update_html()
    }
    last(self) {
        self.page = self.last_page
        self.update_html()
    }
    update_total_pages(total_pages) {
        if (total_pages)
            this.total_pages = this.last_page = Number(total_pages)
    }
    onchange(request, total_pages) {
        if (request.xhr.readyState === 4) {
            this.update_total_pages(total_pages)
            this.update_html()
        }
    }
    listen(el) {
        for (let key in this.html) {
            if (el.closest(this.class_selector + this.html[key].class) && this.html[key].hasOwnProperty('exec')) {
                this.html[key].exec(this)
                return true
            }
        }
    }
}