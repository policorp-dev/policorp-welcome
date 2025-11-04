function openApp(id, appName) {
    var content = document.getElementById("content");
    content.style.opacity = "0.5";
    
    let id_ = "#" + id
    $(id_).addClass('cursor-progress');
    
    cmd(appName);

    setTimeout(function () {
        content.style.opacity = "1.0";

        $(id_).removeClass('cursor-progress');
        
        setCursorNormal();
    }, 1500);
}