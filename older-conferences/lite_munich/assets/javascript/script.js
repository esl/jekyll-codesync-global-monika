/* begin Page */
var artEventHelper = {
  'bind' : function (obj, evt, fn) {
    if (obj.addEventListener)
      obj.addEventListener(evt, fn, false);
    else if (obj.attachEvent)
      obj.attachEvent('on' + evt, fn);
    else
      obj['on' + evt] = fn;
  }
};

var artLoadEvent = (function() {
  var userAgent = navigator.userAgent.toLowerCase();
  var browser = {
    version: (userAgent.match(/.+(?:rv|it|ra|ie)[\/: ]([\d.]+)/) || [])[1],
    safari: /webkit/.test(userAgent),
    opera: /opera/.test(userAgent),
    msie: /msie/.test(userAgent) && !/opera/.test(userAgent),
    mozilla: /mozilla/.test(userAgent) && !/(compatible|webkit)/.test(userAgent)
  };

  var list = [];

  var done = false;
  var ready = function () {
    if (done) return;
    done = true;
    for (var i = 0; i < list.length; i++)
      list[i]();
  };

  if (document.addEventListener && !browser.opera)
    document.addEventListener('DOMContentLoaded', ready, false);

  if (browser.msie && window == top) {
    (function () {
      try {
        document.documentElement.doScroll('left');
      } catch (e) {
        setTimeout(arguments.callee, 10);
        return;
      }
      ready();
    })();
  }

  if (browser.opera) {
    document.addEventListener('DOMContentLoaded', function () {
      for (var i = 0; i < document.styleSheets.length; i++) {
        if (document.styleSheets[i].disabled) {
          setTimeout(arguments.callee, 10);
          return;
        }
      }
      ready();
    }, false);
  }

  if (browser.safari) {
    var numStyles;
    (function(){
      if (document.readyState != 'loaded' && document.readyState != 'complete') {
        setTimeout(arguments.callee, 10);
        return;
      }
      if ('undefined' == typeof numStyles) {
        numStyles = document.getElementsByTagName('style').length;
        var links = document.getElementsByTagName('link');
        for (var i = 0; i < links.length; i++) {
          numStyles += (links[i].getAttribute('rel') == 'stylesheet') ? 1 : 0;
        }
        if (document.styleSheets.length != numStyles) {
          setTimeout(arguments.callee, 0);
          return;
        }
      }
      ready();
    })();
  }

  artEventHelper.bind(window, 'load', ready);

  return ({
    add: function(f) {
      list.push(f);
    }
  })
})();

(function () {
  // fix ie blinking
  var m = document.uniqueID && document.compatMode && !window.XMLHttpRequest && document.execCommand;
  try{ if(!!m) { m("BackgroundImageCache", false, true); } }
  catch(oh){};
})();

function xGetElementsByClassName(clsName, parentEle, tagName) {
  var elements = null;
  var found = [];
  var slash = String.fromCharCode(92);
  var re = new RegExp(slash + "b" + clsName + slash + "b");
  if (!parentEle) parentEle = document;
  if (!tagName) tagName = '*';
  elements = parentEle.getElementsByTagName(tagName);
  if (elements) {
    for (var i = 0; i < elements.length; ++i) {
      if (elements[i].className.search(re) != -1) {
        found[found.length] = elements[i];
      }
    }
  }
  return found;
}

function artButtonSetupJsHover(btn)
{
  artEventHelper.bind(btn, 'mouseover', function() {
    var spans = btn.getElementsByTagName("span");
    if (spans.length > 0)
      spans[0].className += " hover";
  });
  artEventHelper.bind(btn, 'mouseout', function() {
    var spans = btn.getElementsByTagName("span");
    if (spans.length > 0)
      spans[0].className = spans[0].className.replace(/hover/, "");
  });
}

function artButtonsSetupJsHover() {
  var elements = xGetElementsByClassName("btn", document, "span");
  for (var i = 0; i < elements.length; i++) {
    if (!elements[i].tagName) continue;
    artButtonSetupJsHover(elements[i].parentNode);
  }
}

