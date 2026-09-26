document.addEventListener(
    "DOMContentLoaded",
    function () {

        const form =
            document.getElementById(
                "comic-form"
            );

        const button =
            document.getElementById(
                "generate-btn"
            );

        if (!form || !button) {
            return;
        }

        form.addEventListener(
            "submit",
            function () {

                button.disabled = true;

                button.textContent =
                    "Generating... Please wait";

            }
        );
    }
);