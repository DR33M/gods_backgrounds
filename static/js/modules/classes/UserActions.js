class UserActions {
    currEl = {}

    display_switch = 'dn'

    drop_list_class = 'drop-list'
    data_drop_list_id = 'data-drop-list-id'

    toggle_visibility(el) {
        if (el)
            el.classList.toggle(this.display_switch)
    }

    drop_list(e) {
        if ((this.currEl = e.target.closest('[' + this.data_drop_list_id + ']')) && !e.target.closest('.' + this.drop_list_class)) {
            if (this.currEl) {
                let drop_list_el = document.getElementById(this.currEl.dataset.dropListId)
                this.toggle_visibility(drop_list_el)
            }
        }
    }
}