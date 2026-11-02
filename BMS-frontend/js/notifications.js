async function loadAllerNotifications(targetSelector) {
  const target = document.querySelector(targetSelector);
  if (!target || !window.allerApi) return;
  try {
    const result = await allerApi.notifications();
    target.innerHTML = (result.data || []).map(n =>
      `<div class="panel" style="padding:12px;margin-bottom:8px"><b>${n.title}</b><div style="font-size:11px;color:var(--muted)">${n.message}</div></div>`
    ).join("");
  } catch(e) {}
}
