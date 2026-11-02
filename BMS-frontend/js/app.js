document.addEventListener("DOMContentLoaded", () => {
  const $ = (s, r=document) => r.querySelector(s);
  const $$ = (s, r=document) => [...r.querySelectorAll(s)];

  // Public mobile navigation
  const menuBtn = $(".mobile-menu-btn");
  if(menuBtn){
    menuBtn.addEventListener("click", () => $(".public-header")?.classList.toggle("mobile-open"));
  }

  // Role-aware login
  const roleButtons = $$(".role-option");
  roleButtons.forEach(btn => btn.addEventListener("click", () => {
    roleButtons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    const role = btn.dataset.role;
    const hidden = $("#loginRole");
    if(hidden) hidden.value = role;
  }));

  const loginForm = $("#loginForm");
  if(loginForm){
    loginForm.addEventListener("submit", e => {
      e.preventDefault();
      const role = $("#loginRole")?.value || "customer";
      const target = {
        customer: "customer-dashboard.html",
        employee: "employee-dashboard.html",
        manager: "manager-dashboard.html",
        admin: "admin-dashboard.html"
      }[role];
      if(target) window.location.href = target;
    });
  }

  $$("[data-toggle-password]").forEach(btn => btn.addEventListener("click", () => {
    const input = btn.closest(".input-wrap")?.querySelector("input");
    if(!input) return;
    input.type = input.type === "password" ? "text" : "password";
    btn.innerHTML = input.type === "password" ? '<i class="fa-regular fa-eye"></i>' : '<i class="fa-regular fa-eye-slash"></i>';
  }));

  $$("[data-demo-alert]").forEach(el => el.addEventListener("click", e => {
    e.preventDefault();
    showToast(el.dataset.demoAlert || "This action is ready to connect to the backend.");
  }));

  // Dashboard sidebar
  const sidebar = $("#sidebar");
  $("[data-sidebar-open]")?.addEventListener("click", () => sidebar?.classList.add("open"));
  $("[data-sidebar-close]")?.addEventListener("click", () => sidebar?.classList.remove("open"));
  $$(".nav-item").forEach(item => item.addEventListener("click", () => {
    $$(".nav-item").forEach(n => n.classList.remove("active"));
    item.classList.add("active");
    if(window.innerWidth < 800) sidebar?.classList.remove("open");
  }));

  $$("[data-logout]").forEach(btn => btn.addEventListener("click", () => {
    sessionStorage.removeItem("allerRole");
    window.location.href = (location.pathname.includes("/customer/") || location.pathname.includes("/staff/") || location.pathname.includes("/branch-manager/") || location.pathname.includes("/admin/")) ? "../login.html" : "login.html";
  }));

  // Chatbot: intentionally a frontend demonstration; connect to a secured backend AI/service API.
  const chatbot = $("#chatbot");
  const chatToggle = $("[data-chat-toggle]");
  const chatClose = $("[data-chat-close]");
  const chatBody = $("[data-chat-body]");
  const chatForm = $("[data-chat-form]");
  const chatInput = $("[data-chat-input]");

  chatToggle?.addEventListener("click", () => chatbot?.classList.toggle("open"));
  chatClose?.addEventListener("click", () => chatbot?.classList.remove("open"));

  const addMessage = (text, type="bot") => {
    if(!chatBody) return;
    const div = document.createElement("div");
    div.className = type === "user" ? "user-message" : "bot-message";
    div.textContent = text;
    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
  };

  const botReply = text => {
    const t = text.toLowerCase();
    if(t.includes("pending") || t.includes("task")) return "I can guide you to the current task or approval queue. For production, this response should come from the authenticated role and live workflow API.";
    if(t.includes("security")) return "ALLER BANK's UI is designed around MFA, role-based access, maker-checker controls, fraud/risk checks and audit trails. Never share OTPs, PINs or passwords.";
    if(t.includes("service") || t.includes("request")) return "Service requests can be registered, categorised, prioritised, assigned, tracked and escalated according to SLA.";
    if(t.includes("transfer")) return "A transfer should pass authentication, validation, risk/fraud checks, limits, approval where required, debit/credit processing, GL posting, notification and audit.";
    return "I can help with accounts, payments, loans, cards, KYC, service requests, security and dashboard navigation. Connect this widget to your secured AI/service API for live answers.";
  };

  chatForm?.addEventListener("submit", e => {
    e.preventDefault();
    const text = chatInput?.value.trim();
    if(!text) return;
    addMessage(text, "user");
    chatInput.value = "";
    setTimeout(() => addMessage(botReply(text)), 350);
  });

  $$("[data-chat-prompt]").forEach(btn => btn.addEventListener("click", () => {
    const text = btn.dataset.chatPrompt;
    addMessage(text, "user");
    setTimeout(() => addMessage(botReply(text)), 300);
  }));

  // Small toast utility
  function showToast(message){
    let toast = $(".aller-toast");
    if(!toast){
      toast = document.createElement("div");
      toast.className = "aller-toast";
      Object.assign(toast.style,{
        position:"fixed", left:"50%", bottom:"24px", transform:"translateX(-50%)",
        background:"#06283e", color:"#fff", padding:"11px 15px", borderRadius:"10px",
        fontSize:"10px", zIndex:"200", boxShadow:"0 15px 40px rgba(0,0,0,.2)", maxWidth:"min(520px,90vw)"
      });
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.style.opacity = "1";
    clearTimeout(window.__allerToast);
    window.__allerToast = setTimeout(() => toast.style.opacity = "0", 3000);
  }

  // Smooth reveal for cards
  const observer = "IntersectionObserver" in window ? new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if(entry.isIntersecting){ entry.target.style.opacity="1"; entry.target.style.transform="none"; observer.unobserve(entry.target); }
    });
  },{threshold:.08}) : null;
  if(observer) $$(".service-card,.product-card,.metric-card,.panel,.admin-card,.workflow-card").forEach(el => {
    el.style.opacity = "0"; el.style.transform = "translateY(10px)"; el.style.transition = "opacity .5s ease, transform .5s ease";
    observer.observe(el);
  });
});