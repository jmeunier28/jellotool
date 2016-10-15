//Import Dependencies

var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var fs = require('fs');
var PythonShell = require('python-shell');
var multer  =   require('multer');
var process = require('process');
var jsonfile = require('jsonfile');
var util = require('util');

// Define middleware for file uploads
var storage =   multer.diskStorage({
  destination: function (req, file, callback) {
    callback(null, './');
  },
  filename: function (req, file, callback) {
    callback(null, file.fieldname = "Original.UCF.json");
  }
});

var upload = multer({ storage : storage}).single('json');


// var socket = io();

// Listen on port 3000 

http.listen(3000, function() {
  console.log('Listening on port 3000');

});


// Look in the Public directory for all static assets
app.use('/', express.static(__dirname + '/Public'));

// Defines routes
app.get('/', function(req, res) {
  res.sendfile('index.html');
});

// Route for file Post request
app.post('/api',function(req,res){
    upload(req,res,function(err) {
        if(err) {
            return res.end("Error uploading file.");
        }
        res.end("File is uploaded as Original.UCF.json. Plese go back to continue");
    });
});


// Estabilish web socket connection 

io.on('connection', function(socket){
  console.log('A client connected');

  socket.on('vhdl',function(vhdl){
    
    fs.writeFile("vhdl.v", vhdl, function(err) {
    if(err) {
        return console.log(err);
    }

    console.log("The file was saved!");
}); 

    console.log('User VHDL file has been saved on disk');
    //console.log(vhdl);
  });

  socket.on('cello',function(cello){
        
    console.log(cello);
    var pyshell = new PythonShell('automateAPI.py');
        
    pyshell.on('message', function (message) {
    // received a message sent from the Python script (a simple "print" statement) 
    console.log(message);
    //var update = message;
    socket.emit('update', message);

    // end the input stream and allow the process to exit 
    pyshell.end(function (err) {
    
    if (err) throw err;
        console.log('finished');
      });
    });  
  });
});

