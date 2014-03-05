require('./template/entry');

var controller = new Leap.Controller();
var direction = 0;
controller.on("frame", function(frame) {
  direction = 0;
  if (frame.hands.length == 1 ) {
  	// console.log(frame.hands[0].direction[0]);
  	if (frame.hands[0].direction[0] > 0) {
  		direction = 2;
  	} else {
  		direction = 1;
  	}


	  	serialPort.write(direction + "\n", function(err, results) {
	    	// console.log('err ' + err);
	    	// console.log(results);
	    });
  }
});








controller.on('ready', function() {
    console.log("ready");
});
controller.on('connect', function() {
    console.log("connect");
});
controller.on('disconnect', function() {
    console.log("disconnect");
});
controller.on('focus', function() {
    console.log("focus");
});
controller.on('blur', function() {
    console.log("blur");
});
controller.on('deviceConnected', function() {
    console.log("deviceConnected");
});
controller.on('deviceDisconnected', function() {
    console.log("deviceDisconnected");
});

controller.connect();
console.log("\nWaiting for device to connect...");


// Arduino

var SerialPort = require("serialport").SerialPort
var serialPort = new SerialPort("/dev/tty.usbmodem1421", {
  baudrate: 9600
});

// serialPort.on("open", function () {
//   console.log('open');
//   serialPort.on('data', function(data) {
//     process.stdout.write(data);
//   });
// });

// serialPort.on('error', function(error){});
