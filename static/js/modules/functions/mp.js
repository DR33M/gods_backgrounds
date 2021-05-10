function render(image_data) {
    let image = document.getElementsByClassName('image-detail__img')[0]
    let imageAuthorName = document.querySelector('.account-info .full-name')
    let imageAuthorAvatar = document.querySelector('.image-detail .avatar')
    let imageCreatedTime = document.getElementsByClassName('created-time')[0]
    let imageColors = document.getElementsByClassName('colors-panel')[0]
    let colors = imageColors.querySelectorAll('.color')
    let colorUrl = colors[0].getAttribute('href').split('=')[0]
    let color = colors[0].cloneNode(true)

    image.setAttribute('src', image_data.image)
    imageAuthorAvatar.setAttribute('src', image_data.author.profile.photo)
    imageAuthorName.innerHTML = image_data.author.first_name + ' ' + image_data.author.last_name
    imageCreatedTime.innerHTML = new Date(image_data.created_at).toLocaleString('en-US')


    colors.forEach(e => e.remove())

    for(let i = 0; i < image_data.colors.length; i++) {
       color.setAttribute('href',colorUrl + '=' + image_data.colors[i].hex)
       color.style.background = image_data.colors[i].hex
       imageColors.append(color.cloneNode(true))
    }

    update_tags(image_data.tags)
}

function mp_onload(request) {
    if (request.xhr.status === 202 && request.xhr.responseText) {
        render(JSON.parse(request.xhr.responseText))
    }
}