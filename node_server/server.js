var http = require('http');  
var url = require('url');  
var fs = require('fs');
const scrape = require('website-scraper');

const hostname = '127.0.0.1';
const port = 3000;

var server = http.createServer(function(request, response) {  
    var path = 'node-homepage/index.html'
    switch (path) {   
        case 'node-homepage/index.html':  
            //fs.readFile(__dirname + path, function(error, data) {  
            fs.readFile(path, function(error, data) {  
                console.log(`Path: ${path}`)
                if (error) {  
                    response.writeHead(404);  
                    response.write(error);  
                    response.end();  
                } else {  
                    response.writeHead(200, {  
                        'Content-Type': 'text/html'
                    });  
                    response.write(data);  
                    response.end();  
                }  
            });  
            break;  
        default:  
            response.writeHead(404);  
            response.write("opps this doesn't exist - 404");  
            response.end();  
            break;  
    }  
});  
server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});