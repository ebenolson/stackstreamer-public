var BinaryServer = require('binaryjs').BinaryServer;
var fs = require('fs');

var DATA_ROOT = '/home/eben/torres/torres-research-webviewer/pyramid/breast/pyramid/HnE'
var DATA_ROOT = '/data/breast/pyramid/HnE'
// Start Binary.js server
var server = BinaryServer({port: 9000});
// Wait for new user connections
server.on('connection', function(client){
	client.on('stream', function(stream, meta){
//		console.log(meta);
		var file = fs.createReadStream(DATA_ROOT + meta['path']);
		file.pipe(stream);
	})
});