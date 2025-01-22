window.onload = function() {
    function Init() {
        setCursorBusy();
        setTimeout(function () {
            cmd("init-system-info");
        }, 1000);
    }

    Init();
};