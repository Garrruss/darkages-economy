/* Единый список страниц. Новая страница вики добавляется одной строкой. */
var SITE_PAGES = [
  {href: "index.html",    title: "Главная"},
  {href: "glossary.html", title: "Словарь терминов"},
  {href: "money.html",    title: "Деньги и потоки"},
  {href: "treasury.html", title: "Казна"},
  {href: "markets.html",  title: "Склад, земли, рынки"},
  {href: "roles.html",    title: "Заработок по ролям"},
  {href: "prices.html",   title: "Цены"},
  {href: "model.html",    title: "Модель казны"},
  {href: "analysis.html", title: "Разбор системы"},
  {href: "issues.html",   title: "Неясное и обсуждение"}
];
(function () {
  var root = document.getElementById("nav-root");
  if (!root) return;
  var cur = (location.pathname.split("/").pop() || "index.html");
  var links = SITE_PAGES.map(function (p) {
    return '<a href="' + p.href + '"' + (p.href === cur ? ' aria-current="page"' : '') + '>' + p.title + '</a>';
  }).join("");
  root.innerHTML =
    '<div class="topbar"><a class="brand" href="index.html">Экономика Dark Ages 13</a>' +
    '<button class="burger" type="button" aria-expanded="false" aria-controls="sitenav" aria-label="Меню">&#9776;</button></div>' +
    '<nav id="sitenav" aria-label="Разделы"><span class="navtitle">Экономика Dark Ages 13</span>' + links + '</nav>';
  var btn = root.querySelector(".burger"), nav = root.querySelector("#sitenav");
  btn.addEventListener("click", function () {
    var o = nav.classList.toggle("open");
    btn.setAttribute("aria-expanded", o ? "true" : "false");
  });
})();
