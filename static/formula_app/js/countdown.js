var countDownDate = new Date(document.getElementById("countdown").dataset.value);

var x = setInterval(function () {
	var now = new Date().getTime();
	var distance = countDownDate - now;

	var days = Math.floor(distance / (1000 * 60 * 60 * 24));
	var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
	var seconds = Math.floor((distance % (1000 * 60)) / 1000);

	if (days < 10) {
		if (days < 0) {
			if (days > -10) {
				days = "-0" + Math.abs(days);
			}
		}
		else {
			days = "0" + days;
		}
	}
	if (hours < 10) {
		if (hours < 0) {
			if (hours > -10) {
				hours = "-0" + Math.abs(hours);
			}
		}
		else {
			hours = "0" + hours;
		}
	}
	if (minutes < 10) {
		if (minutes < 0) {
			if (minutes > -10) {
				minutes = "-0" + Math.abs(minutes);
			}
		}
		else {
			minutes = "0" + minutes;
		}
	}
	if (seconds < 10) {
		if (seconds < 0) {
			if (seconds > -10) {
				seconds = "-0" + Math.abs(seconds);
			}
		}
		else {
			seconds = "0" + seconds;
		}
	}

	const cntElem = document.getElementById("cntd");
	cntElem.innerHTML = days + " : " + hours + " : " + minutes + " : " + seconds + " ";

	if (distance < 0){
		cntElem.style.color = "gray";
	}
	else{
		cntElem.style.color = "white";
	}

}, 1000);


// TODO moze da se optimizira tuka ovoa so dropdown kako rabote ako ostane vreme
function smeniSesija(datum) {
	sesija = document.getElementById(datum);
	document.getElementById("dropButton").innerText = sesija.innerHTML;
	countDownDate = new Date(sesija.dataset.value);
}
