function allerEscape(value="") {
  return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function renderRows(selector, rows, columns) {
  const body = document.querySelector(selector);
  if (!body) return;
  body.innerHTML = rows.map(row => `<tr>${columns.map(c => `<td>${allerEscape(row[c] ?? "")}</td>`).join("")}</tr>`).join("");
}
