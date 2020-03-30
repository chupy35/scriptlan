// var http = require('http');
// var fs = require('fs');

// var download = function(url, dest, cb) {
//   var file = fs.createWriteStream(dest);
//   var request = http.get(url, function(response) {
//     response.pipe(file);
//     file.on('finish', function() {
//       file.close(cb);  // close() is async, call cb after close completes.
//     });
//   }).on('error', function(err) { // Handle errors
//     fs.unlink(dest); // Delete the file async. (But we don't check the result)
//     if (cb) cb(err.message);
//   });
// };

// ------------------------------------------------------------------------
// const fs = require('fs');
// const request = require('request');

// const download = (url, dest, cb) => {
//     const file = fs.createWriteStream(dest);
//     const sendReq = request.get(url);

//     // verify response code
//     sendReq.on('response', (response) => {
//         if (response.statusCode !== 200) {
//             return cb('Response status was ' + response.statusCode);
//         }

//         sendReq.pipe(file);
//     });

//     // close() is async, call cb after close completes
//     file.on('finish', () => file.close(cb));

//     // check for request errors
//     sendReq.on('error', (err) => {
//         fs.unlink(dest);
//         return cb(err.message);
//     });

//     file.on('error', (err) => { // Handle errors
//         fs.unlink(dest); // Delete the file async. (But we don't check the result)
//         return cb(err.message);
//     });
// };
// ------------------------------------------------------------------------