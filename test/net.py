

var http = require("http");
var fs = require('fs');
var iconv = require('iconv-lite');
var BufferHelper = require('bufferhelper');
var config = require("./read-ini.js").load("config.ini");
var wwwroot = config["server"]["wwwroot"]; 
Date.prototype.Format = function (fmt) { //author: meizz 
    var o = {
        "M+": this.getMonth() + 1, //月份 
        "d+": this.getDate(), //日 
        "h+": this.getHours(), //小时 
        "m+": this.getMinutes(), //分 
        "s+": this.getSeconds(), //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}
var time = function(data){
    return typeof data == "undefined" ? new Date().getTime() : new Date(data).getTime();
}
var get = function(url,callback){
    var req = http.get(url,function(res) {
        var bufferHelper = new BufferHelper();
        //var content = "";
        res.on('data', function(data) {
                bufferHelper.concat(data);
        });

        res.on('timeout',function(){
            console.log("timeout");
        });

        res.on("end",function(){
            clearTimeout(request_timer);
            //console.log(iconv.decode(bufferHelper.toBuffer(),'GBK'));
            callback(bufferHelper);
        });

    }).on('error', function(e) {
        console.log("error");
    });

    var request_timer = setTimeout(function() {
        req.abort();
    }, 5000);

    req.on("abort", function() {
        console.log("abort");
    });
}
var lotteryendtime = {};
var dpc = {
    sd:{
        cn:"福彩3D",
        url:{
            endtime:"http://m.cp.360.cn/int/sdindex",
            xml:"http://www.500.com/static/info/kaijiang/xml/sd/index.xml"
        },
        open:"20:30"
    },
    ssq:{
        cn:"双色球",
        url:{
            endtime:"http://m.cp.360.cn/int/ssqindex",
            xml:"http://www.500.com/static/info/kaijiang/xml/ssq/index.xml"
        },
        open:"21:20",
        bonus:[1,2]
    },
    qlc:{
        cn:"七乐彩",
        url:{
            endtime:"http://m.cp.360.cn/int/qlcindex",
            xml:"http://www.500.com/static/info/kaijiang/xml/qlc/index.xml"
        },
        open:"21:20",
        bonus:[1,2,3]
    },
    swxw:{
        cn:"15选5",
        url:{
            endtime:"http://m.cp.360.cn/int/xwindex",
            xml:"http://www.500.com/static/info/kaijiang/xml/swxw/index.xml"
        },
        open:"19:10",
        bonus:[1]
    },
    dlt:{
        cn:"大乐透",
        url:{
            endtime:"http://m.cp.360.cn/int/sltindex",
            xml:"http://www.500.com/static/info/kaijiang/xml/dlt/index.xml"
        },
        open:"20:30",
        bonus:[1,2,3]
    },
    pls:{
        cn:"排列三",
        url:{
            endtime:"http://m.cp.360.cn/int/p3index",
            xml:"http://www.500.com/static/info/kaijiang/xml/pls/index.xml"
        },
        open:"20:30"
    },
    plw:{
        cn:"排列五",
        url:{
            endtime:"http://m.cp.360.cn/int/p5index",
            xml:"http://www.500.com/static/info/kaijiang/xml/plw/index.xml"
        },
        open:"20:30"
    },
    qxc:{
        cn:"七星彩",
        url:{
            endtime:"http://m.cp.360.cn/int/qxcindex",
            xml:"http://www.500.com/static/info/kaijiang/xml/qxc/index.xml"
        },
        open:"20:30",
        bonus:[1,2]
    },
    sfc:{
        cn:"胜负彩",
        url:{
            endtime:"http://trade.500.com/sfc/",
            xml:"http://www.500.com/static/info/kaijiang/xml/sfc/index.xml"
        },
        RegE:/<MatchTeam HomeTeamName="(.+?)" GuestTeamName="(.+?)" MatchScore=".+?" Result=".+?" MatchTime="(.+?)" AverageOdds="(.+?)" OrderNum=".+?" FixtureID=".+?" HomeTeamID=".+?" GuestTeamID=".+?" stageid=".+?" seasonid=".+?" stagemode=".+?" homestanding=".+?" gueststanding=".+?" SimpleGBName="(.+?)" BackColor=".+?" HomeMoneyLine=".+?" AwayMoneyLine=".+?" HandicapLineName=".*?" winkl=".+?" drawkl=".+?" lostkl=".+?" win=".+?" draw=".+?" lost=".+?" \/>/g,
        key:["host","guest","gametime","AverageOdds","SimpleGBName"],
        open:"20:30",
        bonus:[1,2]
    },
    zc6:{
        cn:"6场半全场",
        url:{
            endtime:"http://trade.500.com/zc6/",
            xml:"http://www.500.com/static/info/kaijiang/xml/zc6/index.xml"
        },
        RegE:/<MatchTeam HomeTeamName="(.+?)" GuestTeamName="(.+?)" MatchTime="(.+?)" HalfResult=".+?" Result=".+?" PLStrFor3="(.+?)" BPLStrFor3="(.*?)" HalfMatchScore=".+?" MatchScore=".+?" MatchInfoID=".+?" OrderNum=".+?" FixtureID=".+?" \/>/g,
        key:["host","guest","gametime","PLStrFor3","BPLStrFor3"],
        open:"20:30",
        bonus:[1]
    },
    jq4:{
        cn:"4场进球",
        url:{
            endtime:"http://trade.500.com/jq4/",
            xml:"http://www.500.com/static/info/kaijiang/xml/jq4/index.xml"
        },
        RegE:/<MatchTeam TeamName="(.+?)" MatchScore=".+?" Result=".+?" MatchTime="(.+?)" AverageOdds="(.+?)" OrderNum=".+?" FixtureID=".+?" \/>/g,
        key:["host","gametime","AverageOdds"],
        open:"20:30",
        bonus:[1]
    }
}
var ftb = ["sfc","zc6","jq4"];

var overtime = function(lottery, callback){
    var lottery = lottery.toLowerCase();
    ftb.indexOf(lottery)>=0 ? football(lottery, callback) : szc(lottery, callback);
}
var szc = function(lottery, callback) {
    var lottery = lottery.toLowerCase();
    lotteryendtime[lottery] = {issue:0,endtime:0,nextTime:5000};
    get(dpc[lottery].url.endtime,function(data){
        var data = JSON.parse(data).info.issues[0];
        issue = data[0];
        lotteryendtime[lottery] = {issue:data[0].substr(-5),endtime:data[1]};
        var tc = time(lotteryendtime[lottery].endtime)-time();
        var overnextTime = tc+30*60000>10*60000 ? tc : 10*60000;
        lotteryendtime[lottery].nextTime = nextTime(lottery)-time();
        //console.log("["+lottery+"] 下次采集时间间隔"+lotteryendtime[lottery].nextTime);
        //xml(lottery);
        if(typeof callback !== "undefined") callback(lotteryendtime[lottery]);
    });
}
var nextTime = function(t){
    var startTime = [
        new Date(new Date(lotteryendtime[t].endtime).Format("yyyy-MM-dd 00:00:00")).getTime()
    ];
    var timeOne = dpc[t].open.split(":");
    var b = timeOne[0]*60*60*1000 + timeOne[1]*60*1000;
    return new Date(startTime[0]).getTime()+b;
}
var xml = function(lottery,callback){
    var lottery = lottery.toLowerCase();
    var kaijiang = {
        index:wwwroot+"/kaijiang/xml/"+lottery+"/index.xml",
        history:wwwroot+"/kaijiang/xml/"+lottery+"/history"
    }
    if(lottery == "swxw"){
        dpc.swxw.url.xml = "http://www.500.com/static/info/kaijiang/xml/hdswxw/"+lotteryendtime.swxw.issue.toString().substr(-5)+"/index.xml";
    }
    get(dpc[lottery].url.xml,function(data){
        try{
			var data = data.toString();
            data = data.replace(/.+[\u4e00-\u9fa5].+/g,"");
            var body = data.match(/<xml>([.|\s\S]*)<\/xml>/);
            var issue = xmlWord(data,"PeriodicalNO");
            var xmlstr = '<?xml version="1.0" encoding="GBK"?>\n<xml>\n<open>'+body[1]+'</open>\n</xml>';
            var buf = iconv.encode(xmlstr,'utf8');
            xmlstr = iconv.decode(buf,'gbk');
            fs.exists(kaijiang.history,function(exists){
                if(!exists) fs.mkdirSync(kaijiang.history);//同步创建history文件夹
                fs.exists(kaijiang.history+"/"+issue+".xml",function(exists){
                    if(!exists){
                        fs.writeFileSync(kaijiang.history+"/"+issue+".xml",xmlstr);
                        fs.writeFileSync(kaijiang.index,xmlstr);
                        console.log("["+lottery+"] XML文件生成更新成功");
                        var boun = [];
                        if(typeof dpc[lottery].bonus != "undefined") for(i=1;i<=dpc[lottery].bonus.length;i++) boun.push(xmlWord(data,"Money"+i).replace(/,/g,''));
                        callback(boun,issue);                        
                    }
                });
                //奖金，彩种，N等奖
            });
        }catch(e){
            console.log(e);
        }
    });
}
var xmlWord = function(xml,word){
    var re = new RegExp("<"+word+">(.+?)</"+word+">");
    return xml.match(re)[1];
}
var football = function(lottery, callback) {
    var lottery = lottery.toLowerCase();
    get(dpc[lottery].url.endtime,function(data){
        // var b = iconv.encode(data,'utf8');
        data = iconv.decode(data.toBuffer(),'gbk');
        var issue = data.match(/当前期(\d{5})期/)[1];
        var endtime = time("2016-"+data.match(/截止时间： .*(\d{2}-\d{2} \d{2}:\d{2})/)[1]+":00");
        //console.log({endtime:endtime,issue:issue});
        callback({nextTime:endtime-time(),endtime:endtime,issue:issue});
    });
}
var fbxml = function(lottery,callback) {
    var lottery = lottery.toLowerCase();
    var kaijiang = {
        index:wwwroot+"/kaijiang/xml/"+lottery+"/index.xml",
        history:wwwroot+"/kaijiang/xml/"+lottery+"/history"
    }
    get(dpc[lottery].url.xml,function(data){
        try{

            var data = data.toString();
            var body = data.match(/<xml>([.|\s\S]*)<\/xml>/);
            var issue = xmlWord(data,"PeriodicalNO");
            var code = xmlWord(data,"Result").split(",");

            var IsOutMoney = xmlWord(data,"IsOutMoney");
            var xmlstr = '<?xml version="1.0" encoding="GBK"?>\n<xml>\n<open>'+body[1]+'</open>\n</xml>';

            fs.exists(kaijiang.history,function(exists){
                if(!exists) fs.mkdirSync(kaijiang.history);//同步创建history文件夹
                xmlstr = xmlstr.replace(xmlstr.match(/<MatchTeams>([.|\s\S]*)<\/MatchTeams>/)[0],"");
                //console.log(xmlstr);
                fs.writeFileSync(kaijiang.index,xmlstr);
                console.log("["+lottery+"] XML文件生成更新成功");
                if(IsOutMoney=="1"){
                    fs.exists(kaijiang.history+"/"+issue+".xml",function(exists){
                        if(!exists){
                            fs.writeFileSync(kaijiang.history+"/"+issue+".xml",xmlstr);
                            var boun = [];
                            if(typeof dpc[lottery].bonus != "undefined")
                                for(i=1;i<=dpc[lottery].bonus.length;i++){
                                    boun.push(xmlWord(data,"Money"+i).replace(/,/g,''));
                                   // query("UPDATE KR_Lottery_Win SET win_money="+money+" WHERE Lottery_Name='"+dpc[lottery].cn+"' AND win_level="+i+"");
                                }
                            if(lottery == 'sfc') boun.push(xmlWord(data,"NineMoney").replace(/,/g,''));
                                //query("UPDATE KR_Lottery_Win SET win_money="++" WHERE Lottery_Name='任选九场' AND win_level="+i+"");
                            //console.log("1");
                            callback(1,code,issue,boun);
                        }
                    });
                }else{
                    callback(0,code,issue);
                }
            });
        }catch(e){
            console.log(e);
        }
    });
}
var fblist = function(lottery,issue,callback){
    var lottery = lottery.toLowerCase();
    get("http://www.500.com/static/info/kaijiang/xml/"+lottery+"/"+(1+Number(issue))+".xml",function(data){
        console.log("http://www.500.com/static/info/kaijiang/xml/"+lottery+"/"+(1+Number(issue))+".xml");
        var data = data.toString();
        var key = dpc[lottery].key;
        var ree = [];
        while(tee = dpc[lottery].RegE.exec(data)){
            var ret = {};
            delete tee.input,tee.index,tee[0];
            delete tee.index;
            tee.splice(0, 1);
            for(var i=0;i<key.length;i++) ret[key[i]] = tee[i].replace(/&amp;/g,'&');
            ree.push(ret);
        }
        callback(ree);
    });
}
var o = {
    wwwroot:"D:\vipcai\caipiao", //网站目录物理路径
    overtime:overtime,
    xml:xml,
    dpc:dpc,
    fbxml:fbxml,
    fblist:fblist
}

exports.dpc = o;