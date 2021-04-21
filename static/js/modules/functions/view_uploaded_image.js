function uploadImageMain() {
    let imgInp = document.getElementById("input-image"),
        previews = document.getElementsByClassName("input-image-preview");

    if (imgInp)
        imgInp.addEventListener("change", function () {
            changeImage(this);
        });

    function changeImage(input) {
        let reader;

        if (input.files && input.files[0]) {
            reader = new FileReader();

            reader.onload = function (e) {
                for (let preview of previews) {
                    preview.setAttribute('src', e.target.result);
                }
            }

            reader.readAsDataURL(input.files[0]);
        }
    }
}