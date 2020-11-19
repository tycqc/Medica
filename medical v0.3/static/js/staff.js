// $(function() {
    function changbackgroundcolor() {
        var trs = document.getElementById("staff_table").getElementsByTagName("tr");
        for (var i = 0; i < trs.length; i++) {
            if (i % 2 == 0) {
                trs[i].style.backgroundColor = "#f9f9f9";
            } else {
                trs[i].style.backgroundColor = "#f7f7f7";
            }
        }
    }
// })
