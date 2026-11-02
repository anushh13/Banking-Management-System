(function(){
  const rolePaths = {
    customer: "customer-dashboard.html",
    employee: "employee-dashboard.html",
    manager: "manager-dashboard.html",
    admin: "admin-dashboard.html"
  };
  window.allerAuth = {
    isLoggedIn(){ return !!sessionStorage.getItem("allerAccessToken"); },
    role(){ return sessionStorage.getItem("allerRole") || ""; },
    requireRole(expected){
      const role = this.role();
      if (!this.isLoggedIn() || (expected && role !== expected)) {
        window.location.href = "../login.html";
        return false;
      }
      return true;
    },
    dashboard(role){ return rolePaths[role] || "login.html"; },
    signOut(){ sessionStorage.clear(); localStorage.removeItem("allerAccessToken"); window.location.href = "../login.html"; }
  };
})();

/* =========================================
   USER MENU / LOGOUT
========================================= */

const userMenu = document.getElementById("userMenu");
const userMenuTrigger = document.getElementById("userMenuTrigger");
const logoutBtn = document.getElementById("logoutBtn");


/* Open / Close User Menu */

userMenuTrigger.addEventListener("click", function (event) {

    event.stopPropagation();

    userMenu.classList.toggle("active");

});


/* Close when clicking outside */

document.addEventListener("click", function (event) {

    if (!userMenu.contains(event.target)) {

        userMenu.classList.remove("active");

    }

});


/* Logout */

logoutBtn.addEventListener("click", function () {

    const confirmLogout = confirm(
        "Are you sure you want to logout?"
    );

    if (confirmLogout) {

        // Change this path to your actual login page
        window.location.href = "../login.html";

    }

});

/* =========================================
   PROFILE
========================================= */

const profileBtn = document.getElementById("profileBtn");

profileBtn.addEventListener("click", function () {

    // Change this to your actual profile page
    window.location.href = "security.html" || "customer/security.html" ;

});