function saveExport() {
  target = $('<div class="clicktarget"></div>');
  target.css('left', $('#container').css('left'));
  target.css('top', $('#container').css('top'));  
  target.css('width', $('#container').css('width'));  
  target.css('height', $('#container').css('height'));
  $('#viewport').append(target);
  $('body').append($('<div class="exportpopup" style="display:none"><h2><span class="label label-info">Click and drag to select export region</span></h2></div>'));
  $('.exportpopup').bPopup({
    appendTo:'container',
    autoClose:1000,
    modal:false,
  });
  $('.clicktarget').mousedown(function(event) {
    console.log('clicked');
    var offset = $('.clicktarget').offset(); 
    var mouseX = event.pageX - offset.left;
    var mouseY = event.pageY - offset.top;

    var px0 = mouseX*Math.pow(2, $('#container').data('zoom'));
    var py0 = mouseY*Math.pow(2, $('#container').data('zoom'));
    var layer0 = $('#container').data('slice');

    $('.clicktarget').append($('<div class="dragbox"></div>'));
    $('.dragbox').css('left', mouseX);
    $('.dragbox').css('top', mouseY);

    $('.clicktarget').mousemove(function(event) {
      var newmouseX = event.pageX - offset.left;
      var newmouseY = event.pageY - offset.top;
      x0 = Math.min(mouseX, newmouseX);
      y0 = Math.min(mouseY, newmouseY);
      x1 = Math.max(mouseX, newmouseX);
      y1 = Math.max(mouseY, newmouseY);

      $('.dragbox').css('left', x0);
      $('.dragbox').css('top', y0);
      $('.dragbox').css('width', x1-x0);
      $('.dragbox').css('height', y1-y0);
    });

    $('.clicktarget').mouseup(function(event) {
      var offset = $('.clicktarget').offset(); 
      var mouseX = event.pageX - offset.left;
      var mouseY = event.pageY - offset.top;
      var px1 = mouseX*Math.pow(2, $('#container').data('zoom'));
      var py1 = mouseY*Math.pow(2, $('#container').data('zoom'));

      $('.clicktarget').unbind('mousemove');
      $('.clicktarget').unbind('mousedown');

      $('.exportpopup').remove();
      $('body').append($('<div class="exportpopup" style="display:none"><h2><span class="label label-info">Navigate to final layer and click to complete selection</span></h2></div>'));
      $('.exportpopup').bPopup({
        appendTo:'container',
        autoClose:1000,
        modal:false,
      });

      $('.clicktarget').mouseup(function(event) {
        var layer1 = $('#container').data('slice');

        $('.clicktarget').remove();
        $('.exportpopup').remove();

        $.get('/export/dataexport/', function(data) {
          bootbox.dialog({
            message: data,
            title:"Export Region",
            buttons: {
                      success: {
                        label: "Create Data Export",
                        className: "btn-success",
                        callback: function () {
                          $('#exportform').ajaxSubmit();
                        }
                      }
            } 
          });

          $('#id_pixel_x0').attr('value',px0);
          $('#id_pixel_x1').attr('value',px1);
          $('#id_pixel_y0').attr('value',py0);
          $('#id_pixel_y1').attr('value',py1);

          $('#id_layer0').attr('value',layer0);
          $('#id_layer1').attr('value',layer1);
          $('#id_stack').attr('value',info.id);
        });
      });
    });
  });
}

function saveSnapshot() {
  var x0, x1, y0, y1;
  x0 = -$('#container').offset().left;
  x1 = x0+$(window).width();
  y0 = -$('#container').offset().top;
  y1 = y0+$(window).height();
  var url = sprintf('/export/snapshot/%s/%d/%d/%d/%d/%d/%d', info['uuid'], $('#container').data('slice'), $('#container').data('zoom'), x0, y0, x1, y1);
  console.log(url);
  $('a#snapshotbutton').attr('href',url).attr('download','snapshot.png');
}
