/**
 * Created by skype on 2018/8/10.
 */
// 	表单提交
var bool = false;
function toSubmit(){
    var name = $('#reservationName').val();
    var mobile = $('#reservationPhone').val();
    var id = $('#reservationId').val();
// 		$('form').submit(function(){
    if($("#endDate").val()==''){
        showMsg('请选择离店时间！');
        bool = false;
        return bool;
    }else{
        bool = true;
    }
    if(bool){
        var sdate = new Date($("#startDate").val());
        var edate = new Date($("#endDate").val());

    }
// 		});
}

var obj ;
// var id = ${roomId};
// var sdate = new Date();
var sdate = '2018-07-04';
// $.post('../hotel/roomOrder',{id:id},function(data){
//   if(data.code==1000){
//     if(data.result.hotelOrder.leaveTime != undefined){
//       if(data.result.hotelOrder.leaveTime.time > new Date().getTime()){
//         sdate = new Date(data.result.hotelOrder.leaveTime.time);
//       }
//     }
//   }

// 	alert(sdate);
//     $.post('../hotel/reservatTime',{id:id},function(data){
//       obj = data.result;
obj = ['2018-07-12','2018-07-13','2018-07-20'];//禁用日期可以从数据库查
// 	自定义格式
$.fn.datetimepicker.dates['zdy'] = {
    days: ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"],
    daysShort: ["周日", "周一", "周二", "周三", "周四", "周五", "周六"],
    daysMin:  ["日", "一", "二", "三", "四", "五", "六"],
    months: ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"],
    monthsShort: ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"],
    today: "今天",
    format:"yyyy-mm-dd",
    titleFormat:"yyyy-mm-",
    weekStart:1,
    suffix: [],
    meridiem: ["上午", "下午"]
};
$('#startDate').datetimepicker({
    language:  'zdy',
    weekStart: 1,
    todayBtn:  1,
    autoclose: 1,
    startDate:sdate,
    minView:2,
    maxView:3,
    onRenderDay: function(date) {
        // 	    	alert(date);
        var date1 = date.getFullYear()+'-'
            +(date.getMonth()<9?'0'+(date.getMonth()+1):date.getMonth()+1)
            +'-'
            +(date.getDate()<10?'0'+(date.getDate()-1):date.getDate()-1);
        // for(var o in obj){
        //   if(date1==obj[o]){
        //     return ['disabled'];
        //   }
        // }

    }
}).on('changeDate', function(ev){
    // 		alert($("#startDate").val());
    $('#endDate').datetimepicker('remove');
    $('#endDate').val('');
    var sdate=$("#startDate").val();
    var edate;
    for(var o in obj){
        if(new Date(sdate)<=new Date(obj[o])){
            var date = new Date(obj[o])
            var ndate = +date+24*60*60*1000;
            var leaveTime = new Date(ndate);
            edate = leaveTime.getFullYear()+'-'+(leaveTime.getMonth()+1)+'-'+leaveTime.getDate();

            break;
        }
    }
// 			alert(edate);
    $('#endDate').datetimepicker({
        language:  'zdy',
        weekStart: 1,
        todayBtn:  1,
        autoclose: 1,
        startDate:sdate,
        endDate:edate,
        minView:2,
        maxView:3
    }).on('changeDate', function(ev){
        // 		            alert(o+++"~~")
    });
});
// });
// });
$("#endDate").click(function(){
    if($("#startDate").val()!=''){

    }else{
        showMsg('请先选择入住时间！');
    }
});