/* Trang khám phá phân rã chức năng: cây có lọc, ma trận CRUD, truy vết yêu cầu, actor × module, kết quả lint.
   Dữ liệu nằm ở window.FD_DATA (do scripts/build_explorer_page.py nhúng). Không cần mạng. */
(function () {
  const D = window.FD_DATA;
  const $ = (s, r) => (r || document).querySelector(s);
  const el = (t, a, ...kids) => {
    const e = document.createElement(t);
    Object.entries(a || {}).forEach(([k, v]) => (k === 'class' ? (e.className = v) : k === 'text' ? (e.textContent = v) : e.setAttribute(k, v)));
    kids.flat().forEach((k) => k != null && e.append(k.nodeType ? k : document.createTextNode(k)));
    return e;
  };
  const actorName = (id) => (D.actors.find((a) => a.id === id) || {}).name || id;
  const objName = (id) => (D.objects.find((o) => o.id === id) || {}).name || id;
  const state = { q: '', actor: '', prio: '' };

  function matches(n) {
    if (!n.leaf) return true;
    if (state.actor && !(n.actors || []).includes(state.actor)) return false;
    if (state.prio && n.priority !== state.prio) return false;
    if (state.q) {
      const hay = (n.id + ' ' + n.name + ' ' + (n.note || '') + ' ' + (n.reqs || []).join(' ')).toLowerCase();
      if (!hay.includes(state.q.toLowerCase())) return false;
    }
    return true;
  }
  function anyMatch(n) { return n.leaf ? matches(n) : n.children.some(anyMatch); }

  function renderNode(n) {
    if (!anyMatch(n)) return null;
    const head = el('span', { class: 'row' },
      el('span', { class: 'nid', text: n.id }), ' ', el('span', { class: 'nname', text: n.name }));
    if (n.leaf) {
      (n.actors || []).forEach((a) => head.append(' ', el('span', { class: 'chip', text: actorName(a) })));
      if (n.priority) head.append(' ', el('span', { class: 'chip p-' + n.priority, text: n.priority }));
      Object.entries(n.ops || {}).forEach(([o, l]) => head.append(' ', el('span', { class: 'chip ops', text: objName(o) + ': ' + l })));
      (n.reqs || []).forEach((r) => head.append(' ', el('span', { class: 'chip req', text: r })));
      if (n.note) head.append(' ', el('span', { class: 'note', text: '— ' + n.note }));
      return el('li', { class: 'leaf' }, head);
    }
    const d = el('details', { open: state.q || state.actor || state.prio ? 'open' : null }, el('summary', {}, head),
      el('ul', {}, n.children.map(renderNode)));
    if (n.depth === 1) d.setAttribute('open', 'open');
    return el('li', { class: 'depth' + n.depth }, d);
  }

  function renderTree() {
    const box = $('#tree'); box.replaceChildren(el('ul', { class: 'tree' }, D.modules.map(renderNode)));
  }

  function table(head, rows, cls) {
    return el('table', { class: cls || '' }, el('thead', {}, el('tr', {}, head.map((h) => el('th', { text: h })))),
      el('tbody', {}, rows.map((r) => el('tr', {}, r.map((c) => (c && c.nodeType ? c : el('td', { text: c })))))));
  }
  const td = (text, cls) => el('td', { class: cls || '', text });

  function renderCrud() {
    const rows = D.objects.map((o) => {
      const cells = [td(o.name)];
      ['C', 'R', 'U', 'D'].forEach((ch) => {
        const ids = D.crud[o.id] && D.crud[o.id][ch];
        const why = (D.waived[o.id] || {})[ch];
        cells.push(ids && ids.length ? td(ids.join(', ')) : why ? td('— (miễn: ' + why + ')', 'muted') : td('❌ thiếu', 'bad'));
      });
      return cells;
    });
    $('#crud').replaceChildren(D.objects.length ? table(['Đối tượng', 'Create', 'Read', 'Update', 'Delete / Hủy'], rows) : el('p', { text: 'Spec chưa khai báo objects.' }));
  }
  function renderReqs() {
    const rows = D.requirements.map((r) => {
      const ids = D.cover[r.id] || [];
      return [td(r.id), td(r.text || ''), ids.length ? td(ids.join(', ')) : td('❌ chưa phủ', 'bad')];
    });
    const orphan = D.functions.filter((f) => !(f.reqs && f.reqs.length) && !f.derived).map((f) => f.id);
    $('#reqs').replaceChildren(D.requirements.length ? table(['Yêu cầu', 'Nội dung', 'Chức năng phủ'], rows) : el('p', { text: 'Spec chưa khai báo requirements.' }),
      orphan.length && D.requirements.length ? el('p', { class: 'warn', text: 'Chức năng chưa truy về yêu cầu: ' + orphan.join(', ') }) : null);
  }
  function renderMatrix() {
    const rows = D.actors.map((a) => [td(a.name)].concat(D.modules.map((m) => td(String((D.matrix[a.id] || {})[m.id] || '')))));
    $('#matrix').replaceChildren(D.actors.length ? table(['Actor'].concat(D.modules.map((m) => m.id + '. ' + m.name)), rows) : el('p', { text: 'Spec chưa khai báo actors.' }));
  }
  function renderLint() {
    const L = D.lint;
    const counts = { 'LỖI': 0, 'CẢNH BÁO': 0, 'MIỄN': 0 };
    L.forEach((x) => counts[x.level]++);
    $('#lint').replaceChildren(
      el('p', { class: counts['LỖI'] ? 'bad' : 'ok', text: counts['LỖI'] + ' lỗi · ' + counts['CẢNH BÁO'] + ' cảnh báo · ' + counts['MIỄN'] + ' miễn trừ' }),
      L.length ? table(['Mức', 'Mã', 'Vị trí', 'Mô tả'], L.map((x) => [td(x.level, x.level === 'LỖI' ? 'bad' : x.level === 'MIỄN' ? 'muted' : 'warn'), td(x.code), td(x.where), td(x.message)])) : el('p', { class: 'ok', text: 'Không có phát hiện.' }));
  }

  function init() {
    $('#title').textContent = D.name;
    $('#stats').textContent = D.modules.length + ' module · ' + D.functions.length + ' chức năng · sâu ' + D.depth + ' cấp';
    const sa = $('#f-actor'); sa.append(el('option', { value: '', text: 'Mọi actor' }));
    D.actors.forEach((a) => sa.append(el('option', { value: a.id, text: a.name })));
    $('#f-q').addEventListener('input', (e) => { state.q = e.target.value; renderTree(); });
    sa.addEventListener('change', (e) => { state.actor = e.target.value; renderTree(); });
    $('#f-prio').addEventListener('change', (e) => { state.prio = e.target.value; renderTree(); });
    $('#expand').addEventListener('click', () => document.querySelectorAll('#tree details').forEach((d) => (d.open = true)));
    $('#collapse').addEventListener('click', () => document.querySelectorAll('#tree details').forEach((d) => (d.open = false)));
    document.querySelectorAll('.tabs button').forEach((b) => b.addEventListener('click', () => {
      document.querySelectorAll('.tabs button').forEach((x) => x.setAttribute('aria-selected', String(x === b)));
      document.querySelectorAll('.panel').forEach((p) => (p.hidden = p.id !== b.dataset.panel));
    }));
    renderTree(); renderCrud(); renderReqs(); renderMatrix(); renderLint();
    const bad = D.lint.filter((x) => x.level === 'LỖI').length;
    $('#tab-lint').textContent = 'Kiểm tra (' + (bad ? bad + ' lỗi' : D.lint.filter((x) => x.level === 'CẢNH BÁO').length + ' cảnh báo') + ')';
  }
  init();
})();
