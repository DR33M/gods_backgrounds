let imagesList = document.getElementsByClassName('images-list')[0]
let imageColumns = document.getElementsByClassName('image-column')
let imageItems = document.getElementsByClassName('image-item')

function change_order(el) {
    if (el) {
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

    let imageStatus = document.getElementsByClassName('image-status')[0]
    let imageLink = document.getElementsByClassName('image-link')[0]
    let imagePreview = document.getElementsByClassName('image-preview')[0]
    let imageAuthor = document.getElementsByClassName('author__account-link')[0]
    let imageRating = document.getElementsByClassName('rating')[0]
    let imageDownloads = document.getElementsByClassName('downloads')[0]
    let imageRatingButton = document.getElementsByClassName('rating-button')[0]
    let imageDownloadButton = document.getElementsByClassName('download-button')[0]

    for (let i = 0; i < images_data.length; i++) {
        if (images_data[i].status === 0) {
            imageStatus.innerHTML = 'On moderation'
            imageStatus.classList.remove('dn')
        } else imageStatus.classList.add('dn')

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
function sort_onload(xhr, sort) {
    if (xhr.responseText) {
        window.history.replaceState(null, null, sort.query_path)
        prepare_place()
        add_images(JSON.parse(xhr.responseText))
        arrange_images()
    }
}