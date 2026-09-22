/*
 * Table behaviour for figures.html and record.html.
 *
 * build.py inlines this script into each page, after three JSON blocks:
 *   #table-columns   the columns to show, in order (defined in build.py)
 *   #table-rows      one object per conflict
 *   #table-sources   the numbered source list, as [number, label, url]
 *
 * Each column has a "kind" (num, date, cat, text or refs); renderCell()
 * shows how each kind is drawn.
 */
(function () {
  "use strict";

  var COLUMNS = readJson("table-columns");
  var ROWS = readJson("table-rows");
  var SOURCES = readJson("table-sources");

  var table = document.getElementById("tbl");
  var thead = table.querySelector("thead");
  var tbody = table.querySelector("tbody");

  // The CSS colour variable for each conflict type (see page.css).
  var TYPE_COLOUR = {
    "Defensive": "--tDefensive",
    "Offensive": "--tOffensive",
    "Humanitarian": "--tHumanitarian",
    "Freedom of passage": "--tFreedom",
    "Other": "--tOther"
  };

  // The current sort: a column key, and 1 for lowest first or -1 for highest.
  var sortKey = "idx";
  var sortDirection = 1;

  function readJson(id) {
    return JSON.parse(document.getElementById(id).textContent);
  }

  function columnFor(key) {
    for (var i = 0; i < COLUMNS.length; i++) {
      if (COLUMNS[i].key === key) return COLUMNS[i];
    }
    return null;
  }


  /* ---- Formatting ----------------------------------------------------- */

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  // Millions of dollars, shortened: $150m, $1.50bn, $33.4bn, $2.30tn.
  function formatMoney(millions) {
    if (millions == null) return null;
    if (millions >= 1e6) return "$" + (millions / 1e6).toFixed(2) + "tn";
    if (millions >= 1e3) return "$" + (millions / 1e3).toFixed(millions >= 1e4 ? 1 : 2) + "bn";
    return "$" + Math.round(millions) + "m";
  }

  function formatNumber(n) {
    return n == null ? null : Math.round(n).toLocaleString("en-US");
  }

  // Source numbers as superscript links to the list at the foot of the page.
  function sourceLinks(numbers) {
    var links = numbers.map(function (n) {
      return '<a href="#ref-' + n + '">' + n + "</a>";
    });
    return '<sup class="ref">' + links.join(",") + "</sup>";
  }


  /* ---- Cells ---------------------------------------------------------- */

  // One <td> for a row and column.
  function renderCell(column, row) {
    var value = row[column.key];

    if (column.kind === "num") {
      var text = column.money ? formatMoney(value) : formatNumber(value);
      var numClass = "num" + (column.strong && value != null ? " strong" : "");
      var shown = text == null ? '<span class="nil">&mdash;</span>' : text;
      return '<td class="' + numClass + '">' + shown + "</td>";
    }
    if (column.key === "name") {
      // Pinned to the left edge; the theatre goes on a second line.
      var flag = row.flag ? ' <span class="small">' + escapeHtml(row.flag) + "</span>" : "";
      return '<td class="c-name sticky2">' + escapeHtml(row.name) + flag +
        '<span class="sub">' + escapeHtml(row.theatre) + "</span></td>";
    }
    if (column.key === "auth_label") {
      var note = column.detail ?
        '<div class="small auth-note">' + escapeHtml(row.auth_note) + "</div>" : "";
      return '<td><span class="chip lv' + row.auth_level + '">' +
        escapeHtml(row.auth_label) + "</span>" + note + "</td>";
    }
    if (column.key === "type") {
      return '<td><span class="tchip" style="color:var(' + TYPE_COLOUR[row.type] + ')">' +
        escapeHtml(row.type) + "</span></td>";
    }
    if (column.kind === "refs") {
      return '<td class="num">' + sourceLinks(value) + "</td>";
    }
    if (column.kind === "date") {
      // Sorted by the ISO date, shown in words.
      return '<td class="num">' + escapeHtml(row[column.key + "_text"]) + "</td>";
    }
    var proseClass = "prose" + (column.wide ? " wide" : "") + (column.small ? " small" : "");
    return '<td class="' + proseClass + '">' + escapeHtml(value) + "</td>";
  }


  /* ---- Header --------------------------------------------------------- */

  // The first two columns are pinned to the left edge (see page.css).
  function pinClass(column) {
    if (column.key === "idx") return "sticky1";
    if (column.key === "name") return "sticky2";
    return "";
  }

  // A heading whose button sorts the column.
  function headingCell(column) {
    var classes = ["sortable"];
    if (column.kind === "num") classes.push("num");
    if (pinClass(column)) classes.push(pinClass(column));
    return '<th scope="col" class="' + classes.join(" ") + '" data-key="' + column.key + '">' +
      '<button type="button">' + escapeHtml(column.label) +
      ' <span class="arrow">&#9650;</span></button></th>';
  }

  function buildHeader() {
    thead.innerHTML = "<tr>" + COLUMNS.map(headingCell).join("") + "</tr>";
  }


  /* ---- Sorting -------------------------------------------------------- */

  // What a column sorts by: numbers and ISO dates as they are, authorization
  // by its strength rather than its label, everything else as text.
  function sortValue(row, column) {
    var value = row[column.key];
    if (column.kind === "num" || column.kind === "date") return value;
    if (column.key === "auth_label") return row.auth_level;
    return String(value == null ? "" : value);
  }

  // Blanks always sort last; ties fall back to the # order.
  function compareRows(a, b) {
    var column = columnFor(sortKey);
    var va = sortValue(a, column);
    var vb = sortValue(b, column);
    var aBlank = va == null || va === "";
    var bBlank = vb == null || vb === "";
    if (aBlank && bBlank) return a.idx - b.idx;
    if (aBlank) return 1;
    if (bBlank) return -1;
    if (typeof va === "string" && column.kind !== "num") {
      var order = va.localeCompare(vb);
      return order !== 0 ? order * sortDirection : a.idx - b.idx;
    }
    return va === vb ? a.idx - b.idx : (va - vb) * sortDirection;
  }

  // Clicking the sorted column reverses it. A new column starts highest
  // first for numbers and authorization, lowest first for the rest.
  function sortBy(key) {
    if (key === sortKey) {
      sortDirection = -sortDirection;
    } else {
      var column = columnFor(key);
      sortKey = key;
      sortDirection = column.kind === "num" || key === "auth_label" ? -1 : 1;
    }
    render();
  }

  // Mark the sorted heading, and say in the toolbar what the order is.
  function showSortState() {
    thead.querySelectorAll("th.sortable").forEach(function (th) {
      var arrow = th.querySelector(".arrow");
      if (th.dataset.key === sortKey) {
        th.setAttribute("aria-sort", sortDirection === 1 ? "ascending" : "descending");
        arrow.innerHTML = sortDirection === 1 ? "&#9650;" : "&#9660;";
      } else {
        th.removeAttribute("aria-sort");
        arrow.innerHTML = "&#9650;";
      }
    });
    document.getElementById("sort-state").textContent =
      columnFor(sortKey).label + ", " + (sortDirection === 1 ? "lowest first" : "highest first");
  }


  /* ---- Drawing -------------------------------------------------------- */

  function render() {
    var rows = ROWS.slice();
    rows.sort(compareRows);
    tbody.innerHTML = rows.map(function (row) {
      return "<tr>" + COLUMNS.map(function (column) {
        return renderCell(column, row);
      }).join("") + "</tr>";
    }).join("");
    document.getElementById("count").textContent = rows.length + " of " + ROWS.length;
    showSortState();
  }

  // The numbered list of sources at the foot of the page.
  function renderSources() {
    document.getElementById("reflist").innerHTML = SOURCES.map(function (source) {
      var number = source[0];
      var label = escapeHtml(source[1]);
      var url = source[2];
      var text = url ? '<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + label + "</a>" : label;
      return '<li id="ref-' + number + '">' + text + "</li>";
    }).join("");
  }


  /* ---- Start ---------------------------------------------------------- */

  buildHeader();

  thead.querySelectorAll("th.sortable button").forEach(function (button) {
    button.addEventListener("click", function () {
      sortBy(button.parentNode.dataset.key);
    });
  });

  document.getElementById("reset").addEventListener("click", function () {
    sortKey = "idx";
    sortDirection = 1;
    render();
  });

  renderSources();
  render();
})();
