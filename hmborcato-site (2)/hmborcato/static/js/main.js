// ==========================================================================
// H.M. Borçato — interações do site
// ==========================================================================
(function () {
  "use strict";

  // ---- Menu mobile -------------------------------------------------------
  var toggle = document.getElementById("menu-toggle");
  var menu = document.getElementById("mobile-menu");
  var iconOpen = document.getElementById("icon-open");
  var iconClose = document.getElementById("icon-close");

  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var isOpen = !menu.classList.contains("hidden");
      menu.classList.toggle("hidden");
      toggle.setAttribute("aria-expanded", String(!isOpen));
      iconOpen.classList.toggle("hidden");
      iconClose.classList.toggle("hidden");
    });

    // fecha o menu ao clicar em um link
    menu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        menu.classList.add("hidden");
        toggle.setAttribute("aria-expanded", "false");
        iconOpen.classList.remove("hidden");
        iconClose.classList.add("hidden");
      });
    });
  }

  // ---- Reveal on scroll ----------------------------------------------------
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var revealEls = document.querySelectorAll(".reveal");

  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  } else {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(function (el) { observer.observe(el); });
  }

  // ---- Animação do trajeto no mapa de cobertura ----------------------------
  var routePaths = document.querySelectorAll(".route-path");
  if (routePaths.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      routePaths.forEach(function (p) { p.classList.add("is-visible"); });
    } else {
      var routeObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            routeObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.3 });
      routePaths.forEach(function (p) { routeObserver.observe(p); });
    }
  }

  // ---- Máscara simples de telefone (formulário de contato) -----------------
  var telInput = document.getElementById("telefone");
  if (telInput) {
    telInput.addEventListener("input", function (e) {
      var v = e.target.value.replace(/\D/g, "").slice(0, 11);
      if (v.length > 6) {
        v = v.replace(/(\d{2})(\d{4,5})(\d{0,4})/, "($1) $2-$3");
      } else if (v.length > 2) {
        v = v.replace(/(\d{2})(\d{0,5})/, "($1) $2");
      } else if (v.length > 0) {
        v = v.replace(/(\d{0,2})/, "($1");
      }
      e.target.value = v.trim();
    });
  }

  // ---- Contador de caracteres da mensagem -----------------------------------
  var msgInput = document.getElementById("mensagem");
  var msgCount = document.getElementById("mensagem-contador");
  if (msgInput && msgCount) {
    var max = parseInt(msgInput.getAttribute("maxlength") || "600", 10);
    var updateCount = function () {
      msgCount.textContent = msgInput.value.length + " / " + max;
    };
    msgInput.addEventListener("input", updateCount);
    updateCount();
  }

  // ---- Destaque de card ao passar o mouse no mapa de cobertura --------------
  document.querySelectorAll("[data-regiao]").forEach(function (waypoint) {
    waypoint.addEventListener("mouseenter", function () {
      var card = document.querySelector('[data-regiao-card="' + waypoint.dataset.regiao + '"]');
      if (card) card.classList.add("ring-2", "ring-action");
    });
    waypoint.addEventListener("mouseleave", function () {
      var card = document.querySelector('[data-regiao-card="' + waypoint.dataset.regiao + '"]');
      if (card) card.classList.remove("ring-2", "ring-action");
    });
  });
})();
