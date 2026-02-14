document.addEventListener("DOMContentLoaded", () => {
  const monitorsBody = document.getElementById("monitorsBody");
  const healthText = document.getElementById("healthText");
  const healthPill = document.getElementById("healthPill");
  const refreshBtn = document.getElementById("refreshBtn");
  const createForm = document.getElementById("createForm");

  async function fetchHealth() {
    try {
      const res = await fetch("/health");
      if (!res.ok) throw new Error("Health check failed");
      healthText.textContent = "Operational";
      healthPill.querySelector(".dot").style.background = "#22c55e";
    } catch {
      healthText.textContent = "Degraded";
      healthPill.querySelector(".dot").style.background = "#ef4444";
    }
  }

  async function fetchMonitors() {
    try {
      const res = await fetch("/monitors");
      if (!res.ok) throw new Error("Failed to load monitors");
      const data = await res.json();
      renderMonitors(data);
    } catch {
      monitorsBody.innerHTML =
        `<tr><td colspan="5" class="muted">Unable to load monitors</td></tr>`;
    }
  }

  function renderMonitors(items) {
    if (!items || items.length === 0) {
      monitorsBody.innerHTML =
        `<tr><td colspan="5" class="muted">No monitors yet</td></tr>`;
      return;
    }
    monitorsBody.innerHTML = items
      .map(
        (m) => `
      <tr>
        <td>${m.name}</td>
        <td>${m.url}</td>
        <td>${m.interval_seconds}</td>
        <td><span class="muted">Pending</span></td>
        <td>
          <button class="btn" data-edit="${m.id}">Edit</button>
          <button class="btn" data-delete="${m.id}">Delete</button>
        </td>
      </tr>
    `
      )
      .join("");
  }

  createForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(createForm);
    const payload = Object.fromEntries(formData.entries());
    payload.interval_seconds = Number(payload.interval_seconds);
    const res = await fetch("/monitors", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (res.ok) {
      createForm.reset();
      await fetchMonitors();
    }
  });

  refreshBtn.addEventListener("click", () => {
    fetchHealth();
    fetchMonitors();
  });

  monitorsBody.addEventListener("click", async (e) => {
    const editId = e.target.getAttribute("data-edit");
    const deleteId = e.target.getAttribute("data-delete");

    if (editId) {
      const name = prompt("Name:");
      const url = prompt("URL:");
      const interval = Number(prompt("Interval (seconds):", "60"));
      if (!name || !url || !interval) return;
      await fetch(`/monitors/${editId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, url, interval_seconds: interval }),
      });
      fetchMonitors();
    }

    if (deleteId) {
      if (!confirm("Delete this monitor?")) return;
      await fetch(`/monitors/${deleteId}`, { method: "DELETE" });
      fetchMonitors();
    }
  });

  fetchHealth();
  fetchMonitors();
  setInterval(() => {
    fetchHealth();
    fetchMonitors();
  }, 15000);
});