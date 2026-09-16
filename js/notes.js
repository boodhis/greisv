/* Простые текстовые заметки на каждой странице: одна кнопка, одно поле.
   Текст сохраняется в localStorage по пути страницы — сам, при вводе. */
(function () {
  if (document.getElementById('nts')) return;
  var box = document.createElement('div');
  box.id = 'nts';
  box.hidden = true;
  box.innerHTML = '<div class="nts-bar"><b>Заметка</b><button type="button" class="nts-x" aria-label="Закрыть">✕</button></div>'
    + '<textarea class="nts-t" placeholder="Твоя заметка к этой странице — сохраняется сама в браузере"></textarea>';

  var btn = document.createElement('button');
  btn.id = 'nts-btn';
  btn.type = 'button';
  btn.title = 'Заметка страницы';
  btn.setAttribute('aria-label', 'Заметка страницы');
  btn.textContent = '📝';

  var ta = box.querySelector('.nts-t');
  var KEY = 'nts:' + (location.pathname + location.search);

  try { ta.value = localStorage.getItem(KEY) || ''; } catch (e) {}

  function show(on) {
    box.hidden = !on;
    btn.classList.toggle('on', on);
    if (on) setTimeout(function () { ta.focus(); }, 40);
  }

  btn.addEventListener('click', function () { show(box.hidden); });
  box.querySelector('.nts-x').addEventListener('click', function () { show(false); });
  ta.addEventListener('input', function () {
    try { localStorage.setItem(KEY, ta.value); } catch (e) {}
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !box.hidden) show(false);
  });

  document.body.appendChild(btn);
  document.body.appendChild(box);
})();