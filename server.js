/*require('nodetime').profile({
    accountKey: 'f27d07835a8efcc79e9a98c5f9bb5c9fe7e599fa', 
    appName: 'Node.js Application'
  });
*/
var BinaryServer = require('binaryjs').BinaryServer;
var fs = require('fs');
var path = require('path');
var request = require("request")

var DJANGO_URL = 'http://torres.stackstreamer.com';
var APP_ROOT = path.dirname(require.main.filename);
var DATA_ROOT = '/home/eben/torres/torres-research-webviewer/pyramid/breast/pyramid/HnE';
var DATA_ROOT = '/data/breast/pyramid/channel1';
// Start Binary.js server
var server = BinaryServer({port: 9000});

console.log('Server starting up');

// Wait for new user connections
server.on('connection', function(client){
    console.log('Connection');
	client.on('stream', function(stream, meta){
        stream.on('data', function(data) {
            if (data['action']=='open') {
                request({
                    url: DJANGO_URL+'/datapath/'+data['uuid'],
                    json: true
                }, function (error, response, body) {
                    if (!error && response.statusCode === 200) {
                        console.log(body) // Print the json response
                        if (body.result == 'success') {
                            DATA_ROOT=body.path+'/pyramid/channel1';
                            console.log('opening stack: '+DATA_ROOT);
                            fs.readFile(body.path+'/info.json', 'utf8', function(err,data) {
                                console.log('sending info');
                                client.send(data, {'type':'info'});                               
                            });
                        }
                    }
                });
            }
            if (data['action']=='send') {
                var file = fs.createReadStream(DATA_ROOT+data['path']);
                file.on('error', function (error) {
                    file.close();
                    file = fs.createReadStream(APP_ROOT+'/assets/blank.png');
                    client.send(file, {'type':'image', 'src':data['path'], 'target':data['target']});
                });
            	file.on('readable', function() {
                    client.send(file, {'type':'image', 'src':data['path'], 'target':data['target']});
                });
            }
        });
	});
});
