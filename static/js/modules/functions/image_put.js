function rating_onload(xhr, image_put, request, el) {
    let response = JSON.parse(xhr.responseText)

    if (xhr.status === request.HTTP_202_ACCEPTED) {
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

        image_put.update_counter(el, response['count'])
    }
}
function downloads_onload(xhr, image_put, request, el) {
    el.classList.add(image_put.downloads.disabled)
    if (xhr.status === request.HTTP_202_ACCEPTED)
        image_put.update_counter(el, xhr.responseText)
}
