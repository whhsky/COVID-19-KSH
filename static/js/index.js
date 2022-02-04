var localhost = "http://127.0.0.1:8000/" // API路由地址
var gnyq = echarts.init(document.getElementById('gnmrxz'), 'white', {renderer: 'canvas'}); // 国内疫情
var zgdt = echarts.init(document.getElementById('zgdt'), 'white', {renderer: 'canvas'}); // 中国地图
var yqbt = echarts.init(document.getElementById('yqbt'), 'white', {renderer: 'canvas'}); // 饼图
var gfx = echarts.init(document.getElementById('gfx'), 'white', {renderer: 'canvas'}); // 高风险地区
var zfx = echarts.init(document.getElementById('zfx'), 'white', {renderer: 'canvas'}); // 中风险地区
var bj = echarts.init(document.getElementById('bj'), 'chalk', {renderer: 'canvas'}); // 近期31省区市本土现有病例

var q = document.getElementsByClassName('today')
var gd = document.getElementsByClassName('aa')

var ly = document.getElementById('ly')  //当前时间

var fxp = document.getElementsByClassName('pp')
var fxsl = document.getElementsByClassName('fxsl')

var total = new Array()
var add = new Array()

var ul1 = document.getElementById("aa");
var ul2 = document.getElementById("aa1");
var ulbox = document.getElementById("box1");

var rand = Math.floor(Math.random() * 888);

window.onload = function (){
    getdata();
    getssbb();
}

function roll(t) {
  ul2.innerHTML = ul1.innerHTML;
  ulbox.scrollTop = 0; // 开始无滚动时设为0
  var timer = setInterval(rollStart, t); // 设置定时器，参数t用在这为间隔时间（单位毫秒），参数t越小，滚动速度越快
  // 鼠标移入div时暂停滚动
  ulbox.onmouseover = function() {
  clearInterval(timer);
  }
  // 鼠标移出div后继续滚动
  ulbox.onmouseout = function() {
  timer = setInterval(rollStart, t);
  }
}
// 开始滚动函数
function rollStart() {
// 正常滚动不断给scrollTop的值+1,当滚动高度大于列表内容高度时恢复为0
if(ulbox.scrollTop >= ul1.scrollHeight) {
ulbox.scrollTop = 0;
} else {
ulbox.scrollTop++;
}
}



function getTime() {
var myDate = new Date();
var myYear = myDate.getFullYear(); //获取完整的年份(4位,1970-????)
var myMonth = myDate.getMonth() + 1; //获取当前月份(0-11,0代表1月)
var myToday = myDate.getDate(); //获取当前日(1-31)
var myDay = myDate.getDay(); //获取当前星期X(0-6,0代表星期天)
var myHour = myDate.getHours(); //获取当前小时数(0-23)
var myMinute = myDate.getMinutes(); //获取当前分钟数(0-59)
var mySecond = myDate.getSeconds(); //获取当前秒数(0-59)
var week = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
var nowTime;

nowTime = '北京时间：' + myYear + '年' + fillZero(myMonth) + '月' + fillZero(myToday) + '日' + '  ' + fillZero(myHour) + ':' +
fillZero(myMinute) + ':' + fillZero(mySecond) + '  ' + week[myDay] + '  ';
    $('#bjsj').html(nowTime);
};

function fillZero(str) {
    var realNum;
    if (str < 10) {
        realNum = '0' + str;
    } else {
        realNum = str;
    }
    return realNum;
}
setInterval(getTime, 1000);


var old_data = [];
var bjtimer;

function bjfc() {
    bjtimer = setInterval(function () {
        bj1(bj);
    }, 1500)
}

$(
    function () {
        gryq(gnyq);
        Zgdt(zgdt);
        Yqbt(yqbt);
        bj1(bj);
        gfx1(gfx);
        zfx1(zfx);
        fxdqlb1(fxp);
        gxsj(ly);
        bj1(bj);
    }
);


