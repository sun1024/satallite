$(document).ready(function () {
    var socket = io.connect();

    socket.on('connect', function () {
        // socket.emit('table_event', { data: 'table' });
        socket.emit('client_event', { data: 'client' });
    })

    // socket.on('table_response', function (msg){
    // 	console.log(msg);
    // })

    var tmp = '';
    var table = [];
    socket.on('server_response', function (msg) {
        // console.log(msg);
        if (msg.data.length != 0 && tmp != msg.data[0]) {
            change_tmp(msg.data)

            // $('#log').append('<br>' + $('<div/>').text('Received #' + ': ' + msg.data).html());
            // $('#log').prepend('<br>' + $('<div/>').text('\n' + time +' #' + ': ' + tmp).html());

            obj = JSON.parse(msg.data[0])
            // console.log(obj)

            var simple1 = document.getElementById('simple1');
            var simpleResult1 = document.getElementById('simpleResult1');
            var simple2 = document.getElementById('simple2');
            var simpleResult2 = document.getElementById('simpleResult2');

            time = fnDate();

            if (obj.Options) { //收到用户信息
                var user = obj.PIDu.substring(0, 5) + "****";
                simple1.innerHTML = "<h3>" + time + "</h3><br>接收到用户:<h3>" + user + "</h3>发起的身份认证请求\n";
                simpleResult1.innerHTML = "<br><br>即将进行转发处理 </h6>";

                $('#log').prepend('<br>' + $('<div/>').text('\n# ' + time + ' ---------- 接收到用户请求：\n' + tmp).html());

                // setTable(user);
                // console.log(table);
                var status = '请求卫星';
                // console.log(user + time + status)
                toTable = '<tr><td>' + user + '</td><td>' + time + '</td><td>' + status + '</td></tr>';
                $('#table tbody').prepend(toTable);
                showTable();
                $('#user_icon').style.setProperty('display', 'inline');
                user2sata();
                // 接入用户总数加一
                updateUserCount(obj.conn_user, obj.succ_user);
            }
            else if (obj.userData) { //转发用户信息到ncc
                var user = obj.userData.PIDu.substring(0, 5) + "****";
                simple2.innerHTML = "<h3>" + time + "</h3><br>正在转发用户:<h3>" + user + "</h3>发起的身份认证请求\n";
                simpleResult2.innerHTML = "<br><br>正在进行转发处理 </h6>";

                $('#log').prepend('<br>' + $('<div/>').text('\n# ' + time + ' ---------- 转发用户请求到NCC：\n' + tmp).html());

                var status = '转发NCC';
                // 获取table中的该user行，并将status修改
                changeTable(user, status);
                sata2ncc();

            }

            else if (obj.ReqAuth == "200") { //ncc回复卫星，用户认证成功
                var user = obj.PIDu.substring(0, 5) + "****";
                // simple.innerHTML = "正在向NCC请求用户\n" + obj.PIDu + "<br>的身份信息\n";
                simple1.innerHTML = "<h3>" + time + "</h3><br>用户:<h3>" + user + "</h3><font color='#FF0000'>认证成功</font><br><br>正在向用户返回成功认证消息";
                simpleResult1.innerHTML = "<br></h6>";

                $('#log').prepend('<br>' + $('<div/>').text('\n# ' + time + ' ---------- 用户认证成功：\n' + tmp).html());

                var status = '认证成功';
                // 获取table中的该user行，并将status修改
                changeTable(user, status);
                ncc2sata();

                updateUserCountAndratio(obj.conn_user, obj.succ_user);
            }

            else if (obj.ReqAuth == "ReqUserInfo") { //向ncc请求用户身份
                var user = obj.PIDu.substring(0, 5) + "****";
                simple2.innerHTML = "<h3>" + time + "</h3><br>正在向NCC请求用户:<h3>" + user + "</h3>的身份信息\n";
                simpleResult2.innerHTML = "<br></h6>";

                $('#log').prepend('<br>' + $('<div/>').text('\n# ' + time + ' ---------- 向NCC请求用户信息：\n' + tmp).html());

                var status = '请求用户';
                // 获取table中的该user行，并将status修改
                changeTable(user, status);
                sata2user();
            }

            //错误处理
            else if (obj.ReqAuth == "500") { //用户认证失败
                var user = obj.PIDu.substring(0, 5) + "****";
                simple1.innerHTML = "<h3>" + time + "</h3><br>用户:<h3>" + user + "</h3><font color='#FF0000'>认证失败</font>";
                simpleResult1.innerHTML = "</h6>";

                $('#log').prepend('<br>' + $('<div/>').text('\n # ' + time + ' ---------- 用户认证失败：\n' + tmp).html());

                var status = '认证失败';
                // 获取table中的该user行，并将status修改
                changeTable(user, status);

                updateUserCountAndratio(obj.conn_user, obj.succ_user);
            }

            // 用户发起图片请求
            else if (obj.ReqAuth == 'reqImg') {
                var user = obj.IDu.substring(0, 5) + "****";
                simple1.innerHTML = "<h3>" + time + "</h3><br>用户:<h3>" + user + "</h3><font color='#FF0000'>发起图片请求</font>";
                simpleResult1.innerHTML = "</h6>";

                $('#log').prepend('<br>' + $('<div/>').text('\n # ' + time + ' ---------- 用户发起图片请求：\n' + tmp).html());
            }
            // 用户请求图片成功
            else if (obj.ReqAuth == 'rspImg') {
                var user = obj.IDu.substring(0, 5) + "****";
                simple1.innerHTML = "<h3>" + time + "</h3><br>用户:<h3>" + user + "</h3><font color='#FF0000'>请求图片成功</font>";
                simpleResult1.innerHTML = "</h6>";
                simpleResult1.innerHTML += '<img src="static/img/sate.png" alt="satallite" width="145" height="145">';

                $('#log').prepend('<br>' + $('<div/>').text('\n # ' + time + ' ---------- 用户请求图片成功：\n' + tmp).html());
            }
            // 用户请求图片失败
            else if (obj.ReqAuth == 'imgError') {
                var user = obj.IDu.substring(0, 5) + "****";
                simple1.innerHTML = "<h3>" + time + "</h3><br>用户:<h3>" + user + "</h3><font color='#FF0000'>请求图片失败</font>";
                simpleResult1.innerHTML = "</h6>";
                simpleResult1.innerHTML += '<img src="static/img/sate.png" alt="satallite" width="145" height="145">';

                $('#log').prepend('<br>' + $('<div/>').text('\n # ' + time + ' ---------- 用户请求图片失败：\n' + tmp).html());
            }
            // 用户请求二次认证
            else if (obj.ReqAuth == 'second') {
                var user = obj.IDu.substring(0, 5) + "****";
                simple1.innerHTML = "<h3>" + time + "</h3><br>用户:<h3>" + user + "</h3><font color='#FF0000'>发起二次认证请求</font>";
                simpleResult1.innerHTML = "</h6>";

                $('#log').prepend('<br>' + $('<div/>').text('\n # ' + time + ' ---------- 用户请求二次认证：\n' + tmp).html());
            }
            // 返回二次认证成功
            else if (obj.ResAuth == 'rspSecondAuth') {
                var user = obj.IDu.substring(0, 5) + "****";
                simple1.innerHTML = "<h3>" + time + "</h3><br>用户:<h3>" + user + "</h3><font color='#FF0000'>二次认证成功</font>";
                simpleResult1.innerHTML = "</h6>";

                $('#log').prepend('<br>' + $('<div/>').text('\n # ' + time + ' ---------- 用户二次认证成功：\n' + tmp).html());
            }
            // 返回二次认证失败
            else if (obj.RepAuth == '500') {
                simple1.innerHTML = "<h3>" + time + "</h3><br>当前用户:<h3>" + "</h3><font color='#FF0000'>二次认证失败</font>";
                simpleResult1.innerHTML = "</h6>";
                simpleResult1.innerHTML += '<img src="static/img/sate.png" alt="satallite" width="145" height="145">';

                $('#log').prepend('<br>' + $('<div/>').text('\n # ' + time + ' ---------- 用户二次认证失败：\n' + tmp).html());
            }
        }
    });
    function fnDate() {
        var date = new Date();
        var year = date.getFullYear();
        var month = date.getMonth();
        var data = date.getDate();
        var hours = date.getHours();
        var minute = date.getMinutes();
        var second = date.getSeconds();
        var time = year + "-" + fnW((month + 1)) + "-" + fnW(data) + " " + fnW(hours) + ":" + fnW(minute) + ":" + fnW(second);
        return time;
    }
    function fnW(str) {
        var num;
        str > 10 ? num = str : num = "0" + str;
        return num;
    }
    // 改变全局变量tmp的值
    function change_tmp(data) {
        $.ajax({
            async: false,
            success: function () {
                tmp = data;
            }
        })
    }
    function setTable(data) {
        $.ajax({
            async: false,
            success: function () {
                table.push(data)
            }
        })
    }

    function changeTable(user, status) {
        // var v = "";
        var key = 0;
        $("#table tr td:nth-child(1)").each(function () {
            // console.log($(this).text());
            if (user == $(this).text()) {
                v = $("#table tr:gt(0):eq(" + key + ") td:eq(2)").text();
                // console.log(v);
                // 改变status
                $("#table tr:gt(0):eq(" + key + ") td:eq(2)").text(status);
            }
            key += 1;
        });
    }

});

