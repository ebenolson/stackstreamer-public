// Connect to Binary.js server
var client;
var controlStream;

var info;
var TILESIZES = [256, 323, 406];
var VIEWPORTW = $(window).width();
var VIEWPORTH = $(window).height();

var lastUpdatePos = {'left':0,'top':0};

var lmb = false;
var stack_opened = false;
var tiles_loading = 0;
var highResLoaded = false;
//var streams = {};
var tilecache = {};
var cachedBordering = false;
var cachedAboveBelow = false;
var cacheCount = 0;

var subZoom = 0;
var subZoomLevels = 3;

function hideWarning() {
  $('#chromerequired').remove();
  $('#viewport').removeClass('hidden');
}


function openStack() {
  var url = $.url();
  var uuid = url.param('id');
  controlStream.write({'action':'open', 'uuid':uuid});
  stack_opened = true;
} 

function loadImage(target, src) {
  if (src in tilecache) {
    //console.log('load from cache');
    $('#'+target+' img').attr('src', $('#cached_'+tilecache[src]+' img').attr('src'));
    return;
  }
  controlStream.write({'action':'send', 'path':src, 'target':target});
  tiles_loading += 1;
}

function cacheImage(src) {
  if (cacheCount > 500) {
    clearCache();
  } 
  if (src in tilecache) {
    //console.log('already in cache');
    return;
  }
  else {
    //console.log('caching '+ src);
    tilecache[src] = jsmd5(src);
    tile = $('<div class="tile cached hidden"><img src=""/></div>');
    tile.attr('id','cached_'+src);

    controlStream.write({'action':'send', 'path':src, 'target':'cached_'+tilecache[src]});
    tiles_loading += 1;
    cacheCount += 1;
  }
}

function clearCache() {
  $('.cached').remove();
  tilecache = {};
  cacheCount = 0;
}

function buildTiles() {
  $('.tile').remove();

  var nx = info['tile sets'][$('#container').data('zoom')]['nx'];
  var ny = info['tile sets'][$('#container').data('zoom')]['ny'];

  for (x=0; x<nx; x++) {
    for (y=0; y<ny; y++) {
      tile = $('<div class="tile"><img src=""/></div>');
      tile.data('x', x);
      tile.data('y', y);
      tile.attr('id', 'tile_'+x+'_'+y)
      tile.addClass('hidden');
      $('#container').append(tile);
    }
  }

  $('.tile').each( function () {
    $(this).css('left', $(this).data('x')*TILESIZES[subZoom]);
    $(this).css('top', $(this).data('y')*TILESIZES[subZoom]);
  });
}

function buildViewer(slice, zoom) {
  el = $('<div id="container" data-slice=1 data-zoom=0></div>');
  el.data('zoom', zoom);
  el.data('slice',slice);
  $('#viewport').prepend(el);
  var nx = info['tile sets'][zoom]['nx'];
  var ny = info['tile sets'][zoom]['ny'];
  $('#container').css('width', nx*TILESIZES[subZoom]);
  $('#container').css('height', ny*TILESIZES[subZoom]);

  $('#viewport').css('width', VIEWPORTW);
  $('#viewport').css('height', VIEWPORTH);

  return el;      
}

function goHome() {
  console.log('going home');
  var zoom = info['tile sets'].length-1;
  var layer = parseInt(info['number of slices']/2);
  var nx = info['tile sets'][0]['nx'];
  var ny = info['tile sets'][0]['ny'];
  setLocation(layer, zoom, nx*TILESIZES[subZoom]/2, ny*TILESIZES[subZoom]/2);
  console.log(nx*TILESIZES[subZoom]/2);
}

