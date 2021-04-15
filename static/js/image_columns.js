document.addEventListener("DOMContentLoaded", function () {
    let imagesColumns = document.getElementsByClassName('image-column')
    let imagesItems = document.getElementsByClassName('image-item')

    for (let i = 0; i < imagesItems.length; i++)
        imagesColumns[i % 4].append(imagesItems[i]);
})