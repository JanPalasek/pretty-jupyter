/* a lot of this code was taken from rmd styles directly included in the output html page, license was not present there but it is GPL3 */

// nextUntilWithTextNodes does the same as nextUntil but it doesn't ignore text nodes
// credits: https://stackoverflow.com/questions/25873650/jquery-nextuntil-include-text-nodes
$.fn.nextUntilWithTextNodes = function (until) {
  var matched = $.map(this, function (elem, i, until) {
      var matched = [];
      while ((elem = elem.nextSibling) && elem.nodeType !== 9) {
          if (elem.nodeType === 1 || elem.nodeType === 3) {
              if (until && jQuery(elem).is(until)) {
                  break;
              }
              matched.push(elem);
          }
      }
      return matched;
  }, until);

  return this.pushStack(matched);
};


// custom preprocessing

$(document).ready(function () {
  let tabNumber = 1;

  // create nested structure:
  // e.g. wrap <h2></h2> into div ending right before the next <h2>
  // so <h2></h2><h2></h2> -> <div><h2></h2></div><div><h2>...
  // note that this assumes linear structure - the h2, h3 etc must be on the
  // same level and not hidden in the nested divs

  for (let h = 1; h <= 8; h++) {
    $(`h${h}`).each(function(i,e) {
      let x = h;

      d = {
        "id": tabNumber + "",
        "class": ["section", `level${x}`],
      };
      
      // add the computed classes and attributes
      class_attr = d["class"].join(" ");
      id_attr = d["id"];
      
      untilNodes = `${this.tagName}`
      for (let hPrev = 1; hPrev < x; hPrev++) {
        untilNodes += `,.level${hPrev}`
      }

      $(this).nextUntilWithTextNodes(untilNodes).addBack().wrapAll(`<div id='${id_attr}' class='${class_attr}' />`);

      tabNumber += 1;
    });
  }

    // process all pj-token elements (pretty-jupyter-token for backwards compatibility)
    $(".pj-token,.pretty-jupyter-token").each(function (i, e) {
      // if it has tabset, add tabset class to the section
      if ($(this).hasClass("tabset")) {
        $(this).parent().closest(".section").addClass("tabset");
      }
      // if the element has tabset-pills => add tabset-pills to the section
      if ($(this).hasClass("tabset-pills")) {
        $(this).parent().closest(".section").addClass("tabset-pills");
      }
    });

});

window.initializeCodeFolding = function(show) {
  $("#jup-show-all-code").click(function() {
    $('div.py-code-collapse').each(function() {
      $(this).collapse('show');
    });
  });
  $("#jup-hide-all-code").click(function() {
    $('div.py-code-collapse').each(function() {
      $(this).collapse('hide');
    });
  });

  // index for unique code element ids
  var currentIndex = 1;

  // select all jupyter code blocks
  var jupyterCodeBlocks = $('div.pj-input');
  jupyterCodeBlocks.each(function() {

    // create a collapsable div to wrap the code in
    var div = $('<div class="collapse py-code-collapse"></div>');
    var showThis = (show || $(this).hasClass('fold-show')) && !$(this).hasClass('fold-hide');
    if (showThis) div.addClass('in');
    var id = 'code-643E0F36' + currentIndex++;
    div.attr('id', id);
    $(this).before(div);
    $(this).detach().appendTo(div);

    // add a show code button right above
    var showCodeText = $('<span>' + (showThis ? 'Hide' : 'Code') + '</span>');
    var showCodeButton = $('<button type="button" class="btn btn-default btn-xs code-folding-btn pull-right"></button>');
    showCodeButton.append(showCodeText);
    showCodeButton
        .attr('data-toggle', 'collapse')
        .attr('data-target', '#' + id)
        .attr('aria-expanded', showThis)
        .attr('aria-controls', id);

    var buttonRow = $('<div class="row"></div>');
    var buttonCol = $('<div class="col-md-12"></div>');

    buttonCol.append(showCodeButton);
    buttonRow.append(buttonCol);

    div.before(buttonRow);

    // update state of button on show/hide
    div.on('hidden.bs.collapse', function () {
      showCodeText.text('Code');
    });
    div.on('show.bs.collapse', function () {
      showCodeText.text('Hide');
    });
  });
}

window.initializeTOC = function() {
  // temporarily add toc-ignore selector to headers for the consistency with Pandoc
  $('.unlisted.unnumbered').addClass('toc-ignore')

  // move toc-ignore selectors from section div to header
  $('div.section.toc-ignore')
    .removeClass('toc-ignore')
    .children('h1,h2,h3,h4,h5').addClass('toc-ignore');

  // establish options
  var options = {
    selectors: "h1,h2,h3",
    theme: "bootstrap3",
    context: '.toc-content',
    hashGenerator: function (text) {
      return text.replace(/[.\\/?&!#<>]/g, '').replace(/\s/g, '_');
    },
    ignoreSelector: ".toc-ignore",
    scrollTo: 0
  };
  options.showAndHide = true;
  options.smoothScroll = true;

  // tocify
  var toc = $("#TOC").tocify(options).data("toc-tocify");
}


if (window.hljs) {
    hljs.configure({
        languages: []
    });
    hljs.initHighlightingOnLoad();

    if (document.readyState && document.readyState === "complete") {
        window.setTimeout(function () {
            hljs.initHighlighting();
        }

            , 0);
    }
}

// add bootstrap table styles to pandoc tables
function bootstrapStylePandocTables() {
  $('tr.odd').parent('tbody').parent('table').addClass('table table-condensed');
}
$(document).ready(function () {
  bootstrapStylePandocTables();
});




// tabsets 
$(document).ready(function () {
  window.buildTabsets("TOC");
});

$(document).ready(function () {
  $('.tabset-dropdown > .nav-tabs > li').click(function () {
    $(this).parent().toggleClass('nav-tabs-open')
  });
});


// custom post-processing: remove some ugly styles etc 
$(document).ready(function () {
  // prettify tables (that aren't ignored)
  $("table:not(.pj-tab-ignore)").addClass("table");
  $("table:not(.pj-tab-ignore)").addClass("table-striped");
  $("table.dataframe:not(.pj-tab-ignore)").removeAttr("border");

  // remove useless anchor with useless anchor-link
  $("a.anchor-link").remove();
});