function buildInfo() {
  for (i=info['number of slices']-1; i>=0; i--) {
    tile = $('<div class="layericon"><img src="./assets/icon_layer.svg"/></div>');
    tile.attr('id', 'layericon'+i);
    tile.data('layer', i);
    tile.css('top', 100+800*i/info['number of slices']);
    $('#info').append(tile);      
  }
  $('.layericon').click( function() {
    changeLayer($(this).data('layer'));
  });      
  $('.layericon img').hover(function() {
    $(this).attr('src', "./assets/icon_layer_hover.svg");
  }, function() {
    if ($(this).closest('.layericon').hasClass('active')) {
      $(this).attr('src', "./assets/icon_layer_selected.svg");
    }
    else {
      $(this).attr('src', "./assets/icon_layer.svg");     
    }
  });
  $('.layericon').on('dragstart', function(event) { event.preventDefault(); });
}

function cacheBordering() {
  cachedBordering = true;  

  var x0 = -parseInt($('#container').css('left'));
  var y0 = -parseInt($('#container').css('top'));

  var nxmin = Math.max(0, Math.floor(x0/TILESIZES[subZoom])-1);
  var nymin = Math.max(0, Math.floor(y0/TILESIZES[subZoom])-1);
  var nxmax = Math.min(info['tile sets'][$('#container').data('zoom')]['nx'], Math.ceil(x0/TILESIZES[subZoom]+VIEWPORTW/TILESIZES[subZoom])+1);
  var nymax = Math.min(info['tile sets'][$('#container').data('zoom')]['ny'], Math.ceil(y0/TILESIZES[subZoom]+VIEWPORTH/TILESIZES[subZoom])+1);

  for (var i=nxmin-1; i<=nxmax+1; i++) {
    for (var j=nymin-1; j<=nymax+1; j++) {
      if ($('div.tile#tile_'+i+'_'+j).length != 1) {
        cacheImage(sprintf("/zoom%1d/slice_%04d/tile_x%04d_y%04d.20.jpg", 
                  $('#container').data('zoom'), $('#container').data('slice'), i, j));                        
      }
    }
  }
}

function cacheAboveBelow() {
  cachedAboveBelow = true;

  //console.log('cache above below');
  var x0 = -parseInt($('#container').css('left'));
  var y0 = -parseInt($('#container').css('top'));

  var nxmin = Math.max(0, Math.floor(x0/TILESIZES[subZoom])-1);
  var nymin = Math.max(0, Math.floor(y0/TILESIZES[subZoom])-1);
  var nxmax = Math.min(info['tile sets'][$('#container').data('zoom')]['nx'], Math.ceil(x0/TILESIZES[subZoom]+VIEWPORTW/TILESIZES[subZoom])+1);
  var nymax = Math.min(info['tile sets'][$('#container').data('zoom')]['ny'], Math.ceil(y0/TILESIZES[subZoom]+VIEWPORTH/TILESIZES[subZoom])+1);

  for (var i=nxmin; i<=nxmax; i++) {
    for (var j=nymin; j<=nymax; j++) {
      cacheImage(sprintf("/zoom%1d/slice_%04d/tile_x%04d_y%04d.20.jpg", 
                $('#container').data('zoom'), $('#container').data('slice')-1, i, j));                        
      cacheImage(sprintf("/zoom%1d/slice_%04d/tile_x%04d_y%04d.20.jpg", 
                $('#container').data('zoom'), $('#container').data('slice')+1, i, j));                        
    }
  }
}

