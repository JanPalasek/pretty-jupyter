/* a lot of this code was taken from rmd styles directly included in the output html page, license was not present there but it is GPL3 */

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
      $(this).nextUntil(this.tagName).addBack().wrapAll(`<div id='${id_attr}' class='${class_attr}' />`);

      tabNumber += 1;
    });
  }

    // process all pretty-jupyter-token elements
    $(".pretty-jupyter-token").each(function (i, e) {
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


// code folding 

$(document).ready(function () {

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
});




// dynamically load mathjax for compatibility with self-contained 
(function () {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "https://mathjax.rstudio.com/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML";
  document.getElementsByTagName("head")[0].appendChild(script);
})();


// custom post-processing: remove some ugly styles etc 
$(document).ready(function () {
  // prettify tables
  $("table").addClass("table");
  $("table").addClass("table-striped");
  // $("table").addClass("table-word-wrapped");
  $("table.dataframe").removeAttr("border");

  // remove useless anchor with useless anchor-link
  $("a.anchor-link").remove();
});
