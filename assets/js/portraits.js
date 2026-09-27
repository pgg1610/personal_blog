// Crossfades the home portraits every few seconds. The first image stays put
// when motion is reduced or JavaScript is unavailable.
(() => {
  const container = document.getElementById('home-portraits');
  if (!container) return;
  const images = container.querySelectorAll('img');
  if (images.length < 2) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  let current = 0;
  window.setInterval(() => {
    images[current].classList.remove('is-active');
    current = (current + 1) % images.length;
    images[current].classList.add('is-active');
  }, 5000);
})();
