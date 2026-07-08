//windows phone fix
if (navigator.userAgent.match(/IEMobile\/10\.0/)) {
  var msViewportStyle = document.createElement('style')
  msViewportStyle.appendChild(
    document.createTextNode(
      '@-ms-viewport{width:auto!important}'
    )
  )
  document.querySelector('head').appendChild(msViewportStyle)
}

$(document).ready(function() {
  $(".dropdown").on('shown.bs.dropdown', function (e) {
    //function called when dropdown-menu becomes visible
    var dropdownMenu = $('ul:first', this); //find dropdown-menu
    //if element was moved to left, set left back to 0 for next calculations
    $(this).find(".dropdown-menu").first().css('left', 0);
    var offset = dropdownMenu.offset();
    var leftOffset = offset.left;
    var width = dropdownMenu.width();
    var documentWidth = $(document).width();
    console.log(offset);
    console.log(width);
    console.log(documentWidth);
    var sticksOutRightSide = leftOffset + width - documentWidth;
    console.log(sticksOutRightSide);
    if (sticksOutRightSide > 0) {
      console.log("Sticks out");
      $(this).find(".dropdown-menu").first().css('left', -(sticksOutRightSide + 20));
     }
  });
});