// 只显示7行
function showTable() {
    // 获取总行数
    rows = $("#table").find("tr").length
    if (rows > 7) {
        //如果规定显示行号，请用下面代码
        var showNumber = new Array(1, 2, 3, 4, 5, 6, 7);

        $("#table tr").hide();
        for (i = 0; i < showNumber.length; i++) {
            $("#table tr:eq(" + showNumber[i] + ")").show();
        }
    }
}

//接入用户总数更新
function updateUserCount(conn_user, succ_user) {
    document.getElementById("userCount").innerHTML = Number(conn_user);
}

// 计算接入成功率
function updateUserCountAndratio(conn_user, succ_user) {
    document.getElementById("userCount").innerHTML = Number(conn_user);
    userCount = Number(conn_user);
    successCount = Number(succ_user);
    // 判断userCount
    if(userCount!=0){
        succ_ratio = Math.round(successCount / userCount * 100) + "%";
        document.getElementById("succ_ratio").innerHTML = succ_ratio;
    }
}

// 画线
// 控制line的路径展示
var line1 = document.getElementById("line1");
var line2 = document.getElementById("line2");
var line3 = document.getElementById("line3");
var line4 = document.getElementById("line4");
line1.parentNode.removeChild(line1);
line2.parentNode.removeChild(line2);
line3.parentNode.removeChild(line3);
line4.parentNode.removeChild(line4);
// runLine();


