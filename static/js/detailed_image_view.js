document.addEventListener("DOMContentLoaded", function () {
    arrange_images();
    let imageApi = new ImageSortApi();
    imageApi.image_id_class = 'upvote'

    document.body.addEventListener('click', function (e) {
        imageApi.listener_logic(e)
    })
})