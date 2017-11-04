//declare required modules
var app = require('http').createServer(handler)
  , io = require('socket.io').listen(app)
  , fs = require('fs')
  , static = require('node-static')
  , util = require('util')
  , colors = require('colors')
 // , piblaster = require('pi-blaster.js')
  //, sleep = require('sleep')
  , argv = require('optimist').argv;
  app.listen(8080);
 

//Make a web server on port 8080
//
var file = new(static.Server)();
function handler(request, response) 
{
  console.log('serving file',request.url)
  file.serve(request, response);
};

// make a zerorc server to output to Python client

var zerorpc = require("zerorpc")

alpha = 1.1;
beta = 2.2;
gamma =3.3;
count = 1;

//global angles for Python Server
GlobalAlpha = 0.1;
GlobalBeta = 0.1;
GlobalGamma = 0.1;
GlobalMatrix = [GlobalAlpha*1, GlobalBeta*1, GlobalGamma*1]



var server = new zerorpc.Server({
    hello: function(name, reply) {
       //reply(null, "Hello, " + name +  " Alpha "+GlobalAlpha + " Beta  " +GlobalBeta +" Gamma " +GlobalGamma +"  " + count);
       reply(null,  GlobalMatrix);
	count++
    }
});

server.bind("tcp://0.0.0.0:4242");

var logcount = 0;



console.log('Pi Car my server listening on port 8080 visit http://ipaddress:8080/socket.html');
lastAction = "";

//If we lose comms set the servos to neutral
function emergencyStop()
{
  	console.log('###EMERGENCY STOP - signal lost or shutting down'.yellow);
}//END emergencyStop


// fire up a web socket server isten to cmds from the phone and set pwm
io.sockets.on('connection', function (socket) 
{ 
	//got phone msg
	socket.on('fromclient', function (data) 
	{
		logcount = logcount + 1;
		GlobalAlpha = data.alpha.toFixed(2);
		GlobalBeta =  data.beta.toFixed(2);
		GlobalGamma = data.gamma.toFixed(2);
		GlobalMatrix = [GlobalAlpha*1, GlobalBeta*1, GlobalGamma*1];

		if(logcount == 10)
		{
			//@ 2 Hz
			logcount = 0;
			console.log("Alpha: "+GlobalAlpha+" Beta: "+GlobalBeta+" Gamma: "+GlobalGamma);
			console.log();
			//console.log("Alpha: "+data.alpha+" Beta: "+tmp_beta+" Gamma: "+tmp_gamma);				
		}
	
		clearInterval(lastAction); //stop emergency stop timer
		lastAction = setInterval(emergencyStop,2000); //set emergency stop timer for 1 second
				
	});
});//END io.sockets.on

//user hits ctrl+c
//
process.on('SIGINT', function() 
{
	emergencyStop();
	console.log("\nGracefully shutting down from SIGINT (Ctrl-C)");
 	console.log("\nShould set demand angles to 0.2");

	GlobalAlpha = 0.2;
	GlobalBeta = 0.2;
	GlobalGamma = 0.2;
 
	 return process.exit();
});//END process.on 
