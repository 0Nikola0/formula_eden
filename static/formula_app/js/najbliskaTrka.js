// TODO mozze podobro so indeksi ovaka dvapati ode niz niza za da najde koja trka e (dole e drugio loop)
function findClosestPrevDate(arr, target) {
    let targetDate = new Date(target);
    let previousDates = arr.filter(e => (targetDate - new Date(e)) < 0)
    let sortedPreviousDates = previousDates.filter((a, b) => new Date(a) - new Date(b))
    return sortedPreviousDates[0] || null
}

const deneska = new Date().getTime();
var data = JSON.parse("{{data|escapejs}}")['results'];
var dateArray = [];

data.forEach(element => {
    try{
        dateArray.push(element['sessions']['7']['date']);
    }
    catch (e){
        // pass
    }
});

let najbliskaData = findClosestPrevDate(dateArray, deneska);
var najblisko = null;

// TODO drugio loop, popravi da e se u edno
data.forEach(element => {
    try{
        if (element['sessions']['7']['date'] == najbliskaData){
            najblisko = element;
        }
    }
    catch (e){
        // pass
    }
});

document.getElementById("traka").innerHTML = najblisko['country'] + " - " + najblisko['track']
document.getElementById("countdown").dataset.value = najbliskaData;