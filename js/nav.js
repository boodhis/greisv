/* Сворачиваемая навигация «щупальца»: навигационные разделы-аккордеон.
   Заголовок группы (.ngt) — клик раскрывает подразделы (.nli) с эффектом.
   Активный раздел (текущая страница) раскрыт автоматически. */
(function () {
  var groups = document.querySelectorAll('.ngroup');
  if (!groups.length) return;

  function current() { return document.querySelector('.ngroup .nli.on'); }

  function closeOthers(keep) {
    for (var i = 0; i < groups.length; i++) {
      var g = groups[i];
      if (g !== keep && g.classList.contains('open')) g.classList.remove('open');
      if (g !== keep) g.setAttribute('aria-expanded', 'false');
    }
  }

  for (var i = 0; i < groups.length; i++) {
    var g = groups[i];
    var title = g.querySelector('.ngt');
    if (!title) continue;
    title.setAttribute('tabindex', '0');
    title.setAttribute('role', 'button');
    title.setAttribute('aria-expanded', 'false');
    title.addEventListener('click', function (ev) {
      var group = ev.currentTarget.parentNode;
      var wasOpen = group.classList.contains('open');
      closeOthers(null);
      if (!wasOpen) {
        group.classList.add('open');
        group.setAttribute('aria-expanded', 'true');
      }
    });
    title.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); ev.currentTarget.click(); }
    });
  }

  var active = current();
  if (active && active.closest) {
    var host = active.closest('.ngroup');
    if (host) { host.classList.add('open'); host.setAttribute('aria-expanded', 'true'); }
  }
})();