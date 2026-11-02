const ALLER_API = window.ALLER_API_BASE || "http://localhost:5000/api/v1";

async function apiRequest(path, options = {}) {
  const config = { ...options, headers: { "Content-Type": "application/json", ...(options.headers || {}) } };
  const token = sessionStorage.getItem("allerAccessToken");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  const response = await fetch(`${ALLER_API}${path}`, config);
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.message || "Request failed");
  return body;
}
window.allerApi = {
  health: () => apiRequest("/health"),
  login: (payload) => apiRequest("/auth/login", { method: "POST", body: JSON.stringify(payload) }),
  me: () => apiRequest("/auth/me"),
  logout: () => apiRequest("/auth/logout", { method: "POST" }),
  customerDashboard: () => apiRequest("/customer/dashboard"),
  accounts: () => apiRequest("/accounts"),
  transactions: () => apiRequest("/transactions"),
  notifications: () => apiRequest("/notifications"),
  submitAccountOpening: (payload) => apiRequest("/account-opening/applications", { method: "POST", body: JSON.stringify(payload) })
};
