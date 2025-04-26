

var async = require('async');

//通过setTimeout函数实现Sleep的功能
var sleep = function(array, callback) {
  'use strict';

  //初始化变量
  var results = [];  //存放最终结果
  var tmpArray = array.slice(0);  //拷贝一份数据，防止改变变量外部的值
  var isEnd = false;

  //自调用函数
  var run = function() {
    var tmp = null; //存放截取的数组
    if (tmpArray.length > 3) {
      tmp = tmpArray.splice(0, 3);
    } else {
      tmp = tmpArray;
      isEnd = true;
    }
    async.mapLimit(tmp, 2, function(item, itemCallback) {
      console.log('Enter: ' + item.name);
      setTimeout(function() {
        console.log('Handle: ' + item.name);
        itemCallback(false, item.name + '!!!');
      }, item.delay);
    }, function(err, data) {
      console.log(data);
      results = results.concat(data);
      if (isEnd) {
        callback(false, results);
      } else {
        console.log('Sleep 5s');
        setTimeout(run, 5000);
      }
    });
  };

  run();
};


//测试数据
var arr = [
  {name:'mocksleep', delay:3000}
];

// sleep(arr, function(error, data) {
//   'use strict';
//   console.log(data);
// });


//http server

var http = require('http');
var url = require('url');

var counter = 0;

http.createServer(function (req, res) {

  sleep(arr, function(error, data) {

    console.log("-------service external----------");

    var req_url = url.parse(req.url, true);
    var params = req_url.query;
    console.log(params);

    res.writeHead(200,{
      "Content-Type":'application/json',
      'charset':'utf-8',
      'Access-Control-Allow-Origin':'*',
      'Access-Control-Allow-Methods':'PUT,POST,GET,DELETE,OPTIONS'
    });

    if(req_url.pathname.indexOf('greeting_async') > -1){

        console.log("-------greeting_async----------");
        var options = {
            hostname: 'rest-service-1',
            port: '16001',
            path: '/hello1_callback?cal_back=60'
          };
        function handleResponse(response) {
          var serverData = '';
          response.on('data', function (chunk) {
            serverData += chunk;
          });
          response.on('end', function () {
            console.log("Response Status:", response.statusCode);
            console.log("Response Headers:", response.headers);
            console.log(serverData);
          });
        }
        http.request(options, function(response){
          handleResponse(response);
        }).end();
    }else{
        var resObj = {
          id: counter++,
          result: (params.cal < 100 && params.cal > 0)
        };

        // res.writeHead(200,{
        //   "Content-Type":'text/plain',
        //   'charset':'utf-8',
        //   'Access-Control-Allow-Origin':'*',
        //   'Access-Control-Allow-Methods':'PUT,POST,GET,DELETE,OPTIONS'
        // });
        
        res.write(JSON.stringify(resObj));
        
    }

    res.end();
    

  });
  
  
}).listen(16100);










