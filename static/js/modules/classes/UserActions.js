class UserActions {
    currEl = {}

    display_switch = 'dn'
    modal_window_class = '.modal-window'
    el_visibility_class = '.el-visibility'

    show(el) {
        if (el)
            el.classList.remove(this.display_switch)
    }
    hide(el) {
        if (el)
            el.classList.add(this.display_switch)
    }
    toggle_visibility(el) {
        if (el)
            el.classList.toggle(this.display_switch)
    }

    modal_window(el) {
        this.currEl = el

        if ((this.currEl = this.currEl.closest(this.modal_window_class))) {
            if (this.currEl.dataset.window) {
                this.window = document.querySelector(this.currEl.dataset.window)
                if (this.window.dataset.dontCloseIf && el.closest(this.window.dataset.dontCloseIf)) {
                    return
                }
                this.toggle_visibility(this.window)
            }
        } else if (this.window) {
            this.hide(this.window)
        }
    }
    el_visibility(el) {
        this.currEl = el

        if ((this.currEl = this.currEl.closest(this.el_visibility_class)))
            if (this.currEl.dataset.el)
                this.toggle_visibility(document.querySelector(this.currEl.dataset.el))
    }
}