function getdata(){
    $.ajax({
        type: "GET",
        url: localhost + "app/chinayq/?p=" + rand,
        dataType: "json",
        success: function (result) {
            total.push(result.data.diseaseh5Shelf.chinaTotal.localConfirm);
            total.push(result.data.diseaseh5Shelf.chinaTotal.nowConfirm);
            total.push(result.data.diseaseh5Shelf.chinaTotal.confirm);
            total.push(result.data.diseaseh5Shelf.chinaTotal.noInfect);
            total.push(result.data.diseaseh5Shelf.chinaTotal.importedCase);
            total.push(result.data.diseaseh5Shelf.chinaTotal.dead);

            add.push(result.data.diseaseh5Shelf.chinaAdd.localConfirmH5);
            add.push(result.data.diseaseh5Shelf.chinaAdd.nowConfirm);
            add.push(result.data.diseaseh5Shelf.chinaAdd.confirm);
            add.push(result.data.diseaseh5Shelf.chinaAdd.noInfect);
            add.push(result.data.diseaseh5Shelf.chinaAdd.importedCase);
            add.push(result.data.diseaseh5Shelf.chinaAdd.dead);
            for(var i=0; i<q.length; i++){
                q[i].innerHTML = '<p class="sz">' + q[i].outerText + '</p><p class="sz">' + total[i] + '</p><p class="sz">较昨日+' + add[i] + '</p>';
            }
        }
    });
}

function gryq() {
    $.ajax({
        type: "GET",
        url: localhost + "app/xyqz/",
        dataType: "json",
        success: function (result) {
            var options = result.data;
            gnyq.setOption(options);
            old_data = gnyq.getOption().series[0].data;
        }
    });
}

function Zgdt() {
    $.ajax({
        type: "GET",
        url: localhost + "app/zgdt/?p=" + rand,
        dataType: "json",
        success: function (result) {
            // console.log(result)
            var options = result.data;
            zgdt.setOption(options);
            old_data = zgdt.getOption().series[0].data;
        }
    });
}

function Yqbt() {
    $.ajax({
        type: "GET",
        url: localhost + "app/yqbt/",
        dataType: "json",
        success: function (result) {
            // console.log(result)
            var options = result.data;
            yqbt.setOption(options);
            old_data = yqbt.getOption().series[0].data;
        }
    });
}

function bj1() {
    $.ajax({
        type: "GET",
        url: localhost + "app/bg/",
        dataType: "json",
        success: function (result) {
            // console.log(result)
            var options = result.data;
            bj.setOption(options);
            old_data = bj.getOption().series[0].data;
        }
    });
}

function gfx1() {
    $.ajax({
        type: "GET",
        url: localhost + "app/gfx/?p="+rand,
        dataType: "json",
        success: function (result) {
            var options = result.data;
            gfx.setOption(options);
            old_data = gfx.getOption().series[0].data;
        }
    });
}

function zfx1() {
    $.ajax({
        type: "GET",
        url: localhost + "app/zfx/?p="+rand,
        dataType: "json",
        success: function (result) {
            var options = result.data;
            zfx.setOption(options);
            old_data = zfx.getOption().series[0].data;
        }
    });
}

var str = ''
function getssbb() {
  $.ajax({
      type: "GET",
      url: localhost + "app/ssrd/",
      dataType: "json",
      success: function (result) {
          result = result.data
          for(var j=0; j<result.length; j++){
                str += '<div>最新资讯</div><li>&nbsp<a href="'+ result[j].eventurl +'" target="_blank">'
                    + result[j].eventdescription + '</a></li><div class="timez">'+ result[j].time_ago + '</div>'
              }
		  gd[0].innerHTML = str;
		  roll(50);
      }
  });
}


// 风险地区
function fxdqlb1() {
    $.ajax({
        type: "GET",
        url: localhost + "app/fxdq/?p=" + rand,
        dataType: "json",
        success: function (result) {
            // console.log(result)
            var gaddress = ''
            var zaddress = ''
            for(var i=0; i< result.data.data[0].地区.length; i++){
                gaddress += '<li>' + result.data.data[0].地区[i] + '</li>';
            }
            for(var i=0; i< result.data.data[1].地区.length; i++){
                zaddress += '<li>' + result.data.data[1].地区[i] + '</li>';
            }
            fxsl[0].innerHTML = '高风险(' + result.data.data[0].数量 + ')'
            fxsl[1].innerHTML = '中风险(' + result.data.data[1].数量 + ')'
            fxp[0].innerHTML = gaddress;
            fxp[1].innerHTML = zaddress;

            $('#J_scroll1').width($('#J_scroll1').width() - $('#J_scroll1 li:first-child').innerWidth());
            $('#J_scroll1').addClass('theanimation');

            $('#J_scroll2').width($('#J_scroll2').width() - $('#J_scroll2 li:first-child').innerWidth());
            $('#J_scroll2').addClass('theanimation1');
        }
    });
}

// 更新时间
function gxsj() {
    $.ajax({
      type: "GET",
      url: localhost + "app/chinayq/?p=" + rand,
      dataType: "json",
      success: function (result) {
          ly.innerText = '更新时间：'+ result.data.diseaseh5Shelf.lastUpdateTime
      }
    })
}