class Votes {
    list = {
        '-1': 'downvote',
        '0': 'default-vote',
        '1': 'upvote'
    }
    current = this.list['0']

    inactive_class = 'vote-inactive'

    set_current(vote) {
        for (let key in this.list)
            if (Number(key) === Number(vote))
                this.current = this.list[key]
    }
}
class SearchHTML {
    get_tag_list(string) {
        if (typeof string === 'string')
            return  string.split(',')
        return false
    }
    format_tag(tag) {
        if (typeof tag !== 'string')
            return ''

        tag = tag.toLowerCase()
        tag = tag.replace(/([a-zA-Z0-9])\s([a-zA-Z0-9])/g, "$1-$2") //tag name => tag-name
        tag = tag.replace(/\s/g, '') //  t a  gname => tagname

        return tag
    }
    validate_tag(tag) {
        //simple check whether there is prohibited symbols
        if (tag && !tag.match(/[!#$%&'*+\/=\\?^_`{|}~",:;<>@\[\]]+/g))
            return true
    }
    sort_by_alphabet(clean_tags_list) {
        clean_tags_list.sort(function(a, b){
            if(a < b) return -1
            if(a > b) return 1
            return 0
        })

        return clean_tags_list
    }
    get_slug(tags_string) {
        let tags_list = this.get_tag_list(tags_string)
        let clean_tags_list = []

        for (let i = 0; i < tags_list.length; i++) {
            tags_list[i] = this.format_tag(tags_list[i])
            if (this.validate_tag(tags_list[i]))
                clean_tags_list.push(tags_list[i])
        }

        clean_tags_list = this.sort_by_alphabet(clean_tags_list)
        return clean_tags_list.join('-')
    }
}
class SortingHTML {
    asc = '-'
    desc = ' '

    class_names = {
        sort_active: 'sort-active',
        date_order: 'data-order',
        rotate_zero: 'rotate0'
    }

    remove_sort_active_all() {
        let sort_items = document.getElementsByClassName(this.class_names.sort_active)
            for (let i = 0; i < sort_items.length; i++)
                sort_items[i].classList.remove(this.class_names.sort_active)

    }
    change_order(elem) {
        if (!elem.classList.contains(this.class_names.sort_active)) {
            this.remove_sort_active_all()
            elem.classList.add(this.class_names.sort_active)
        }

        if (elem.hasAttribute(this.class_names.date_order)) {
            if (elem.dataset.order === this.asc) {
                elem.dataset.order = this.desc
            } else {
                elem.dataset.order = this.asc
            }

            if (elem.children[1])
                elem.children[1].classList.toggle(this.class_names.rotate_zero)
        }
    }
}
class FilterHTML {
    class_names = {
        active: 'active'
    }
    
    constructor() {
        this.previous_ratio_active = document.getElementsByClassName('ratio-all')[0]
        this.screen_filter_name = document.getElementById('screen-filter-name')
    }

    change_ratio(elem) {
        this.screen_filter_name.innerText = elem.innerText
        this.previous_ratio_active.classList.remove(this.class_names.active)
        elem.classList.add(this.class_names.active)
        this.previous_ratio_active = elem
    }
}
class ImageUpdateHTML {
    class_names = {
        downloaded: 'downloaded'
    }

    constructor() {
        this.votes = new Votes()
    }
    counter(el, count) {
        let counter = document.getElementById(el.dataset.counter)

        if (counter)
            counter.innerText = String(count)
    }
    rating(elem, vote) {
        let children = elem.children

        this.votes.set_current(vote)

        for (let i = 0; i < children.length; i++)
            if (children[i].classList.contains(this.votes.current))
                children[i].classList.remove(this.votes.inactive_class)
            else children[i].classList.add(this.votes.inactive_class)
    }
    downloads(elem, disable=true) {
        if (disable)
            elem.classList.add(this.class_names.downloaded)
    }
}
class ImageHTML {
    class_names = {
        disabled: 'dn'
    }
    
    image = {
        original_list: {
            class: 'images-list',
            el: {}
        },
        column: {
            class: 'image-column',
            el: {}
        },
        item: {
            class: 'image-item',
            el: {},
        },
        status: {
            parent: 'item',
            class: 'image-status',
            el: {},
            default: {
                status: ''
            },
        },
        link: {
            parent: 'item',
            class: 'image-link',
            el: {},
            default: {
                link: ''
            },
        },
        preview: {
            parent: 'item',
            class: 'image-preview',
            el: {},
            default: {
                preview: ''
            },
        },
        author: {
            parent: 'item',
            class: 'author__account-link',
            el: {},
            default: {
                author: ''
            },
        },
        author_avatar: {
            parent: 'item',
            class: 'avatar',
            el: {},
            default: {
                'avatar': ''
            },
        },  
        author_name: {
            parent: 'item',
            class: 'full-name',
            el: {},
            default: {
                name: ''
            },
        },
        rating: {
            parent: 'item',
            class: 'rating',
            el: {},
            default: {
                count: '0',
            },
        },
        rating_button: {
            parent: 'item',
            class: 'rating-button',
            el: {},
            default: {
                id: '',
                counter: '',
            },
        },
        downloads: {
            parent: 'item',
            class: 'downloads',
            el: {},
            default: {
                count: '0',
            },
        },
        download_button: {
            parent: 'item',
            class: 'download-button',
            el: {},
            default: {
                id: '',
                counter: '',
                download: '',
                href: false,
            },
        },
    }

    fill_image_object() {
        for (let key in this.image)
            if (this.image[key]['parent']) {
                this.image[key].parent = this.image[this.image[key].parent]
                this.image[key].el = this.image[key].parent.el.getElementsByClassName(this.image[key].class)[0]
            } else this.image[key].el = document.getElementsByClassName(this.image[key].class)[0]
    }
    constructor(number_of_columns) {
        this.votes = new Votes()

        this.number_of_columns = number_of_columns
        this.image_columns = []

        this.fill_image_object()
    }

    clear_image_list() {
        this.image.original_list.innerHTML = ''
    }
    clear_image_column(image_column) {
        image_column.innerHTML = ''
    }
    choose_vote_svg(image_data) {
        this.votes.current = this.votes.list['0']

        if (image_data['followers'] && image_data['followers'][0] && image_data['followers'][0]['vote'])
            this.votes.set_current(image_data['followers'][0]['vote'])

        for (let i = 0; i < this.image.rating_button.el.children.length; i++) {
            if (this.image.rating_button.el.children[i].classList.contains(this.votes.current))
                this.image.rating_button.el.children[i].classList.remove(this.votes.inactive_class)
            else if (!this.image.rating_button.el.children[i].classList.contains(this.votes.inactive_class))
                this.image.rating_button.el.children[i].classList.add(this.votes.inactive_class)
        }
    }
    choose_status(image_data) {
        if (image_data.status === 0)
            this.image.status.el.classList.remove(this.class_names.disabled)
        else if (!this.image.status.el.classList.contains(this.class_names.disabled))
            this.image.status.el.classList.add(this.class_names.disabled)
    }
    set_image_link(image_data) {
        if (image_data['slug'])
            this.image.link.el.setAttribute('href', '/detail/' + image_data['slug'])
        else
            this.image.link.el.setAttribute('href', this.image.link.default.link)
    }
    set_image_preview(image_data) {
        if (image_data['preview_image'])
            this.image.preview.el.setAttribute('src', image_data['preview_image'])
        else this.image.preview.el.setAttribute('src', this.image.preview.default.preview)
    }
    set_image_author(image_data) {
        this.image.author.el.setAttribute('href', this.image.author.default['author'])
        this.image.author_name.el.innerText = this.image.author_name.default['name']
        this.image.author_avatar.el.setAttribute('src', this.image.author_avatar.default['avatar'])

        if (image_data['author'] ) {
            if (image_data['author']['username']) {
                this.image.author.el.setAttribute('href', '/cabinet/' + image_data['author']['username'])
            }
            if (image_data['author']['first_name'] && image_data['author']['last_name']) {
                this.image.author_name.el.innerText = image_data['author']['first_name'] + ' ' + image_data['author']['last_name']
            }
            if (image_data['author']['profile'] && image_data['author']['profile']['photo']) {
                this.image.author_avatar.el.setAttribute('src', image_data['author']['profile']['photo'])
            }
        }
    }
    set_image_rating(image_data) {
        if (image_data['id'])
            this.image.rating.el.setAttribute('id', 'rating_' + image_data['id'])
        else this.image.rating.el.setAttribute('id', this.image.rating.default['id'])
        if (image_data['rating'] !== '')
            this.image.rating.el.innerHTML = image_data['rating']
        else this.image.rating.el.innerHTML = this.image.rating.default['count']
    }
    set_image_rating_button(image_data) {
        if (image_data['id']) {
            this.image.rating_button.el.setAttribute('data-pk', image_data['id'])
            this.image.rating_button.el.setAttribute('data-counter', 'rating_' + image_data['id'])
        } else {
            this.image.rating_button.el.setAttribute('data-pk', this.image.rating.default['id'])
            this.image.rating_button.el.setAttribute('data-counter', this.image.rating.default['counter'])
        }
    }
    set_image_downloads(image_data) {
        if (image_data['id'])
            this.image.downloads.el.setAttribute('id', 'downloads_' + image_data['id'])
        else this.image.downloads.el.setAttribute('id', this.image.downloads.default['id'])
        if (image_data['downloads'] !== '')
            this.image.downloads.el.innerHTML = image_data['downloads']
        else this.image.downloads.el.innerHTML = this.image.downloads.default['count']
    }
    set_image_download_button(image_data) {
        if (image_data['id']) {
            this.image.download_button.el.setAttribute('href', image_data['image'])
            this.image.download_button.el.setAttribute('download', image_data['title'] + '.' + image_data['extension'])
            this.image.download_button.el.setAttribute('data-pk', image_data['id'])
            this.image.download_button.el.setAttribute('data-counter', 'downloads_' + image_data['id'])
        } else {
            if (!this.image.download_button.default['href'])
                this.image.download_button.el.removeAttribute('href')
            this.image.download_button.el.setAttribute('download', this.image.download_button.default['download'])
            this.image.download_button.el.setAttribute('data-pk', this.image.download_button.default['id'])
            this.image.download_button.el.setAttribute('data-counter', this.image.download_button.default['counter'])
        }
    }
    prepare(images_data) {
        this.clear_image_list()

        let image_column
        let image_item

        for (let i = 0; i < this.number_of_columns; i++) {
            if (this.image_columns[i])
                this.clear_image_column(this.image_columns[i])
            image_column = this.image.column.el.cloneNode()
            image_column.classList.remove(this.class_names.disabled)
            this.image_columns.push(image_column)
        }

        for (let i = 0; i < images_data.length; i++) {
            this.choose_vote_svg(images_data[i])
            this.choose_status(images_data[i])
            this.set_image_link(images_data[i])
            this.set_image_preview(images_data[i])
            this.set_image_author(images_data[i])
            this.set_image_rating(images_data[i])
            this.set_image_rating_button(images_data[i])
            this.set_image_downloads(images_data[i])
            this.set_image_download_button(images_data[i])
            image_item = this.image.item.el.cloneNode(true)
            image_item.classList.remove(this.class_names.disabled)
            this.image_columns[i % this.number_of_columns].append(image_item)
        }
    }
    arrange(images_data) {
        this.prepare(images_data)

        this.image.original_list.el.classList.remove(this.class_names.disabled)
        for (let i = 0; i < this.number_of_columns; i++) {
            this.image.original_list.el.append(this.image_columns[i])
        }

        //console.log(images_data)
    }
}
class ImageView {
    request = {}
    response_text = {}
    elements = {}
    image_get = {}

    constructor(user_actions, number_of_columns, image_get, image_patch) {
        this.user_actions = user_actions
        this.update = new ImageUpdateHTML()
        this.html = new ImageHTML(number_of_columns)
        this.search = new SearchHTML()
        this.sorting = new SortingHTML()
        this.filter = new FilterHTML()
        if (image_get)
            this.image_get = image_get
        if (image_patch)
            this.image_patch = image_patch

        this.not_found = document.getElementsByClassName('not-found')[0]
    }
    onchange(request, elements) {
        if (request.xhr.readyState !== 4) return;

        if (request.xhr.status === request.HTTP_404_NOT_FOUND) {
            this.user_actions.modal_window(this.not_found)
        } else if (request.xhr.responseText.length) {
            this.response_text = JSON.parse(request.xhr.responseText)
            this.request = request
            this.elements = elements

            if (request.xhr.status === request.HTTP_200_OK) {
                this.html.arrange(this.response_text['images'])

                for (let key in this.image_get.listening_elements)
                    switch (this.image_get.options[key]) {
                        case this.image_get.options['created_at']:
                            this.sorting.change_order(this.image_get.listening_elements[key])
                            break
                        case this.image_get.options['downloads']:
                            this.sorting.change_order(this.image_get.listening_elements[key])
                            break
                        case this.image_get.options['rating']:
                            this.sorting.change_order(this.image_get.listening_elements[key])
                            break
                        case this.image_get.options['ratio']:
                            this.filter.change_ratio(this.image_get.listening_elements[key])
                            break;
                    }

                this.image_get.flush_listening_elements()
            } else if (request.xhr.status === request.HTTP_202_ACCEPTED) {
                switch (this.image_patch.options[key]) {
                    case this.image_patch.options['rating']:
                        this.update.rating(this.image_patch.el, this.response_text['vote'])
                        this.update.counter(this.image_patch.el, this.response_text['count'])
                        break
                    case this.image_patch.options['downloads']:
                        this.update.downloads(this.image_patch.el)
                        this.update.counter(this.image_patch.el, this.response_text['count'])
                        break
                }
            }
         }
    }
}