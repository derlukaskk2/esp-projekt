const express = require('express')
const request = require('request');

app = express();
const PORT = 3000;

app.get('/home', function(req, res) {
    request('http://esp.7chatban.de:5000/api/data', function (error, response, body) {
        console.error('error:', error); // Print the error
        console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
        console.log('body:', body); // Print the data received
        res.send(body); //Display the response on the website
      });      
});

app.listen(PORT, function (){ 
    console.log('Listening on Port 3000');
});  
