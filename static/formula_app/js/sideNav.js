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
