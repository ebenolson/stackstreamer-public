
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


function toggleArrowBar() {
  b1 = $('<div class="box"></div>');
  b1.css('left', 0);
  b1.css('top', 0);  
  b1.attr('id','box1');
  $('#container').append(b1)

  b2 = $('<div class="box"></div>');
  b2.css('left', 200);
  b2.css('top', 300);  
  b2.attr('id','box2');
  $('#container').append(b2)

  jsPlumb.connect({
    source: $('#box1'), 
    target:$('#box2'),
    endpoint:"Blank",
    overlays:[[ "Arrow", { location:1, } ],],
    connector:"Straight",
    paintStyle:{ strokeStyle:"black", lineWidth:"2pt"},
    detachable:false,
    anchors:["AutoDefault", "Center"],
  });

  jsPlumb.draggable($('#box2'));
}

function saveArrow() {
  target = $('<div class="clicktarget"></div>');
  target.css('left', $('#container').css('left'));
  target.css('top', $('#container').css('top'));  
  target.css('width', $('#container').css('width'));  
  target.css('height', $('#container').css('height'));
  $('#viewport').append(target)
  $('.clicktarget').click(function(event) {
    console.log('clicked');
    var offset = $('.clicktarget').offset(); 
    var mouseX = event.pageX - offset.left;
    var mouseY = event.pageY - offset.top;

    var x = mouseX*Math.pow(2, $('#container').data('zoom'));
    var y = mouseY*Math.pow(2, $('#container').data('zoom'));

    var data = JSON.stringify({"pixel_x":x,
            "pixel_y":y,
            "layer":$('#container').data('slice'),
            "stack":"/api/v1/stack/"+info.id+'/',
            "zoom":$('#container').data('zoom'),
            });

    $.ajax ({
              url: '/api/v1/arrow/?format=json',
              type: "POST",
              data: data,
              dataType: "json",
              contentType: "application/json; charset=utf-8",
              complete: loadArrowBar,
            }
    );
    $('.clicktarget').remove();
  });
  /*
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
            url: '/api/v1/arrow/?format=json',
            type: "POST",
            data: data,
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            complete: loadArrowBar,
          }
  );*/
}    


function toggleArrowBar() {
  if ($('#arrowbar').hasClass('inactive')) {
    loadArrowBar();
  }
  $('#arrowbar').toggleClass('inactive');
}

function loadArrowBar() {
  console.log('loading arrows');
  $('#arrowlist').load('/arrows/list/'+info.id+'/', function() {
    $('.arrow_delete a').click( function() {
      $.get(this.target, function() {
        loadArrowBar();
      });
    });
    $('.arrow_link a').click( function() {
      gotoArrow(this.target);
    });

    $('.arrowtext').editable({placement:'right', container:'body'});
  });
}

function gotoArrow(arrowid) {
  var url = sprintf('http://test.stackstreamer.com/api/v1/arrow/%s/?format=json', arrowid);
  $.getJSON(url, function(arrow) {
    setLocation(parseInt(arrow.layer), parseInt(arrow.zoom), parseInt(arrow.pixel_x), parseInt(arrow.pixel_y));
  });
}
