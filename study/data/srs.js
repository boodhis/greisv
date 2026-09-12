/* Ядро интервального повторения (SRS) — как на панели Heltec.
   Интервалы, мин: 2, 5, 10, 25, 60, 180, 720, 1440, 2880, 5760, 11520 (8 дней). */
window.SRS = (function () {
  var KEY = 'srs_state_v1';
  var INTERVALS = [2, 5, 10, 25, 60, 180, 720, 1440, 2880, 5760, 11520];

  function nowSec() { return Math.floor(Date.now() / 1000); }

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }
  function save(state) {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}
  }

  function meta(state, w) { return state[w] || (state[w] = { reps: 0, due: 0 }); }

  /* Выбор карточки: overdue → свежие → случайные (не ту же подряд). */
  function pick(cards, state, last) {
    if (!cards.length) return null;
    var now = nowSec();
    var overdue = cards.filter(function (c) { return (state[c[0]] || {}).due <= now; });
    var pool = (overdue.length ? overdue : cards.filter(function (c) { return !state[c[0]]; }));
    if (!pool.length) pool = cards;
    var cand = pool.filter(function (c) { return c[0] !== last; });
    if (!cand.length) cand = pool;
    return cand[Math.floor(Math.random() * cand.length)];
  }

  function show(card) {
    var st = load();
    var m = meta(st, card[0]);
    m.shown = nowSec();
    save(st);
    return { word: card[0], trans: card[1], answer: card[2] };
  }

  /* ok=true — «помню», ok=false — «забыл» (возврат к интервалу 2 мин). */
  function grade(card, ok) {
    var st = load();
    var m = meta(st, card[0]);
    if (ok) {
      m.reps = (m.reps || 0) + 1;
      var i = INTERVALS[Math.min(m.reps - 1, INTERVALS.length - 1)];
      m.due = nowSec() + i * 60;
    } else {
      m.reps = 0;
      m.due = nowSec() + 2 * 60;
    }
    save(st);
    return m;
  }

  function stats(cards) {
    var st = load(), now = nowSec();
    var fresh = 0, due = 0, learned = 0;
    cards.forEach(function (c) {
      var m = st[c[0]];
      if (!m) { fresh++; return; }
      learned++;
      if (m.due <= now) due++;
    });
    return { total: cards.length, fresh: fresh, due: due, learned: learned };
  }

  function reset() { try { localStorage.removeItem(KEY); } catch (e) {} }

  return {
    KEY: KEY,
    INTERVALS: INTERVALS,
    pick: pick,
    show: show,
    grade: grade,
    stats: stats,
    reset: reset
  };
})();