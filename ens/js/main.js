window.onload= function () {

    chushihua()

    login()

}

function chushihua() {

    $("#content").get(0).style.display=""
    $("#content2_1").get(0).style.display=""
}

function login() {
    $("#commit").click(function () {
        var yonghu=  $("#yonghu").val()
        var mima =$("#password").val()
        console.log(yonghu,mima);
        $.ajax({
            type: 'post',
            url: "http://42.192.116.184:5000/getUser",
            dataType:"JSON",
            data: {"yonghu": yonghu,"mima":mima},
            success: function(data) {
                console.log(data)
                if(String(data[1])==String("5")){
                    window.location.href = "./adminsterRegister.html";
                }else if(String(data[1])==String("4")){
                    window.location.href = "./index.html?code="+String(data[0]);
                }else if(String(data[1])==String("1")){
                    window.location.href = "./adminsterReport.html";
                }else if(String(data[1])==String("2")){
                    window.location.href = "./adminsterExamine.html";
                }else if(String(data[1])==String("3")){
                    window.location.href = "./adminsterDetail.html";
                }else if(String(data[1])==String("0")){
                    window.location.href = "./index.html?code="+String(data[0]);
                }

                window.sessionStorage.setItem('currentuser', yonghu)
                window.sessionStorage.setItem('currentuserid', data)
            },
        });
    })

    $("#clear").click(function () {
        var yonghu=  $("#yonghu").val("");
        var mima =$("#password").val("");
        // var aa = [];
        // aa.shift
    })

    $("#zhuce").click(function () {
        $("#content").get(0).style.display="none"
        $("#content2_1").get(0).style.display="none"
        $("#content2").get(0).style.display=""
        $("#content3_1").get(0).style.display=""

    })

    $("#commits").click(function () {
        $("#content2").get(0).style.display="none"
        $("#content3_1").get(0).style.display="none"
        $("#content").get(0).style.display=""
        $("#content2_1").get(0).style.display=""

    })

    $("#queren").click(function () {
       var id = RndNum(8)
       var userName=  $("#yonghu1").val()
       var passWord =$("#password1").val()
       var select = document.getElementById("leibie");
       var nicheng =$("#nicheng1").val()
       var qq=$("#qq").val()
//       alert(nicheng)
       var userType = select.value;
        $.ajax({
            type: 'post',
            url: "http://42.192.116.184:5000/insertUser",
            dataType:"JSON",
            data: {"id":id,"userName": userName,"passWord":passWord,"userType":userType,"nicheng":nicheng,"qq":qq},
            success: function(data) {
                console.log(data)
                if(data){
                    alert("注册成功，返回登录中")
                    window.location.href = "./main.html?code="+id;
                }
            }
        });
    })
}

function RndNum(n){
    var rnd="";
    for(var i=0;i<n;i++)
        rnd+=Math.floor(Math.random()*10);
    return rnd;
}