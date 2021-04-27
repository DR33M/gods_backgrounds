function change_order(el) {
    if (el && el.hasAttributes('data-order')) {
        if (el.dataset.order === '-') {
            if (el.children[1])
                el.children[1].classList.toggle('rotate180')
            el.dataset.order = ''
        } else {
            if (el.children[1])
                el.children[1].classList.toggle('rotate180')
            el.dataset.order = '-'
        }
    }
}