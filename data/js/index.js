setTimeout(function () {
    cmd('check-init-main');
}, 50);

const videoLink = document.getElementById('videoLink');
let isMouseOver = false;

videoLink.addEventListener('mouseenter', () => {
    isMouseOver = true;
    videoLink.classList.remove('blink');
});

videoLink.addEventListener('mouseleave', () => {
    isMouseOver = false;
    videoLink.classList.add('blink');
});

if (!isMouseOver) {
    videoLink.classList.add('blink');
}

function openApp(id, appName) {
    var header = document.getElementById("header");
    var content = document.getElementById("content");
    var footer = document.getElementById("footer");

    header.style.opacity = "0.5";
    content.style.opacity = "0.5";
    footer.style.opacity = "0.5";
    
    let id_ = "#" + id
    $(id_).addClass('cursor-progress');
    
    cmd(appName);

    setTimeout(function () {
        header.style.opacity = "1.0";
        content.style.opacity = "1.0";
        footer.style.opacity = "1.0";

        $(id_).removeClass('cursor-progress');
        
        setCursorNormal();
    }, 1500);
}

function openCodec() {

    header.style.opacity = "0.5";
    content.style.opacity = "0.5";
    footer.style.opacity = "0.5";

    cmd('init-codec')

    setTimeout(function () {
        header.style.opacity = "1.0";
        content.style.opacity = "1.0";
        footer.style.opacity = "1.0";

        $(id_).removeClass('cursor-progress');
        
        setCursorNormal();
    }, 1500);
}

function openSite(id, host) {
    var header = document.getElementById("header");
    var content = document.getElementById("content");
    var footer = document.getElementById("footer");

    let id_ = "#" + id
    $(id_).addClass('cursor-progress');

    header.style.opacity = "0.5";
    content.style.opacity = "0.5";
    footer.style.opacity = "0.5";

    cmd(`opensite=${host}`);

    setTimeout(function () {
        header.style.opacity = "1.0";
        content.style.opacity = "1.0";
        footer.style.opacity = "1.0";

        $(id_).removeClass('cursor-progress');
        
        setCursorNormal();
    }, 1500);
}

function openEmail(id, email) {
    var header = document.getElementById("header");
    var content = document.getElementById("content");
    var footer = document.getElementById("footer");

    let id_ = "#" + id
    $(id_).addClass('cursor-progress');

    header.style.opacity = "0.5";
    content.style.opacity = "0.5";
    footer.style.opacity = "0.5";

    cmd(`openemail=${email}`);

    setTimeout(function () {
        header.style.opacity = "1.0";
        content.style.opacity = "1.0";
        footer.style.opacity = "1.0";

        $(id_).removeClass('cursor-progress');
        
        setCursorNormal();
    }, 3000);
}

function openVideoTour() {
    var header = document.getElementById("header");
    var content = document.getElementById("content");
    var footer = document.getElementById("footer");

    $('#videoLink').addClass('cursor-progress');

    header.style.opacity = "0.5";
    content.style.opacity = "0.5";
    footer.style.opacity = "0.5";

    cmd('init-manual-video')

    setTimeout(function () {
        header.style.opacity = "1.0";
        content.style.opacity = "1.0";
        footer.style.opacity = "1.0";

        $('#videoLink').removeClass('cursor-progress');
        
        setCursorNormal();
    }, 3000);
}

var checkbox = document.getElementById('openNextStartup');

checkbox.addEventListener('change', function () {
    var checkboxRef = this;

    setTimeout(function () {
        if (checkboxRef.checked) {
            cmd('check-status-init=true');
        } else {
            cmd('check-status-init=false');
        }
    }, 50);
});
