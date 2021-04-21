document.addEventListener("DOMContentLoaded", function () {
    arrange_images();
    let imageApi = new ImageApi();

    document.body.addEventListener('click', function (e) {
        imageApi.listener_logic(e)
    })
})