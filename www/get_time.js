
// get the system time live //

function startTime() {

    // date //

    var today=new Date();

    // day //

    var d=today.getDate();

    // month //

    var mm=today.getMonth() + 1;

    // year //

    var y=today.getFullYear();

    // hour //

    var h=today.getHours();

    // minute //

    var m=today.getMinutes();

    // second //

    var s=today.getSeconds();

    // run minutes //

    m = checkTime(m);

    // run seconds //

    s = checkTime(s);

    // write //

    document.getElementById('time').innerHTML = d + "-" + mm + "-" + y + "-" + h + ":" + m + ":" + s;

    // timeout //

    var t = setTimeout(function(){startTime()},500);

}

// track //

function checkTime(i) {

    if (i < 10) {i = "0" + i};

    return i;

}
