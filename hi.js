var http = require('http');

var server = http.createServer(function(req, res) {
res.writeHead(200);
res.end('Hi BCT guys!');
});
server.listen(8089);