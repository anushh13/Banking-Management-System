```javascript
/* =========================================================
   ALLER BANK - USER MENU
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const userMenu = document.getElementById("userMenu");
    const userMenuTrigger = document.getElementById("userMenuTrigger");
    const userDropdown = document.getElementById("userDropdown");
    const headerLogout = document.getElementById("headerLogout");

    if (!userMenu || !userMenuTrigger || !userDropdown) {
        return;
    }

    /* ---------------------------------------------
       OPEN / CLOSE USER MENU
    --------------------------------------------- */

    userMenuTrigger.addEventListener("click", function (event) {

        event.stopPropagation();

        const isOpen = userMenu.classList.toggle("open");

        userMenuTrigger.setAttribute(
            "aria-expanded",
            isOpen ? "true" : "false"
        );

    });


    /* ---------------------------------------------
       CLOSE WHEN CLICKING OUTSIDE
    --------------------------------------------- */

    document.addEventListener("click", function (event) {

        if (!userMenu.contains(event.target)) {

            userMenu.classList.remove("open");

            userMenuTrigger.setAttribute(
                "aria-expanded",
                "false"
            );

        }

    });


    /* ---------------------------------------------
       CLOSE WITH ESCAPE KEY
    --------------------------------------------- */

    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {

            userMenu.classList.remove("open");

            userMenuTrigger.setAttribute(
                "aria-expanded",
                "false"
            );

        }

    });


    /* ---------------------------------------------
       LOGOUT
    --------------------------------------------- */

    if (headerLogout) {

        headerLogout.addEventListener("click", function () {

            /*
             * Clear frontend session information.
             * This is safe for the current frontend prototype.
             */

            localStorage.removeItem("allerUser");
            localStorage.removeItem("allerRole");
            sessionStorage.clear();

            /*
             * Return to common ALLER BANK login page.
             */

            window.location.href = "../login.html";

        });

    }

});
```