function updateVisibleTiles() {
  var x0 = -parseInt($('#container').css('left'));
  var y0 = -parseInt($('#container').css('top'));

  var nxmin = Math.max(0, Math.floor(x0/TILESIZES[subZoom])-1);
  var nymin = Math.max(0, Math.floor(y0/TILESIZES[subZoom])-1);
  var nxmax = Math.min(info['tile sets'][$('#container').data('zoom')]['nx'], Math.ceil(x0/TILESIZES[subZoom]+VIEWPORTW/TILESIZES[subZoom])+1);
  var nymax = Math.min(info['tile sets'][$('#container').data('zoom')]['ny'], Math.ceil(y0/TILESIZES[subZoom]+VIEWPORTH/TILESIZES[subZoom])+1);
  //console.log(nxmin, nxmax);
  //console.log(nxmax);
  //console.log(nymin);
  //console.log(nymax);
  $('.tile').each( function () {
    var nx = $(this).data('x');
    var ny = $(this).data('y');
    if (nx < nxmin || nx > nxmax || ny < nymin || ny > nymax) {
      $(this).remove();
    }
  });

  for (var i=nxmin; i<=nxmax; i++) {
    for (var j=nymin; j<=nymax; j++) {
      if ($('div.tile#tile_'+i+'_'+j).length != 1) {
        tile = $('<div class="tile"><img src=""/></div>');
        tile.data('x', i);
        tile.data('y', j);
        tile.attr('id', 'tile_'+i+'_'+j)
        //tile.addClass('hidden');
        tile.css('left', tile.data('x')*TILESIZES[subZoom]);
        tile.css('top', tile.data('y')*TILESIZES[subZoom]);          
        $('#container').append(tile);
        loadImage(tile.attr('id'), sprintf("/zoom%1d/slice_%04d/tile_x%04d_y%04d.20.jpg", 
                  $('#container').data('zoom'), $('#container').data('slice'), tile.data('x'), tile.data('y')));                        
      }
    }
  }

  $('#container .tile').removeClass('subzoom0').removeClass('subzoom1').removeClass('subzoom2').addClass('subzoom'+subZoom);
}

function dragUpdate(event, ui) {
  if (Math.abs(ui.position.left-lastUpdatePos.left)>64 || Math.abs(ui.position.top-lastUpdatePos.top)>64) {
    console.log('drag update');
    lastUpdatePos = ui.position;
    updateVisibleTiles();

    cachedBordering = false;
    highResLoaded = false;
  }
  //preloadBordering();     
}

function updateInfo() {
  $('#info #slice').text(sprintf("Layer %d of %d", $('#container').data('slice')+1, info['number of slices']));
  var scale = Math.pow(2, $('#container').data('zoom'));
  $('#info #zoom').text(sprintf("Scale 1 : %d", scale));

  $('.layericon,.active img').attr('src', "./assets/icon_layer.svg");
  $('.layericon,.active').removeClass('active');
  $('#layericon'+$('#container').data('slice')).addClass('active');

  $('.layericon,.active img').attr('src', "./assets/icon_layer_selected.svg");           

  if (!$('#arrowbar').hasClass('inactive')) {
    loadArrowMarkers();
  }
}

function updateTileImages() {
  updateVisibleTiles();
//      highResLoaded = false;
//      $('.tile:not(.hidden)').each( function () {
//        loadImage($(this).attr('id'), sprintf("/zoom%1d/slice_%04d/tile_x%04d_y%04d.20.jpg", 
//          $('#container').data('zoom'), $('#container').data('slice'), $(this).data('x'), $(this).data('y')));
//      });
}

function loadHighresTileImages() {
  highResLoaded = true;
  $('.tile:not(.highres)').each( function () {
    loadImage($(this).attr('id'), sprintf("/zoom%1d/slice_%04d/tile_x%04d_y%04d.80.jpg", 
      $('#container').data('zoom'), $('#container').data('slice'), $(this).data('x'), $(this).data('y')));
    $(this).addClass('highres');
  });
}

