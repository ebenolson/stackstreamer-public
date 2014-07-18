var BinaryServer = require('binaryjs').BinaryServer;
var fs = require('fs');

var DATA_ROOT = '/home/eben/torres/torres-research-webviewer/pyramid/breast/pyramid/HnE'
// Start Binary.js server
var server = BinaryServer({port: 9000});
// Wait for new user connections
server.on('connection', function(client){
  // Stream a flower as a hello!
  var file = fs.createReadStream(DATA_ROOT + '/zoom0/slice_0050/tile_x0003_y0003.png');
  client.send(file); 
});