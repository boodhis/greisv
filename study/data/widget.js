/* Виджет «Слово дня» / мини-тренажёр. Использует колоду window.SRS_DAY.
   Если в блоке есть кнопки (.wd-reveal/.wd-forgot/.wd-ok) — работает как
   мини-тренажёр с интервальным повторением (SRS), иначе — простое
   «слово дня»: случайная карточка, клик раскрывает перевод. */
(function () {
  function ready(fn) {
    if (document.readyState !== 'loading') { fn(); } else { document.addEventListener('DOMContentLoaded', fn); }
  }
  ready(function () {
    var el = document.getElementById('wordday');
    if (!el || !window.SRS_DAY || !window.SRS_DAY.length) return;
    var q = el.querySelector('.wd-w'), ph = el.querySelector('.wd-ph'), t2 = el.querySelector('.wd-t2');
    var hint = el.querySelector('.wd-hint');
    var bReveal = el.querySelector('.wd-reveal');
    var bForgot = el.querySelector('.wd-forgot');
    var bOk = el.querySelector('.wd-ok');
    var isTrainer = !!(bReveal && bForgot && bOk);

    function show(card) {
      q.textContent = card[0];
      ph.textContent = card[1] ? '[' + card[1] + ']' : '';
      t2.textContent = card[2];
      el.classList.remove('revealed');
      if (isTrainer) {
        bReveal.style.display = '';
        bForgot.style.display = 'none';
        bOk.style.display = 'none';
      }
    }

    function next(last) {
      var pool = window.SRS_DAY.filter(function (c) { return c[0] !== last; });
      if (!pool.length) pool = window.SRS_DAY;
      var c = pool[Math.floor(Math.random() * pool.length)];
      show(c);
      return c;
    }

    var first = window.SRS_DAY[Math.floor(Math.random() * window.SRS_DAY.length)];

    if (!isTrainer) {
      show(first);
      el.addEventListener('click', function () { el.classList.add('revealed'); });
      return;
    }

    /* Мини-тренажёр: интервалы те же, что в study/srs.js (localStorage). */
    var current = first;
    show(current);

    bReveal.addEventListener('click', function () {
      el.classList.add('revealed');
      bReveal.style.display = 'none';
      bForgot.style.display = '';
      bOk.style.display = '';
      if (window.SRS) window.SRS.show(current);
    });
    bForgot.addEventListener('click', function () {
      if (window.SRS) window.SRS.grade(current, false);
      current = next(current[0]);
    });
    bOk.addEventListener('click', function () {
      if (window.SRS) window.SRS.grade(current, true);
      current = next(current[0]);
    });
    if (hint) hint.textContent = 'жми «Показать перевод», затем «Помню»/«Забыл»';
  });
})();