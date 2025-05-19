document.addEventListener('DOMContentLoaded', () => {
document.querySelectorAll('.post-menu-toggle').forEach(button => {
  button.addEventListener('click', (event) => {
    const menu = button.nextElementSibling;
    const isOpen = !menu.hidden;

    document.querySelectorAll('.post-menu').forEach(m => m.hidden = true);

    menu.hidden = isOpen;
  });
});

document.addEventListener('click', (event) => {
  const isMenu = event.target.closest('.post-menu-wrapper');
  if (!isMenu) {
    document.querySelectorAll('.post-menu').forEach(m => m.hidden = true);
  }
});
});
