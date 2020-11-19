function changbackgroundcolor() {
    var trs = document.getElementById("staff_table").getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        if (i % 2 == 0) {
            trs[i].style.backgroundColor = "#FFFFFF";
        }
        else {
            trs[i].style.backgroundColor = "#000000";
        }
    }
}
