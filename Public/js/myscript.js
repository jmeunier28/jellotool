var socket = io();
var json = null;


$(document).ready(function () {


   $('#uploadbutton').click(function() {
    //get file object
    alert('JSON File has been uploaded');
    var file = document.getElementById('file').files[0];
    if (file) {
        // create reader
        var reader = new FileReader();
        reader.readAsText(file);
        reader.onload = function(e) {
            var string = e.target.result ;
            json = JSON.parse(string);
            console.log(typeof(json));
            // browser completed reading file - display it
            //console.log(e.target.result);
              //socket.emit('file', json);

        };
    }
});


      $('#uploadverilog').click(function() {
    //get file object
    alert('Verilog File has been uploaded');
    var file = document.getElementById('vhdl').files[0];
    if (file) {
        // create reader
        var reader = new FileReader();
        reader.readAsText(file);
        reader.onload = function(e) {
            var verilog = e.target.result ;
            console.log(verilog);
            //console.log(typeof(vhdl));
            //console.log(vhdl);
            // browser completed reading file - display it
            //console.log(e.target.result);
            socket.emit('vhdl', verilog);

        };
    }
});

   $('#cello').click(function() {
    console.log('click');
    $('#update').text(' ');
    var cello = "--------------------STARTING PYTHON SHELL---------------------"; 
    socket.emit('cello', cello);
  });
 
});

