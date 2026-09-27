// Click-to-zoom for images in the writing. Progressive enhancement: without
// JavaScript the images render normally and remain readable in place.
(() => {
  const images = Array.from(document.querySelectorAll('.post-content img, .page-content img'));
  if (images.length === 0) return;

  const overlay = document.createElement('div');
  overlay.className = 'lightbox';
  overlay.hidden = true;
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Enlarged image');

  const figure = document.createElement('figure');
  const full = document.createElement('img');
  full.alt = '';
  const caption = document.createElement('figcaption');
  figure.append(full, caption);

  const close = document.createElement('button');
  close.type = 'button';
  close.className = 'lightbox-close';
  close.setAttribute('aria-label', 'Close image');
  close.textContent = '\u00d7';

  overlay.append(close, figure);
  document.body.append(overlay);

  let lastFocused = null;

  const open = (image) => {
    lastFocused = document.activeElement;
    full.src = image.currentSrc || image.src;
    full.alt = image.alt || '';
    caption.textContent = image.alt || '';
    caption.hidden = !image.alt;
    overlay.hidden = false;
    document.body.style.overflow = 'hidden';
    close.focus();
  };

  const hide = () => {
    overlay.hidden = true;
    full.removeAttribute('src');
    document.body.style.overflow = '';
    if (lastFocused) lastFocused.focus();
  };

  images.forEach((image) => {
    image.classList.add('is-zoomable');
    image.tabIndex = 0;
    image.setAttribute('role', 'button');
    image.setAttribute('aria-label', image.alt ? `Enlarge image: ${image.alt}` : 'Enlarge image');
    image.addEventListener('click', () => open(image));
    image.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        open(image);
      }
    });
  });

  close.addEventListener('click', hide);
  overlay.addEventListener('click', (event) => {
    if (event.target === overlay) hide();
  });
  overlay.addEventListener('keydown', (event) => {
    if (event.key === 'Tab') {
      event.preventDefault();
      close.focus();
    }
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !overlay.hidden) hide();
  });
})();
