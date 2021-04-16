document.addEventListener("DOMContentLoaded", function () {
    document.body.addEventListener('click', function (e) {
        if (currEl = e.target.closest('.upvote')) {
            if (currEl.dataset.pk) {
                $.ajax({
                    type: "GET",
                    async: true,
                    url: 'http://127.0.0.1:8000/rating/' + currEl.dataset.pk + '/1',
                    success: function(data) {
                        console.log(data)
                    },
                });
            }
        }
    })
})