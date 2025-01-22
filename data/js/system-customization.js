window.onload = function () {
    function Init() {
        setCursorBusy();
        setTimeout(function () {
            cmd("gnome-theme");
        }, 50);
    }

    Init();
};

function openConfigBackground() {
    var wrapper = document.getElementById("wrapper");
    wrapper.style.opacity = "0.5";

    document.getElementById('btn_background').style.cursor = 'progress';
    
    setCursorBusy();
    cmd('gnome-control-center-background');

    setTimeout(function () {
        wrapper.style.opacity = "1.0";
        document.getElementById('btn_background').style.cursor = 'default';
        setCursorNormal();
    }, 2500);
}

function openConfigDisplay() {
    var wrapper = document.getElementById("wrapper");
    wrapper.style.opacity = "0.5";

    document.getElementById('btn_display').style.cursor = 'progress';

    setCursorBusy();
    cmd('gnome-control-center-display');

    setTimeout(function () {
        wrapper.style.opacity = "1.0";
        document.getElementById('btn_display').style.cursor = 'default';
        setCursorNormal();
    }, 2500);
}

function selectBtnLight() {
    var btn = document.getElementById('btn_light_mode');
    btn.classList.remove('btn-transparent');
    btn.classList.add('btn-primary');

    setCursorNormal();
}

function selectBtnDark() {
    var btn = document.getElementById('btn_dark_mode');
    btn.classList.remove('btn-transparent');
    btn.classList.add('btn-primary');

    setCursorNormal();
}

function setTheme(theme) {
    var btn_light = document.getElementById('btn_light_mode');
    var btn_dark = document.getElementById('btn_dark_mode');

    setCursorBusy();
    setTimeout(function () {
        cmd(`set-gnome-theme-${theme}`);
    }, 50);

    if (theme == "light") {
        btn_light.classList.remove('btn-transparent');
        btn_light.classList.add('btn-primary');

        btn_dark.classList.remove('btn-primary');
        btn_dark.classList.add('btn-transparent');
    }
    else {
        btn_dark.classList.remove('btn-transparent');
        btn_dark.classList.add('btn-primary');

        btn_light.classList.remove('btn-primary');
        btn_light.classList.add('btn-transparent');
    }

    setCursorNormal();
}
