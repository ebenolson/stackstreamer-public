
function saveFlag() {
  var x = $(window).width()/2-$('#container').offset().left;
  x = x*Math.pow(2, $('#container').data('zoom'));
  var y = $(window).height()/2-$('#container').offset().top;
  y = y*Math.pow(2, $('#container').data('zoom'));
  console.log(x, y);
  var data = JSON.stringify({"pixel_x":x,
          "pixel_y":y,
          "layer":$('#container').data('slice'),
          "stack":"/api/v1/stack/"+info.id+'/',
          "zoom":$('#container').data('zoom'),
          });

  $.ajax ({
            url: '/api/v1/flag/?format=json',
            type: "POST",
            data: data,
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            complete: loadFlagBar,
          }
  );
}    

function loadFlagBar() {
  console.log('loading flags');
  $('#flaglist').load('/flags/list/'+info.id+'/', function() {
    $('.flag_delete a').click( function() {
      $.get(this.target, function() {
        loadFlagBar();
      });
    });
    $('.flag_link a').click( function() {
      gotoFlag(this.target);
    });
    //$('.flagtext').popover();
    $('.flagtext').editable({placement:'right', container:'body'});
    //$('#flaglist').jScrollPane();
  });
}

function gotoFlag(flagid) {
  var url = sprintf('http://test.stackstreamer.com/api/v1/flag/%s/?format=json', flagid);
  $.getJSON(url, function(flag) {
    setLocation(parseInt(flag.layer), parseInt(flag.zoom), parseInt(flag.pixel_x), parseInt(flag.pixel_y));
  });
}

function toggleFlagBar() {
  if ($('#flagbar').hasClass('inactive')) {
    loadFlagBar();
  }
  $('#flagbar').toggleClass('inactive');
}
