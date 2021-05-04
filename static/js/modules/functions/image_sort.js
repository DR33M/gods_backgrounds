let not_found = document.getElementsByClassName('not-found')[0]

let imagesList = document.getElementsByClassName('images-list')[0]
let imageColumns = document.getElementsByClassName('image-column')
let imageItems = document.getElementsByClassName('image-item')

let desktop = document.getElementsByClassName('ratio-desktop')[0]
let phone = document.getElementsByClassName('ratio-phone')[0]
let screen_filter_name = document.getElementById('screen-filter-name')

function get_clean_tags(string) {
    if (typeof string !== 'string')
        return ''

    let tmp = string.split(',')
    let tags_list = []

    for (let i = 0; i < tmp.length; i++) {
        tmp[i] = tmp[i].toLowerCase()
        tmp[i] = tmp[i].replace(/([a-zA-Z0-9])\s([a-zA-Z0-9])/g, "$1-$2")
        tmp[i] = tmp[i].replace(/\s/g, '')
        if (tmp[i] && !tmp[i].match(/[\!\#\$\%\&\'\*\+\/\=\\\?\^\_\`\{\|\}\~\"\,\:\;\<\>\@\[\]]+/g))
            tags_list.push(tmp[i])
    }

    tags_list.sort(function(a, b){
        if(a < b) return -1
        if(a > b) return 1
        return 0
    })
    string = tags_list.join('-')

    return string
}
function change_order(el) {
    if (el) {
        //console.log(el)
        if (!el.classList.contains('sort-active')) {
            let sort_items = document.getElementsByClassName('sort-active')
            for (let i = 0; i < sort_items.length; i++)
                sort_items[i].classList.remove('sort-active')

            el.classList.add('sort-active')
        }

        if (el.hasAttributes('data-order')) {
            if (el.dataset.order === '-') {
                el.dataset.order = ' '
            } else {
                el.dataset.order = '-'
            }

            if (el.children[1])
                el.children[1].classList.toggle('rotate0')
        }
    }
}
function arrange_images() {
    if (!imageColumns || !imageItems)
        return

    for (let i = 0; i < imageItems.length; i++)
        imageColumns[i % 4].append(imageItems[i]);
}
function prepare_place() {
    if (!imagesList || !imageColumns)
        return

    imagesList.append(imageItems[0].cloneNode(true))

    for (let i = 0; i < imageColumns.length; i++)
        imageColumns[i].innerHTML = '';
}
function add_images(images_data) {
    console.log(images_data)
    let imageItem = document.getElementsByClassName('image-item')[0]

    if (!imagesList || !imageColumns || !imageItem)
        return

    let vote

    let imageStatus = document.getElementsByClassName('image-status')[0]
    let imageLink = document.getElementsByClassName('image-link')[0]
    let imagePreview = document.getElementsByClassName('image-preview')[0]
    let imageAuthor = document.getElementsByClassName('author__account-link')[0]
    let imageRating = document.getElementsByClassName('rating')[0]
    let imageDownloads = document.getElementsByClassName('downloads')[0]
    let imageRatingButton = document.getElementsByClassName('rating-button')[0]
    let imageDownloadButton = document.getElementsByClassName('download-button')[0]

    for (let i = 0; i < images_data.length; i++) {
        vote = 'default-vote'

        if (images_data[i].status === 0) {
            imageStatus.innerHTML = 'On moderation'
            imageStatus.classList.remove('dn')
        } else imageStatus.classList.add('dn')

        if (images_data[i]['followers'] && images_data[i]['followers'][0] && images_data[i]['followers'][0]['vote']) {
            switch (images_data[i]['followers'][0]['vote']) {
                case -1:
                    vote = 'downvote'
                    break
                case 1:
                    vote = 'upvote'
                    break
            }
            //console.log(images_data[i]['followers'][0]['vote'])
        }

        for (let j = 0; j < imageRatingButton.children.length; j++) {
            if (imageRatingButton.children[j].classList.contains(vote))
                imageRatingButton.children[j].classList.remove('vote-inactive')
            else if (!imageRatingButton.children[j].classList.contains('vote-inactive'))
                imageRatingButton.children[j].classList.add('vote-inactive')
        }

        imageLink.setAttribute('href', '/detail/' + images_data[i].slug)
        imagePreview.setAttribute('src', images_data[i].preview_image)
        imageAuthor.setAttribute('href', '/cabinet/' + images_data[i].author.username)
        imageRating.setAttribute('id', 'rating_' + images_data[i].id)
        imageRatingButton.setAttribute('data-pk', images_data[i].id)
        imageRatingButton.setAttribute('data-counter', 'rating_' + images_data[i].id)
        imageDownloadButton.setAttribute('data-pk', images_data[i].id)

        imageRating.innerHTML = images_data[i].rating
        imageDownloads.innerHTML = images_data[i].downloads

        if (i === images_data.length - 1)
            imagesList.append(imageItem)
        else imagesList.append(imageItem.cloneNode(true))
    }
}
function image_GET_onload(request, elements, image_get, user_actions) {
    if (request.xhr.readyState !== 4) return;

    //console.log(this.status, this.statusText)
    if (request.xhr.status === request.HTTP_404_NOT_FOUND) {
        //console.log(not_found)
        user_actions.modal_window(not_found)
    } else if (request.xhr.status === request.HTTP_200_OK && request.xhr.responseText.length) {
        set_search_params()
        prepare_place()
        add_images(JSON.parse(request.xhr.responseText))
        arrange_images()
        //console.log(elements)

        for (let key in elements) {
            //console.log(key)
            //console.log(elements[key])
            switch (image_get.options[key]) {
                case image_get.options['created_at']: change_order(elements[key]); break
                case image_get.options['downloads']: change_order(elements[key]); break
                case image_get.options['rating']: change_order(elements[key]); break
                case image_get.options['ratio']:
                    screen_filter_name.innerText = elements[key].innerText
                    desktop.classList.remove('active')
                    phone.classList.remove('active')
                    elements[key].classList.add('active')
                    break
            }
        }
    }
}