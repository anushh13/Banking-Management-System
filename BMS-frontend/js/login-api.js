const loginFormV2 = document.getElementById("loginForm");
if (loginFormV2) {
  loginFormV2.addEventListener("submit", async (e) => {
    e.preventDefault();
    const role = document.getElementById("loginRole")?.value || "customer";
    const userId = document.getElementById("userId")?.value.trim();
    const password = document.getElementById("password")?.value;
    if (!userId || !password) return;
    try {
      const result = await allerApi.login({ userId, password, role });
      sessionStorage.setItem("allerAccessToken", result.data.accessToken);
      sessionStorage.setItem("allerRole", result.data.user.role.toLowerCase());
      window.location.href = `./${result.data.user.role.toLowerCase()}/dashboard.html`;
    } catch (err) {
      alert(err.message || "Unable to sign in");
    }
  });
}
