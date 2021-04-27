let imagesList = document.getElementsByClassName('images-list')[0]
let imageColumns = document.getElementsByClassName('image-column')
let imageItems = document.getElementsByClassName('image-item')

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
    let imageUpvoteButton = document.getElementsByClassName('upvote-button')[0]
    let imageDownloadButton = document.getElementsByClassName('download-button')[0]

    for (let i = 0; i < images_data.length; i++) {
        if (images_data[i].status === 0) {
            imageStatus.innerHTML = 'On moderation'
            imageStatus.classList.remove('dn')
        } else imageStatus.classList.add('dn')

        imageLink.setAttribute('href', images_data[i].slug)
        imagePreview.setAttribute('src', images_data[i].preview_image)
        imageAuthor.setAttribute('href', '/cabinet/' + images_data[i].author.username)
        imageRating.setAttribute('id', 'rating_' + images_data[i].id)
        imageRating.innerHTML = images_data[i].rating
        imageDownloads.innerHTML = images_data[i].downloads
        imageUpvoteButton.setAttribute('data-pk', images_data[i].id)
        imageUpvoteButton.setAttribute('data-counter', 'rating_' + images_data[i].id)
        imageDownloadButton.setAttribute('data-pk', images_data[i].id)

        if (i === images_data.length - 1)
            imagesList.append(imageItem)
        else imagesList.append(imageItem.cloneNode(true))
    }
}