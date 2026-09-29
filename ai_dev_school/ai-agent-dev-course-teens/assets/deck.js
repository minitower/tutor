(function () {
  const slides = Array.from(document.querySelectorAll(".slide"));
  const total = slides.length;
  let idx = 0;

  const counterEl = document.getElementById("deck-counter");
  const progressEl = document.getElementById("deck-progress");

  const clamp = (i) => Math.max(0, Math.min(total - 1, i));

  function render() {
    slides.forEach((s, i) => {
      s.classList.toggle("active", i === idx);
      s.classList.toggle("prev", i < idx);
    });
    if (counterEl) counterEl.textContent = `${idx + 1} / ${total}`;
    if (progressEl) progressEl.style.width = `${(idx / (total - 1 || 1)) * 100}%`;
    history.replaceState(null, "", "#" + (idx + 1));
  }

  const go = (i) => { idx = clamp(i); render(); };
  const next = () => go(idx + 1);
  const prev = () => go(idx - 1);

  document.addEventListener("keydown", (e) => {
    if (["ArrowRight", "ArrowDown", "PageDown", " "].includes(e.key)) { e.preventDefault(); next(); }
    else if (["ArrowLeft", "ArrowUp", "PageUp"].includes(e.key)) { e.preventDefault(); prev(); }
    else if (e.key === "Home") go(0);
    else if (e.key === "End") go(total - 1);
    else if (e.key === "f" || e.key === "F") toggleFullscreen();
  });

  document.querySelectorAll('[data-nav="next"]').forEach((b) => b.addEventListener("click", next));
  document.querySelectorAll('[data-nav="prev"]').forEach((b) => b.addEventListener("click", prev));
  document.querySelectorAll('[data-nav="fullscreen"]').forEach((b) => b.addEventListener("click", toggleFullscreen));

  function toggleFullscreen() {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen?.();
    else document.exitFullscreen?.();
  }

  let touchX = null;
  document.addEventListener("touchstart", (e) => { touchX = e.touches[0].clientX; });
  document.addEventListener("touchend", (e) => {
    if (touchX === null) return;
    const dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) (dx < 0 ? next() : prev());
    touchX = null;
  });

  const initial = parseInt(location.hash.replace("#", ""), 10);
  idx = clamp((initial || 1) - 1);
  render();
})();
