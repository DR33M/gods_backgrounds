document.addEventListener("DOMContentLoaded", function () {
    arrange_images();
    let imageApi = new ImageApi();
    let userActions = new UserActions();

    document.body.addEventListener('click', function (e) {
        imageApi.listener_logic(e)
        userActions.drop_list(e);
    })
})