function lineRun() {
    // 触发线条运动
    var svg = document.getElementById("svg_1");
    svg.appendChild(line1);
    setTimeout(function () {
        line1.parentNode.appendChild(line3);
        setTimeout(function () {
            line1.parentNode.removeChild(line1);
            line3.parentNode.appendChild(line4);
            line3.parentNode.removeChild(line3);
            setTimeout(function () {
                line4.parentNode.append(line2);
                setTimeout(function () {
                    line4.parentNode.removeChild(line4);
                    line2.parentNode.removeChild(line2);
                }, 4000)
            }, 4000)
        }, 4000);
    }, 4000);
}
// lineRun();

// user to sata
function user2sata() {
    var svg = document.getElementById("svg_1");
    svg.appendChild(line1);
}
// user2sata();

// sata to ncc
function sata2ncc() {
    var svg = document.getElementById("svg_1");
    svg.appendChild(line3);
}

// sata2ncc();

// ncc to sata
function ncc2sata() {
    var svg = document.getElementById("svg_1");
    svg.appendChild(line3);
    svg.appendChild(line2);
    line1.parentNode.removeChild(line1);
    line3.parentNode.appendChild(line4);
    line3.parentNode.removeChild(line3);
}
// sata to user
function sata2user() {
    var svg = document.getElementById("svg_1");
    svg.appendChild(line2);
}

// setTimeout(function () {
//     user2sata();
//     ncc2sata();
//     sata2user();
//     }, 4500)