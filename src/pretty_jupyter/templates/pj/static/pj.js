/* a lot of this code was taken from rmd styles directly included in the output html page, license was not present there but it is GPL3 */

MAX_HEADERS = 10;

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

function processToken(tokenElement, targetElement, tokenSep) {
  // Process tokens
  // For each class in token element, it either sets target element ID by it, or adds it to the list of classes
  $.each(tokenElement.text().split(tokenSep), function (tokenIndex, tokenValue) {
    if (tokenValue.startsWith("#")) {
      targetElement.attr("id", tokenValue.substring(1));
    }
    else if (tokenValue.startsWith(".")) {
      targetElement.addClass(tokenValue.substring(1));
    }
    else {
      targetElement.addClass(tokenValue);
    }
  });
}

window.fixElementIds = function() {
  // escape all ids
  $("[id]").attr("id", function (idx, id) {
    // uri decode
    id = decodeURI(id);

    // escape characters
    id = id.replace(/['`~!@#$%^&*()|+=?;:'",.<>\{\}\[\]\\\/]/gi, "")

    return id
  });
};

window.initializeSections = function () {
  let tabNumber = 1;

  // create nested structure:
  // e.g. wrap <h2></h2> into div ending right before the next <h2>
  // so <h2></h2><h2></h2> -> <div><h2></h2></div><div><h2>...
  // note that this assumes linear structure - the h2, h3 etc must be on the
  // same level and not hidden in the nested divs

  for (let h = 1; h <= MAX_HEADERS; h++) {
    $(`#main-content h${h}`).each(function (i, e) {
      let x = h;

      d = {
        "id": tabNumber++ + "",
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
    });
  }
}

window.processTokens = function (tokenSep) {
  // process all pj-token elements
  $("#main-content .pj-token").each(function (i, e) {
    prevSibling = $(this).prev()

    // if we don't have a previous sibling => the element is probably wrapped in paragraph due to markdown compiler
    if (prevSibling.length == 0) {
      prevSibling = $(this).parent().prev()
    }

    // if previous sibling is header => apply tokens to the wrapping section
    processToken(tokenElement = $(this), targetElement = prevSibling, tokenSep = tokenSep)
  });
}

window.processHeaders = function () {
  let customSep = "-O_O-";
  let counterDict = {};
  $("#main-content :header").each(function (idx, e) {
    // get id and class and add it to the wrapping section element
    let sectionElement = $(e).closest("div.section");

    // get id - either from tab number, or from header, if it has one
    let id = $(e).attr("id");
    if (id != null) {
      // initialize id dict
      if (!(id in counterDict)) {
        counterDict[id] = 1;
      }
      $(e).removeAttr("id");

      let newId = id;

      // if has duplicate => modify the ID with counter
      // duplicate can be if counterDict for this id has entry larger than 1 (it has been incremented before)
      // or it found another element with same ID after deleting this elements ID
      let isDuplicate = $(`[id='${id}']`).length > 0 || counterDict[id] > 1
      if (isDuplicate) {
        newId = newId + `${customSep}${counterDict[id]++}`;
      }
      sectionElement.attr("id", newId);
    }

    // get classes from header
    if ($(e).attr("class") != null) {
      $.each($(e).attr('class').split(/\s+/), function (idx, el) {
        sectionElement.addClass(el);
      });

      $(e).attr("class", null);
    }
  })
}

window.initializeCodeFolding = function (show) {
  $("#jup-show-all-code").click(function () {
    $('div.py-code-collapse').each(function () {
      $(this).collapse('show');
    });
  });
  $("#jup-hide-all-code").click(function () {
    $('div.py-code-collapse').each(function () {
      $(this).collapse('hide');
    });
  });

  // index for unique code element ids
  var currentIndex = 1;

  // select all jupyter code blocks
  var jupyterCodeBlocks = $('div.pj-fold');
  jupyterCodeBlocks.each(function () {

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


window.numberSections = function () {
  let headerSelector = "#main-content div.section:not(.unnumbered)>:header"

  let firstLevel = 1;

  // holds current index for each header
  let levels = []
  $(headerSelector).each(function (idx, el) {
    // get current level
    let level = parseInt(this.nodeName.substring(1));

    level = level - firstLevel + 1;

    // current level appeared again => just increment
    if (level == levels.length) {
      levels[level - 1]++;
    }
    // new level appeared => add the new levels and increment
    // e.g.
    // we have h2 and we discovered next new is h4
    // we need to fill in levels for h3 and h4, and then increment h4
    else if (level > levels.length) {
      let levelsLength = levels.length
      for (let i = 0; i < (level - levelsLength); i++) {
        levels.push(0);
      }

      levels[level - 1]++;
    }
    // previous level appeared => we need to shrink
    else if (level < levels.length) {
      levels = levels.slice(0, level);
      levels[level - 1]++;
    }

    numberedText = levels.join(".") + ". " + $(this).text();
    $(this).text(numberedText);
  })
}

window.initializeTOC = function (tocDepth, tocCollapsed, tocSmoothScroll, tocExtendPage) {
  // consistency with pandoc
  $('.unlisted.unnumbered').addClass('toc-ignore')

  // get allowed headers str
  let headers = []
  for (let i = 1; i <= MAX_HEADERS; i++) {
    headers.push(`h${i}`)
  }
  headers = headers.join(",")

  // move toc-ignore selectors from section div to header
  $('div.section.toc-ignore')
    .removeClass('toc-ignore')
    .children(headers).addClass('toc-ignore');

  selectors = []
  for (var i = 0; i < tocDepth; i++) {
    selectors.push(`h${i + 1}`)
  }
  selectors = selectors.join(",");

  // establish options
  var options = {
    selectors: selectors,
    theme: "bootstrap3",
    context: '.toc-content',
    hashGenerator: function (text) {
      return text.replace(/[.\\/?&!#<>"']/g, '').replace(/\s/g, '_');
    },
    ignoreSelector: ".toc-ignore",
    scrollTo: 0,
    extendPage: tocExtendPage
  };

  options.smoothScroll = tocSmoothScroll;

  // tocify
  var toc = $("#TOC").tocify(options).data("toc-tocify");

  if (!tocCollapsed) {
    toc.setOptions({ "showAndHideOnScroll": false, "showAndHide": false });
    $(".tocify-subheader").show();
  }
}

window.initializeTabsets = function () {
  window.buildTabsets("TOC");

  // open tabset-dropdown
  $('.tabset-dropdown > .nav-tabs > li').click(function () {
    $(this).parent().toggleClass('nav-tabs-open')
  });
};
