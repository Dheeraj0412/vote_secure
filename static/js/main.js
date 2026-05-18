/* ============================================================
   VoteSecure — main.js
   Small UI enhancements: password toggle, confirm delete,
   animated result bars, auto-dismiss alerts.
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {

  /* ── 1. Password visibility toggle ── */
  document.querySelectorAll(".toggle-pw").forEach(btn => {
    btn.addEventListener("click", () => {
      const targetId = btn.dataset.target;
      const input    = document.getElementById(targetId);
      if (!input) return;

      const isPassword = input.type === "password";
      input.type = isPassword ? "text" : "password";
      btn.querySelector("i").className = isPassword
        ? "bi bi-eye-slash"
        : "bi bi-eye";
    });
  });

  /* ── 2. Confirm before delete forms ── */
  document.querySelectorAll(".confirm-delete").forEach(form => {
    form.addEventListener("submit", e => {
      if (!confirm("Are you sure you want to delete this candidate? This cannot be undone.")) {
        e.preventDefault();
      }
    });
  });

  /* ── 3. Animate result bars on page load ── */
  const bars = document.querySelectorAll(".result-bar");
  if (bars.length) {
    // Set to 0 first, then animate to real width
    bars.forEach(bar => {
      const target = bar.style.width;
      bar.style.width = "0%";
      // requestAnimationFrame ensures the 0-width paints before transition
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          bar.style.width = target;
        });
      });
    });
  }

  /* ── 4. Auto-dismiss flash alerts after 5 s ── */
  setTimeout(() => {
    document.querySelectorAll("#flash-container .alert").forEach(el => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
      bsAlert.close();
    });
  }, 5000);

  /* ── 5. Highlight active nav link ── */
  const currentPath = window.location.pathname;
  document.querySelectorAll(".vs-nav .nav-link").forEach(link => {
    if (link.getAttribute("href") === currentPath) {
      link.style.color = "var(--amber)";
      link.style.background = "rgba(245,158,11,.08)";
    }
  });

});