artLoadEvent.add(artButtonsSetupJsHover);
/* end Page */

/* begin Menu */
function Insert_Separators()
{
  var menus = xGetElementsByClassName("menu", document);
  for (var i = 0; i < menus.length; i++) {
    var menu = menus[i];
    var childs = menu.childNodes;
    var listItems = [];
    for (var j = 0; j < childs.length; j++){
      var el = childs[j];
      if (String(el.tagName).toLowerCase() == "li")listItems.push(el);
    }
    for (var j = 0; j < listItems.length - 1; j++){
      var span = document.createElement('span');
      span.className = 'separator';
      var li = document.createElement('li');
      li.appendChild(span);
      listItems[j].parentNode.insertBefore(li, listItems[j].nextSibling);
    }
  }
}
artLoadEvent.add(Insert_Separators);

function Menu_IE6Setup() {
  var isIE6 = navigator.userAgent.toLowerCase().indexOf("msie") != -1
    && navigator.userAgent.toLowerCase().indexOf("msie 7") == -1;
  if (!isIE6) return;
  var aTmp2, i, j, oLI, aUL, aA;
  var aTmp = xGetElementsByClassName("menu", document, "ul");
  for (i=0;i<aTmp.length;i++) {
    aTmp2 = aTmp[i].getElementsByTagName("li");
    for (j=0;j<aTmp2.length;j++) {
      oLI = aTmp2[j];
      aUL = oLI.getElementsByTagName("ul");
      if (aUL && aUL.length) {
        oLI.UL = aUL[0];
        aA = oLI.getElementsByTagName("a");
        if (aA && aA.length)
          oLI.A = aA[0];
        oLI.onmouseenter = function() {
          this.className += " menuhover";
          this.UL.className += " menuhoverUL";
          if (this.A) this.A.className += " menuhoverA";
        };
        oLI.onmouseleave = function() {
          this.className = this.className.replace(/menuhover/,"");
          this.UL.className = this.UL.className.replace(/menuhoverUL/,"");
          if (this.A) this.A.className = this.A.className.replace(/menuhoverA/,"");
        };
      }
    }
  }
}
artLoadEvent.add(Menu_IE6Setup);
/* end Menu */

/* Conference programme */
$(document).ready(function(){
  var $tableBody = $('#cProgrammeTable');
  if($tableBody.length) {
    var colsNum = Math.max($tableBody.find('tr')[0].cells.length - 1, 1); // avoid division by zero when no columns
    var totalWidth = $tableBody.width();
    var timelineWidth = $('#cProgrammeTable tr:first').find('.timeline').width();
    var newWidth = (totalWidth - timelineWidth) / colsNum;
    $("#cProgrammeTable tr:first").find('td').not('.timeline').css('min-width', newWidth + 'px');
  }
  var shaded = false;
  function isShaded(element) {
    return $(element).parent().hasClass("shaded");
  }
  function addShade(tag) {
    tagString = "." + $(tag).text();
    $(".shadeable").not(tagString).addClass("shaded");
  }
  function removeShade(track) {
    $(".shadeable").removeClass("shaded");
  }
  $(".talktag").click(function () {
    if (shaded) {
      removeShade();
      shaded = false;
    } else {
      addShade(this);
      shaded = true;
    }
  });
  var colors = ["DEAAC6", "#AADEC2", "#DEDCAA", "#AAABDE", "#AAABDE", "#ABDEAA", "#DEC2AA", "#AAC6DE", "#DEAAAB", "#AADEDC", "#AADEDC", "#ABDEAA"];
  var i = 0;
  var tagColors = {};
  $(".talktag").each(function () {
    tag = $(this).text()
    color = tagColors[tag];
    if (color == undefined) {
      tagColors[tag] = colors[i];
      $(this).css('background-color', colors[i]);
      i = i + 1;
    } else {
      $(this).css('background-color', color);
    }
    console.log("ok");
  });
});
/* end Conference programme */
