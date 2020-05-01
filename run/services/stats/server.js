const os = require('os-utils');
const fs = require('fs');
const express        = require('express');
const MongoClient    = require('mongodb').MongoClient;
const bodyParser     = require('body-parser');
const app            = express();

const tmpFile = "./cpu.txt";

function getCPU() {
    os.cpuUsage(function(v){
        // console.log( v*100 );

        let CPU = v*100+"\n";

        fs.appendFile(tmpFile, CPU, function(err) {
            if(err) {
                return console.log(err);
            }
        }); 
    });
}

let collector = null;

const port = 8000;
app.listen(port, () => {
  console.log('We are live on ' + port);
});

app.get('/start', (req, res) => {
    if (fs.existsSync(tmpFile)) {
        fs.unlinkSync(tmpFile);
    }
    collector = setInterval(getCPU, 1000);
    res.send('Started')
});

app.get('/stop', (req, res) => {
    // console.log(collector)
    if (collector._repeat)
    {
        clearInterval(collector);
        collector = null;
    }
    res.send('Stopped')
});

app.get('/data', (req, res) => {
    fs.readFile(tmpFile, 'utf8', function(err, data) {
        return console.log(err);
        res.writeHead(200, {'Content-Type': 'application/force-download','Content-disposition':'attachment; filename=cpu.txt'});
        res.end( data );
      });

    if (fs.existsSync(tmpFile)) {
        fs.unlinkSync(tmpFile);
    }
});
