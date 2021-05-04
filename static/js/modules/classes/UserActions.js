class UserActions {
    currEl = {}

    display_switch = 'dn'

    drop_list_class = 'drop-list'
    data_drop_list_id = 'data-drop-list-id'

    modal_window_class = 'modal-window'

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

    drop_list(el) {
        this.currEl = el

        if ((this.currEl = this.currEl.closest('[' + this.data_drop_list_id + ']')) && !this.currEl.closest('.' + this.drop_list_class)) {
            if (this.currEl) {
                let drop_list_el = document.getElementById(this.currEl.dataset.dropListId)
                this.toggle_visibility(drop_list_el)
            }
        }
    }

    modal_window(el) {
        this.currEl = el

        if (this.currEl.classList.contains(this.modal_window_class))
            if (this.currEl.dataset.window)
                this.toggle_visibility(document.getElementsByClassName(this.currEl.dataset.window)[0])
    }
    open(el) {
        this.currEl = el

        if (this.currEl.classList.contains(this.modal_window_class))
            if (this.currEl.dataset.window)
                this.show(document.getElementsByClassName(this.currEl.dataset.window)[0])
    }
    close(el) {
        this.currEl = el

        if (this.currEl.classList.contains(this.modal_window_class))
            if (this.currEl.dataset.window)
                this.hide(document.getElementsByClassName(this.currEl.dataset.window)[0])
    }
}