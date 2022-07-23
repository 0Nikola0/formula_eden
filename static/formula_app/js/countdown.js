var countDownDate = new Date(document.getElementById("countdown").dataset.value);

var x = setInterval(function() {
    var now = new Date().getTime();
  
    var distance = countDownDate - now;
  
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // да има 0 пред бројо ако е помал од 10 (09, 08, 05..)
    if (days < 10){
        days = "0" + days;
    }
    if (hours < 10){
        hours = "0" + hours;
    }
    if (minutes < 10){
        minutes = "0" + minutes;
    }
    if (seconds < 10){
        seconds = "0" + seconds;
    }
    // 

    document.getElementById("cntd").innerHTML = days + " : " + hours + " : "
    + minutes + " : " + seconds + " ";
  
    if (distance < 0) {
      clearInterval(x);
      document.getElementById("demo").innerHTML = "Ako gledas ovoa nesto greska ima so countdown";
    }
  }, 1000);