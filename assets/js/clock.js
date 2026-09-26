// Indianapolis time, independent of the visitor's location; DST is automatic.
(() => {
  const clock = document.getElementById('indianapolis-time');
  if (!clock) return;
  const formatter = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/Indiana/Indianapolis',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
    timeZoneName: 'short',
  });
  const update = () => {
    const now = new Date();
    clock.textContent = formatter.format(now);
    clock.dateTime = now.toISOString();
  };
  update();
  document.getElementById('local-clock').hidden = false;
  // No ticking seconds: refresh quietly at each minute boundary.
  const tick = () => {
    update();
    setTimeout(tick, 60000 - Date.now() % 60000);
  };
  setTimeout(tick, 60000 - Date.now() % 60000);
})();
