function openManageUsers() {
    var wrapper = document.getElementById("wrapper");
    wrapper.style.opacity = "0.5";

    document.getElementById('btn_open').style.cursor = 'progress';
    
    setCursorBusy();
    cmd('gnome-control-center-user-accounts')

    setTimeout(function () {
        wrapper.style.opacity = "1.0";
        document.getElementById('btn_open').style.cursor = 'default';
        setCursorNormal();
    }, 2500);
}
