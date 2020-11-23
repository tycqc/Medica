function changbackgroundcolor() {
  var trs = document
    .getElementById("medicine_table")
    .getElementsByTagName("tr");
  for (var i = 0; i < trs.length; i++) {
    if (i % 2 == 0) {
      trs[i].style.backgroundColor = "#f8f8f8";
    } else {
      trs[i].style.backgroundColor = "";
    }
  }
}

function del_medicine(id) {
  layer.open({
        title: ['确认删除'],
        content: '<div style="color:#767676">您确认删除该药品？</div>',
        btn: ['立即删除', '取消'],
        shadeClose: true,
        //回调函数
        yes: function (index, layero) {
            self.location = '../del_medicine/?id='+id;//立即投资按钮
        },
        // btn2: function (index, layero) {
        //     self.location = 'http://www.163.com';//取消按钮
        // },
        // cancel: function (index, layero) { //按右上角“X”按钮
        //     self.location = 'http://www.qq.com';
        // },
    });
}
