/* ============================================================================
   preview.js — 设计系统文档站「固定外壳」行为层
   ----------------------------------------------------------------------------
   工具层，跨项目复用、不要手改。职责：
   1. 主题切换（浅/深）。
   2. 从 #ph-manifest 的 JSON 数据，自动渲染颜色/字体/间距/圆角/阴影章节，
      色板自带对比度徽章 + 点击复制 hex —— 专业呈现由这里兜底，不靠手写。
   3. 代码块展开/收起 + 一键复制。
   4. 侧栏滚动高亮（scrollspy）+ 移动端抽屉。
   token 的「值」始终从 tokens.css 的 CSS 变量实时读取，文档与代码永不漂移。
   ============================================================================ */
(function () {
  "use strict";

  var root = document.documentElement;

  /* -------------------------------------------------- theme */
  var THEME_KEY = "ph-theme";
  function applyTheme(t) {
    root.setAttribute("data-ph-theme", t);
    var btn = document.querySelector("[data-ph-theme-toggle]");
    if (btn) btn.textContent = t === "dark" ? "☀" : "☾";
    renderTokens(); // contrast badges depend on surface color
  }
  try {
    applyTheme(localStorage.getItem(THEME_KEY) || "light");
  } catch (e) {
    applyTheme("light");
  }
  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-ph-theme-toggle]");
    if (!t) return;
    var next = root.getAttribute("data-ph-theme") === "dark" ? "light" : "dark";
    try { localStorage.setItem(THEME_KEY, next); } catch (e2) {}
    applyTheme(next);
  });

  /* -------------------------------------------------- color helpers */
  function readVar(name) {
    return getComputedStyle(root).getPropertyValue(name).trim();
  }
  function toRGB(value) {
    // resolve any css color (named/hex/rgb) by letting the browser compute it
    var probe = document.createElement("span");
    probe.style.color = value;
    probe.style.display = "none";
    document.body.appendChild(probe);
    var c = getComputedStyle(probe).color;
    document.body.removeChild(probe);
    var m = c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    var p = m[1].split(",").map(function (x) { return parseFloat(x); });
    return { r: p[0], g: p[1], b: p[2], a: p[3] === undefined ? 1 : p[3] };
  }
  function toHex(rgb) {
    if (!rgb) return "";
    function h(n) { return ("0" + Math.round(n).toString(16)).slice(-2); }
    return ("#" + h(rgb.r) + h(rgb.g) + h(rgb.b)).toUpperCase();
  }
  function lum(rgb) {
    var a = [rgb.r, rgb.g, rgb.b].map(function (v) {
      v /= 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2];
  }
  function contrast(a, b) {
    if (!a || !b) return 0;
    var l1 = lum(a), l2 = lum(b);
    var hi = Math.max(l1, l2), lo = Math.min(l1, l2);
    return (hi + 0.05) / (lo + 0.05);
  }
  function badge(ratio) {
    if (ratio >= 7) return { cls: "aaa", text: "AAA " + ratio.toFixed(1) };
    if (ratio >= 4.5) return { cls: "aa", text: "AA " + ratio.toFixed(1) };
    return { cls: "fail", text: "✕ " + ratio.toFixed(1) };
  }

  /* -------------------------------------------------- toast / copy */
  function flash(msg) {
    var el = document.createElement("div");
    el.textContent = msg;
    el.style.cssText =
      "position:fixed;left:50%;bottom:32px;transform:translateX(-50%);" +
      "background:#1d1f24;color:#fff;padding:8px 16px;border-radius:8px;" +
      "font-size:13px;z-index:999;box-shadow:0 8px 24px rgba(0,0,0,.25)";
    document.body.appendChild(el);
    setTimeout(function () { el.remove(); }, 1200);
  }
  function copy(text) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(function () { flash("已复制 " + text); });
    } else {
      flash("已复制 " + text);
    }
  }

  /* -------------------------------------------------- token rendering */
  function getManifest() {
    var node = document.getElementById("ph-manifest");
    if (!node) return {};
    try { return JSON.parse(node.textContent); } catch (e) { return {}; }
  }

  function renderColors(list) {
    var host = document.getElementById("ph-colors");
    if (!host || !list) return;
    var surface = toRGB(readVar("--ph-surface")) || { r: 255, g: 255, b: 255, a: 1 };
    host.className = "ph-swatches";
    host.innerHTML = "";
    list.forEach(function (t) {
      var rgb = toRGB(readVar(t.var));
      var hex = toHex(rgb);
      var b = badge(contrast(rgb, surface));
      var card = document.createElement("div");
      card.className = "ph-swatch";
      card.innerHTML =
        '<div class="ph-swatch-color" style="background:var(' + t.var + ')" data-copy="' + hex + '"></div>' +
        '<div class="ph-swatch-meta">' +
        '<div class="ph-swatch-name">' + (t.name || "") + "</div>" +
        '<div class="ph-swatch-var">' + t.var + "</div>" +
        '<div class="ph-swatch-row"><span class="ph-swatch-hex">' + hex + "</span>" +
        '<span class="ph-badge ' + b.cls + '" title="对比当前 surface">' + b.text + "</span></div>" +
        (t.usage ? '<div class="ph-swatch-usage">' + t.usage + "</div>" : "") +
        "</div>";
      host.appendChild(card);
    });
  }

  function renderType(list) {
    var host = document.getElementById("ph-type");
    if (!host || !list) return;
    host.innerHTML = "";
    list.forEach(function (t) {
      var size = readVar(t.var);
      var row = document.createElement("div");
      row.className = "ph-type-row";
      var weight = t.weightVar ? readVar(t.weightVar) : "";
      row.innerHTML =
        '<div class="ph-type-meta">' + (t.name || "") + "<br>" + size +
        (weight ? " / " + weight : "") + "</div>" +
        '<div class="ph-type-sample" style="font-size:' + size +
        (weight ? ";font-weight:" + weight : "") +
        (t.mono ? ";font-family:var(--font-family-mono,monospace)" : "") + '">' +
        (t.sample || "The quick brown fox 中文样张 0123") + "</div>";
      host.appendChild(row);
    });
  }

  function renderScale(id, list, mode) {
    var host = document.getElementById(id);
    if (!host || !list) return;
    host.className = "ph-scale-list";
    host.innerHTML = "";
    var max = 0;
    var vals = list.map(function (t) {
      var v = parseFloat(readVar(t.var)) || 0;
      if (v > max) max = v;
      return v;
    });
    list.forEach(function (t, i) {
      var v = vals[i];
      var row = document.createElement("div");
      row.className = "ph-scale-row";
      var barStyle =
        mode === "radius"
          ? "width:48px;height:32px;border-radius:" + readVar(t.var) + ";background:var(--ph-accent)"
          : "width:" + Math.max(6, (v / max) * 100) + "%";
      row.innerHTML =
        '<span class="ph-scale-name">' + (t.name || t.var) + "</span>" +
        '<span class="ph-scale-val">' + readVar(t.var) + "</span>" +
        '<span class="ph-scale-bar" style="' + barStyle + '"></span>';
      host.appendChild(row);
    });
  }

  function renderShadow(list) {
    var host = document.getElementById("ph-shadow");
    if (!host || !list) return;
    host.className = "ph-tiles";
    host.innerHTML = "";
    list.forEach(function (t) {
      var tile = document.createElement("div");
      tile.className = "ph-tile";
      tile.innerHTML =
        '<div class="ph-tile-shadow" style="box-shadow:var(' + t.var + ')"></div>' +
        '<div class="ph-tile-name">' + (t.name || t.var) + "</div>" +
        '<div class="ph-tile-val">' + t.var + "</div>";
      host.appendChild(tile);
    });
  }

  function renderTokens() {
    var m = getManifest();
    renderColors(m.colors);
    renderType(m.type);
    renderScale("ph-spacing", m.spacing, "spacing");
    renderScale("ph-radius", m.radius, "radius");
    renderShadow(m.shadow);
  }
  renderTokens();

  /* -------------------------------------------------- copy + code blocks */
  document.addEventListener("click", function (e) {
    var sw = e.target.closest("[data-copy]");
    if (sw) { copy(sw.getAttribute("data-copy")); return; }

    var cp = e.target.closest("[data-ph-copy-code]");
    if (cp) {
      var demo = cp.closest(".ph-demo");
      var code = demo && demo.querySelector("code");
      if (code) copy(code.textContent);
      return;
    }
    var tg = e.target.closest("[data-ph-toggle-code]");
    if (tg) {
      var d = tg.closest(".ph-demo");
      var block = d && d.querySelector(".ph-code");
      if (block) {
        block.classList.toggle("is-open");
        tg.textContent = block.classList.contains("is-open") ? "隐藏代码" : "查看代码";
      }
    }
  });

  /* -------------------------------------------------- mobile sidebar */
  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-ph-menu]")) {
      document.querySelector(".ph-sidebar").classList.toggle("is-open");
    } else if (!e.target.closest(".ph-sidebar")) {
      var sb = document.querySelector(".ph-sidebar.is-open");
      if (sb && window.innerWidth <= 880) sb.classList.remove("is-open");
    }
  });

  /* -------------------------------------------------- scrollspy */
  var links = Array.prototype.slice.call(document.querySelectorAll(".ph-nav-link"));
  var sections = links
    .map(function (l) { return document.querySelector(l.getAttribute("href")); })
    .filter(Boolean);
  if ("IntersectionObserver" in window && sections.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            links.forEach(function (l) {
              l.classList.toggle("is-active", l.getAttribute("href") === "#" + en.target.id);
            });
          }
        });
      },
      { rootMargin: "-50% 0px -45% 0px" }
    );
    sections.forEach(function (s) { io.observe(s); });
  }
})();
