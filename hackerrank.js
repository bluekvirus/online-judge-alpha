var page = require('webpage').create();
var system = require('system');
var env = system.env;

page.onConsoleMessage = function(msg) {
    //console.log('remote> ' + msg);
};

var hrank;
var token;

page.onResourceReceived = function(response) {
	var match = response.url.match(/www.hackerrank.com\/$/);
	
	if(match){
	   response.headers.forEach(function(header){
			if(header.name === 'Set-Cookie') {
				var h = header.value, target = "_hrank_session=";
				var idx = h.indexOf(target) + target.length;
				var val = h.slice(idx);
				var idxstop = val.indexOf(";");
				//console.log("***************session id******************");
				hrank = val.slice(0, idxstop);
				//console.log("***************session id******************");
			}
       });
   }
};

page.settings.userAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0';

page.open('https://www.hackerrank.com/', function(status){
	//console.log(status);
});


setTimeout(function(){

	page.open('https://www.hackerrank.com/login', function(status){
		//console.log(status);
			//console.log(page.title);
		if(status != 'success'){
			console.log('Unable to access network');
		} else{

			token = page.evaluate(function(username, pwd){
				document.querySelector('input#login').value = username;
				document.querySelectorAll('input#password')[1].value = pwd;
				document.getElementsByClassName('login-button')[0].click();
				return document.querySelector("meta[name=csrf-token]").getAttribute("content");
			},env['HRANK_USER'], env['HRANK_PWD']);
		}

	});
}, 4000);

setTimeout(function(){
    page.open('https://www.hackerrank.com/rest/contests/master/challenges/simple-array-sum/submissions', function(status){
        if (status !== "success") {
            console.log('fail2');
        }
       // console.log('finished!', page.plainText);
       	var obj = JSON.parse(page.plainText);
       	if(obj['models'].length > 0){
       		//console.log(hrank);
       		console.log("hrank="+ hrank);
       		console.log("auth-token=" + token);
       	}
        phantom.exit();
    });
}, 10000);