function setLocation(layer, zoom, centerX, centerY) {
  el = $('#container');

  if (zoom<0) { zoom=0; }
  if (zoom>info['tile sets'].length-1) { zoom = info['tile sets'].length-1; }


  el.data('zoom',zoom);

  var nx = info['tile sets'][$('#container').data('zoom')]['nx'];
  var ny = info['tile sets'][$('#container').data('zoom')]['ny'];
  $('#container').css('width', nx*TILESIZES[subZoom]);
  $('#container').css('height', ny*TILESIZES[subZoom]);      

  var x = centerX/Math.pow(2, zoom);
  x = $(window).width()/2 - x;
  var y = centerY/Math.pow(2, zoom);
  y = $(window).height()/2 - y;
  el.css('left', x);
  el.css('top', y);

  el.children('.tile').remove();

  if (layer<0) { layer=0; }
  if (layer>info['number of slices']-1) { layer = info['number of slices']-1; }
  el.data('slice', layer);

  updateTileImages();
  updateInfo();    

  cachedBordering = false;
  cachedAboveBelow = false;
  highResLoaded = false;
  clearCache();
}

function changeZoom(zoom, subzoom, event) {
  console.log('changeZoom ', zoom, subzoom);
  if ($('.oldcontainer').length != 0) return;

  el = $('#container');
  oldzoom = el.data('zoom');

  if (zoom<0) return;
  if (zoom>info['tile sets'].length-1) return;
  if (zoom == oldzoom && subzoom == subZoom) return;
  if (subzoom < 0 || subzoom >= subZoomLevels) return;
  
  var parentOffset = $('#viewport').offset(); 
//or $(this).offset(); if you really just want the current element's offset
  if (event == false) {
    var mouseX = 0;
    var mouseY = 0;
  }
  else {
    var mouseX = event.pageX - parentOffset.left;
    var mouseY = event.pageY - parentOffset.top;
  }
  oldContainerX = parseInt(el.css('left'));
  oldContainerY = parseInt(el.css('top'));      
  newContainerX = mouseX - (mouseX - oldContainerX) * Math.pow(2, oldzoom-zoom - (subZoom-subzoom)/subZoomLevels);
  newContainerY = mouseY - (mouseY - oldContainerY) * Math.pow(2, oldzoom-zoom - (subZoom-subzoom)/subZoomLevels);

  oldContainer = el.clone();
  oldContainer.attr('id','').addClass('oldcontainer').prependTo('#viewport');
  oldContainer.children('.tile').attr('id','');

  el.data('zoom',zoom);
  el.css('left', newContainerX);
  el.css('top', newContainerY);

  subZoom = subzoom;

  var nx = info['tile sets'][$('#container').data('zoom')]['nx'];
  var ny = info['tile sets'][$('#container').data('zoom')]['ny'];
  $('#container').css('width', nx*TILESIZES[subZoom]);
  $('#container').css('height', ny*TILESIZES[subZoom]);      

  $('#container').addClass('hidden');
  //buildTiles();     
  el.children('.tile').remove();
  updateInfo();      
  updateTileImages();

  cachedBordering = false;
  cachedAboveBelow = false;
  highResLoaded = false;
  clearCache();  
}

function changeLayer(i) {
  el = $('#container');
  if (i<0) { i=0; }
  if (i>info['number of slices']-1) { i = info['number of slices']-1; }
  el.data('slice', i);

  el.children('.tile').each( function () {
    $(this).removeClass('highres');
    loadImage($(this).attr('id'), sprintf("/zoom%1d/slice_%04d/tile_x%04d_y%04d.20.jpg", 
    $('#container').data('zoom'), $('#container').data('slice'), $(this).data('x'), $(this).data('y')));           
  });
  updateVisibleTiles();

  cachedBordering = false;
  cachedAboveBelow = false;
  highResLoaded = false;

  //updateTileImages();
  updateInfo();
  //console.log(event.deltaX, event.deltaY, event.deltaFactor);
}

function toggleInfo() {
  $('.overlay').toggleClass('hidden');

  if ($('.overlay').hasClass('hidden')) {
    $('.fullscreenpopup').bPopup({
      appendTo:'container',
      autoClose:1000,
      modal:false,
    });
  }
}

