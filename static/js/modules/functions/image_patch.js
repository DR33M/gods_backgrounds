function update_counter(el, count) {
    let counter = document.getElementById(el.dataset.counter)

    if (counter)
        counter.innerText = count
}
function rating_onload(request, image_patch, el) {
    let response = JSON.parse(request.xhr.responseText)

    if (response) {
        let children = el.children, vote = 'default-vote'

        switch (response['vote']) {
            case -1: vote = 'downvote'; break
            case 0: vote = 'default-vote'; break
            case 1: vote = 'upvote'; break
        }

        for (let i = 0; i < children.length; i++) {
            if (children[i].classList.contains(vote))
                children[i].classList.remove('vote-inactive')
            else children[i].classList.add('vote-inactive')
        }

        update_counter(el, response['count'])
    }
}
function downloads_onload(request, image_patch, el) {
    el.classList.add(image_patch.downloads.disabled)
    if (request.xhr.status === request.HTTP_202_ACCEPTED)
        update_counter(el, request.xhr.responseText)
}
function image_PATCH_onload(request, elements, image_patch) {
    if (request.xhr.readyState !== 4) return;

    //console.log(this.status, this.statusText)
    if (request.xhr.status === request.HTTP_202_ACCEPTED && request.xhr.responseText.length) {
        for (let key in elements) {
            //console.log(key)
            //console.log(elements[key])
            switch (image_patch.options[key]) {
                case image_patch.options['rating']:
                    rating_onload(request, image_patch, elements[key]);
                    break
                case image_patch.options['downloads']:
                    downloads_onload(request, image_patch, elements[key]);
                    break
            }
        }
    }
}