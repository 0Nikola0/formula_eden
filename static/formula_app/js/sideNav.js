// TODO ako ostavas hamburger menu samo za open a X za close nema da treba if-else tuka
function openNav() {
    const sideNav = document.getElementById("mySidenav");
    if (sideNav.style.width != "100%"){
        sideNav.style.width = "100%";
    }
    else{
        sideNav.style.width = "0";
    }

}


function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}