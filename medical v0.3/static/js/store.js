// function sumbit_sure() {
//   var gnl = confirm("确定注销或删除?");
//   if (gnl == true) {
//     return true;
//   } else {
//     return false;
//   }
// }
//   layer.open({
//         title: ['确认注销'],
//         content: '<div style="color:#767676">您确认注销账号？</div>',
//         btn: ['立即删除', '取消'],
//         shadeClose: true,
//         //回调函数
//         yes: function(index){
//           //当点击‘确定’按钮的时候，获取弹出层返回的值
//           var res = window["layui-layer-iframe" + index].callbackdata();
//           //打印返回的值，看是否有我们想返回的值。
//           console.log(res);
//           //最后关闭弹出层
//           layer.close(index);
//           },
//           cancel: function(){
//                 //右上角关闭回调
//               }
//
//     });
// }
// var callbackdata = function () {
//             return true;
//         }