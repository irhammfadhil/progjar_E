var http = require('http');
const express = require('express');
const app = express();
const path = require('path');
const router = express.Router();
var bodyParser = require('body-parser');
var mariadb = require('mariadb');
var md5 = require('md5');
var session = require('express-session');
var sess;

app.use(bodyParser.urlencoded({extended : true}));

const pool = mariadb.createPool({
     host: '10.151.30.144', 
     user:'root', 
     database: 'pbkk_2',
     port: 3306
});

const pool2 = mariadb.createPool({
	host: '127.0.0.1',
	user: 'root',
	database: 'pbkk_2',
	port: 3306
})
app.use(session({secret: 'ssshhhhh'}));

app.use('/', router);

router.get('/', function(req, res){
	var users = [];
	var passwords = [];
	/*if (req.session.page_views) {
		req.session.page_views++;
		console.log(req.session.page_views);
		res.send("You visited this page " + req.session.page_views + " times");
	}*/
	query = 'select * from users';
	pool2.query(query).then(results => {
		var wkwk = results;
		var i;
		for (i=0;i<results.length;i++) {
			users.push(results[i].username);
			passwords.push(results[i].password);
		}
		console.log(users);
		console.log(passwords);
	});
	console.log(query);
	res.send("Hello World");
	//querying.query('select NOW()');
	//console.log(query.sql);
});
router.get('/login',function(req,res){
	var time1 = [];
	var time2 = [];
	var desc1 = [];
	var desc2 = [];
	var query = 'select * from log';
	console.log(query)
	pool.query(query).then(results => {
		for(var i = 0;i<results.length;i++) {
			time1.push(results[i].time_stamp);
			desc1.push(results[i].description);
		}
		pool2.query(query).then(results => {
			for (var i=0;i<results.length;i++) {
				time2.push(results[i].time_stamp);
				desc2.push(results[i].description);
			}
			/*console.log(time2[1].toString());
			console.log(desc2[1]);
			console.log(time1[1].toString());
			console.log(desc1[1]);
			if (time2[1].toString() == time1[1].toString()) {
				console.log('sama');
			}*/
			for (var i=0;i<time1.length;i++) {
				var flag=0;
				for (var j=0;j<time2.length;j++) {
					console.log('data ke- ' + i + j)
					var test1 = time1[i].toString();
					var test2 = time2[j].toString();
					if (test1 == test2) {
						flag=flag+1;
						console.log('data ke' + i + j + 'sama');
						console.log(time1[i]);
						console.log(desc1[i]);
						console.log('---')
					}
					else {
						console.log('data ke '+ i + j + ' beda');
						console.log(time1[i]);
						console.log(desc1[i]);
						console.log(time2[j]);
						console.log(desc2[j]);
						console.log('---')
					}
					//console.log(flag);
					/*if (flag == 0) {
						var k =new Date(time2[j]).getTime()/1000
						var querying='insert into log values(' + "FROM_UNIXTIME("+ k + ")"+ ',' + "'"+ desc2[j] +  "'"+')';
						console.log(querying);
					}*/
				}
				console.log(flag);
				if (flag == 0) {
					var k =new Date(time1[i]).getTime()/1000;
					console.log(k)
					var querying='insert into log values(' + "FROM_UNIXTIME("+ k + ")"+ ',' + "'"+ desc1[i] +  "'"+')';
					console.log(querying);
					pool2.query(querying);
				}
			}
		});
	});
	//for (var i=0;i<)
  res.sendFile(path.join(__dirname+'/login.html'));
  //__dirname : It will resolve to your project folder.
});

