/* Token player: chạy lần lượt các bước animation trên một SVG sơ đồ BPMN.
   Dùng bởi scripts/build_token_page.py, cũng có thể nhúng vào trang/slide khác.

   tokenPlayer({ svg, caption, buttons, scenarios })
     svg       : phần tử <svg> của sơ đồ
     caption   : phần tử hiển thị câu thuyết minh
     buttons   : NodeList các nút có data-sc="<id kịch bản>"
     scenarios : { id: [step, ...] }
   Các loại step:
     {t:"spawn", tok, at:[x,y], color}   tạo token
     {t:"move",  tok, pts:[[x,y],...]}   token chạy theo đường gấp khúc
     {t:"msg",   pts}                    phong bì message bay theo message flow
     {t:"busy",  box:[x,y,w,h], ms}      tô viền task đang làm
     {t:"say",   text}                   đổi câu thuyết minh (cho phép <b>)
     {t:"ring",  at, color}              vòng sóng ở event/gateway
     {t:"kill",  tok}                    token bị huỷ (đổi màu rồi mờ dần)
     {t:"fade",  tok}                    token biến mất nhẹ nhàng
     {t:"stuck", tok, at}                token kẹt: vòng sóng lặp lại
     {t:"wait",  ms}
*/
(function (global) {
  const NS = 'http://www.w3.org/2000/svg';
  const COLORS = { green: '#1F8A4C', yellow: '#F2C94C', pink: '#E8508F', ink: '#1B1B1F' };
  const CSS = `
    .tp-dot{ transition:opacity .5s; filter:drop-shadow(0 2px 0 rgba(0,0,0,.3)); }
    .tp-dot.gone{ opacity:0; }
    .tp-busy{ fill:none; stroke:${COLORS.pink}; stroke-width:5; animation:tpBusy .9s ease-in-out infinite alternate; }
    @keyframes tpBusy{ from{ stroke-opacity:.25; } to{ stroke-opacity:.95; } }
    .tp-ring{ fill:none; stroke-width:4; transform-box:fill-box; transform-origin:center; animation:tpRing 1s ease-out forwards; }
    @keyframes tpRing{ from{ opacity:1; transform:scale(.7); } to{ opacity:0; transform:scale(2.2); } }`;

  function tokenPlayer(opts) {
    const { svg, caption, buttons, scenarios } = opts;
    const reduce = global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const SPEED = reduce ? 100 : (opts.speed || 0.3);   // đơn vị toạ độ SVG / ms
    if (!svg.querySelector('style.tp-style')) {
      const st = document.createElementNS(NS, 'style');
      st.setAttribute('class', 'tp-style'); st.textContent = CSS; svg.appendChild(st);
    }
    const layer = document.createElementNS(NS, 'g');
    svg.appendChild(layer);
    let run = 0;

    function el(tag, attrs, cls, parent) {
      const e = document.createElementNS(NS, tag);
      for (const k in attrs) e.setAttribute(k, attrs[k]);
      if (cls) e.setAttribute('class', cls);
      (parent || layer).appendChild(e);
      return e;
    }
    const at = (g, x, y) => g.setAttribute('transform', `translate(${x} ${y})`);
    const color = c => COLORS[c] || c || COLORS.green;

    function player(id) {
      const toks = {};
      const alive = () => { if (id !== run) throw 'stop'; };
      const wait = ms => new Promise((res, rej) => setTimeout(() => id === run ? res() : rej('stop'), reduce ? 0 : ms));
      function move(g, pts) {
        return new Promise((res, rej) => {
          const seg = []; let total = 0;
          for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); seg.push(d); total += d; }
          if (!seg.length) { at(g, pts[0][0], pts[0][1]); return res(); }
          const dur = Math.max(1, total / SPEED), t0 = performance.now();
          (function step(now) {
            if (id !== run) return rej('stop');
            const t = Math.min(1, (now - t0) / dur);
            let d = t * total, i = 0;
            while (i < seg.length - 1 && d > seg[i]) { d -= seg[i]; i++; }
            const k = seg[i] ? d / seg[i] : 1;
            at(g, pts[i][0] + (pts[i + 1][0] - pts[i][0]) * k, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * k);
            t < 1 ? requestAnimationFrame(step) : res();
          })(performance.now());
        });
      }
      function ring(p, c) { const r = el('circle', { cx: p[0], cy: p[1], r: 20, stroke: color(c) }, 'tp-ring'); setTimeout(() => r.remove(), 1100); }
      const H = {
        async spawn(s) {
          const g = el('g', {}, 'tp-dot');
          el('circle', { r: 10, fill: color(s.color), stroke: COLORS.ink, 'stroke-width': 2.5 }, null, g);
          at(g, s.at[0], s.at[1]); toks[s.tok] = g;
        },
        async move(s) { if (toks[s.tok]) await move(toks[s.tok], s.pts); },
        async msg(s) {
          const g = el('g', {}, 'tp-dot');
          el('rect', { x: -12, y: -8, width: 24, height: 16, rx: 2, fill: COLORS.yellow, stroke: COLORS.ink, 'stroke-width': 2 }, null, g);
          el('polyline', { points: '-12,-8 0,1 12,-8', fill: 'none', stroke: COLORS.ink, 'stroke-width': 2 }, null, g);
          at(g, s.pts[0][0], s.pts[0][1]);
          await move(g, s.pts); g.classList.add('gone'); setTimeout(() => g.remove(), 600);
        },
        async busy(s) {
          const [x, y, w, h] = s.box;
          const r = el('rect', { x: x - 5, y: y - 5, width: w + 10, height: h + 10, rx: 13 }, 'tp-busy');
          await wait(s.ms || 700); r.remove();
        },
        async say(s) { alive(); caption.innerHTML = s.text; },
        async ring(s) { ring(s.at, s.color); },
        async kill(s) {
          const g = toks[s.tok]; if (!g) return;
          g.firstChild.setAttribute('fill', COLORS.pink); await wait(450); g.classList.add('gone'); await wait(400);
        },
        async fade(s) { const g = toks[s.tok]; if (g) g.classList.add('gone'); },
        async stuck(s) { for (let i = 0; i < 5; i++) { ring(s.at, 'pink'); await wait(900); } },
        async wait(s) { await wait(s.ms); }
      };
      return async steps => { for (const s of steps) { alive(); await H[s.t](s); if (s.t === 'move' || s.t === 'msg') await wait(120); } };
    }

    function play(key) {
      const id = ++run;
      layer.innerHTML = '';
      buttons.forEach(b => b.classList.toggle('on', b.getAttribute('data-sc') === key));
      player(id)(scenarios[key]).catch(() => {});
    }
    buttons.forEach(b => b.addEventListener('click', () => play(b.getAttribute('data-sc'))));
    return { play };
  }
  global.tokenPlayer = tokenPlayer;
})(window);