function activateControls() {
  $('#viewport').mousewheel(function(event) {
    var delta = event.deltaY;
    if (delta > 1) { delta = 1; }
    if (delta < -1) { delta = -1; }

    if (lmb == true || event.ctrlKey == true) {
      var i = $('#container').data('slice')+delta;
      changeLayer(i);
    }
    else {
      var z = $('#container').data('zoom');
      var sz = subZoom-delta;
      if (sz < 0) {
        sz = subZoomLevels-1;
        z = z+1;
      }
      else if (sz >= subZoomLevels) {
        sz = 0;
        z = z-1;
      }
      changeZoom(z, sz, event);
    }
    event.preventDefault();
  });

  $('body').mousedown(function(event) {
    if (event.which === 1) lmb = true;
  });

  $('body').mouseup(function(event) {
    if (event.which === 1) lmb = false;
  });
/*
  $('#container').mouseup(function(event) {
    if (event.originalEvent.detail === 2) { 
      if (event.which === 3) { // right-click
        var i = $(this).data('zoom')+1;
        changeZoom(i, event);
      } 
      if (event.which === 1) { // right-click
        var i = $(this).data('zoom')-1;
        changeZoom(i, event);
      } 
    }
  });
*/
  $('#container').draggable({ drag: dragUpdate});

  $('#helpbutton').click(doTour);

  $('#flagbutton').click(toggleFlagBar);
  $('#addflagbutton').click(saveFlag);

  $('#arrowbutton').click(toggleArrowBar);
  $('#addarrowbutton').click(saveArrow);

  $('#snapshotbutton').click(saveSnapshot);
  $('#exportbutton').click(saveExport);
    //$('a#snapshotbutton').attr('href','/export/fullslice/7a6e377e-ba80-4756-a857-a23c177722e2/100').attr('download','snapshot.png');

  $('#homebutton').click(goHome);
  $('#hideinfobutton').click(toggleInfo);

  $(document).keyup(function(e) {
    if (e.keyCode == 27) { 
      toggleInfo();
    }
  });
}

function connectToServer() {
  client = new BinaryClient(SERVER_ADDRESS);
  client.on('close', function() {
    console.log('Websocket connection closed, reopening');
    connectToServer();
  });

  client.on('open', function(){
    controlStream = client.createStream();
    if (stack_opened == false) openStack(); 
  });

  client.on('stream', function(stream, meta){
    if (meta['type'] == 'image') {    
      // Buffer for parts
      var parts = [];
      // Got new data
      stream.on('data', function(data){
        parts.push(data);
      });
      stream.on('end', function(){
        // Display new data in browser!
        $('#'+meta['target']+' img').attr('src', (window.URL || window.webkitURL).createObjectURL(new Blob(parts)));
        tiles_loading -= 1;
        stream.destroy();
      });
    }
    if (meta['type'] == 'info') {
      stream.on('data', function(data){         
        console.log('received info');
        info = $.parseJSON(data);

        var url = sprintf('/api/v1/stack/?uuid=%s', info['uuid']);
        $.getJSON( url, function( data ) { 
          info.id = data.objects[0].id;
        });

        updateInfo();
        //buildTiles();         
        buildInfo();
        buildViewer(parseInt(info['number of slices'])/2, info['tile sets'].length-1);
        goHome();
        activateControls();
        setInterval(timerUpdate, 50);
      });
    }
  });

}

function timerUpdate() {
  if (tiles_loading == 0) {
    $('#container').removeClass('hidden');
    $('.oldcontainer').remove();
    if (cacheEnabled) {
      if (cachedBordering == false) cacheBordering();
      if (cachedAboveBelow == false) cacheAboveBelow();
    }
    if (highResLoaded == false) loadHighresTileImages();
  }  
}

$( document ).ready(function() {
  connectToServer();
  $(function() {
    $(this).bind("contextmenu", function(e) {
        e.preventDefault();
    });
  }); 
  if (!!window.chrome == true) {
    hideWarning();
  }
});