router.post('/login', function(req, res) {
	var mkmk;
	var results;
	//console.log(req.session.username);
	var uname = req.body.username;
	var pass = req.body.password;
	console.log("Mencoba login dengan nama pengguna", uname, "dengan password", pass);
	query = 'select password from users where username=' + "'" + uname + "'"
	console.log(query)
    pool2.query(query)
    .then(results => {
    	mkmk = results[0].password;
    	console.log(mkmk);
    	console.log(md5(pass));
    	if (md5(pass) == mkmk) {
    		console.log('password benar');
    		var querylogin = 'insert into log values(now(),' + "'" + 'login username ' + uname + ' sukses' + "')";
    		pool2.query(querylogin);
    		console.log(querylogin);
    		res.redirect('/berhasillogin')
    	}
    	else {
    		console.log('password salah');
    		res.redirect('/gagallogin')
    	}
    }).catch(err => {
    	console.log(err);
    	res.redirect('/gagallogin');
    })
});

router.get('/berhasillogin',  function(req, res) {
	res.sendFile(path.join(__dirname+'/berhasillogin.html'));
});

router.get('/gagallogin',  function(req, res) {
	res.sendFile(path.join(__dirname+'/gagallogin.html'));
});

router.get('/create_account',function(req,res){
  res.sendFile(path.join(__dirname+'/create_account.html'));
  var un1 = [];
	var un2 = [];
	var pas1 = [];
	var pas2 = [];
	var query = 'select * from users';
	console.log(query)
	pool.query(query).then(results => {
		for(var i = 0;i<results.length;i++) {
			un1.push(results[i].username);
			pas1.push(results[i].password);
		}
		pool2.query(query).then(results => {
			for (var i=0;i<results.length;i++) {
				un2.push(results[i].username);
				pas2.push(results[i].password);
			}
			/*console.log(time2[1].toString());
			console.log(desc2[1]);
			console.log(time1[1].toString());
			console.log(desc1[1]);
			if (time2[1].toString() == time1[1].toString()) {
				console.log('sama');
			}*/
			for (var i=0;i<un1.length;i++) {
				var flag=0;
				for (var j=0;j<un2.length;j++) {
					console.log('data ke- ' + i + j)
					var test1 = un1[i];
					var test2 = un2[j];
					if (test1 == test2) {
						flag=flag+1;
						console.log('data ke' + i + j + 'sama');
						console.log(un1[i]);
						console.log(pas1[i]);
						console.log('---')
					}
					else {
						console.log('data ke '+ i + j + ' beda');
						console.log(un1[i]);
						console.log(pas1[i]);
						console.log(un2[j]);
						console.log(pas2[j]);
						console.log('---')
					}
					//console.log(flag);
					/*if (flag == 0) {
						var k =new Date(time2[j]).getTime()/1000
						var querying='insert into log values(' + "FROM_UNIXTIME("+ k + ")"+ ',' + "'"+ desc2[j] +  "'"+')';
						console.log(querying);
					}*/
				}
				console.log(flag);
				if (flag == 0) {
					//var k =new Date(time1[i]).getTime()/1000;
					//console.log(k)
					var querying='insert into users values(' + "'" +un1[i] + "'" + ',' +"'" + pas1[i] + "'"+ ')';
					console.log(querying);
					pool2.query(querying);
				}
			}
		});
	});
});

router.post('/create_account', function(req, res) {
	var uname = req.body.username;
	var pass = req.body.password;
	var confirm = req.body.password_confirm;
	console.log("Mencoba buat akun dengan nama pengguna", uname, "dengan password", pass, "konfirmasi pass", confirm);
	query = 'insert into users values(' + "'" +uname + "'" + ',' + 'md5(' +"'" + pass + "'"+ '))';
	if (pass != confirm) {
		res.redirect('/gagalbuatakun');
	}
	else {
		console.log(query);
	    pool2.query(query)
	    .then(results => {
	    	res.redirect('/suksesbuatakun');
	    }).catch (err => {
	    	res.redirect('/gagalbuatakun');
	    });
	}

});

router.get('/gagalbuatakun', function(req, res) {
	res.sendFile(path.join(__dirname+'/gagalbuatakun.html'));
});

router.get('/suksesbuatakun', function(req, res){
	res.sendFile(path.join(__dirname+'/berhasilbuatakun.html'));
});
//add the router

app.listen(process.env.port || 3000);

console.log('Running at Port 3000');