document.addEventListener('DOMContentLoaded', function() {
    // Determina o idioma do sistema
    const systemLanguage = navigator.language || navigator.userLanguage; // Pode ser pt-BR, en-US, etc.

    // Verifica se o idioma do sistema é português (pt) ou outro idioma
    const isPortuguese = systemLanguage.startsWith('pt');

    // Seleciona todos os elementos com a classe .hover-box
    const hoverBoxes = document.querySelectorAll('.hover-box');

    // Função para aplicar a substituição de BREAK por <br>
    function applyTextReplacement(language) {
        hoverBoxes.forEach(function(hoverBox) {
            // Pega o conteúdo do atributo data-lang-{language}
            const text = hoverBox.getAttribute(`data-lang-${language}`);

            // Substitui o marcador [[BREAK]] por <br>
            const replacedText = text.replace(/BREAK/g, '<br>');

            // Atualiza o conteúdo da hover-box com o texto modificado
            hoverBox.innerHTML = replacedText;
        });
    }

    // Aplica a substituição conforme o idioma
    if (isPortuguese) {
        applyTextReplacement('pt');  // Se o idioma for português, usa o data-lang-pt
    } else {
        applyTextReplacement('en');  // Se não for português, usa o data-lang-en
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Determina o idioma do sistema
    const systemLanguage = navigator.language || navigator.userLanguage; // Pode ser pt-BR, en-US, etc.

    // Verifica se o idioma do sistema é português (pt) ou outro idioma
    const isPortuguese = systemLanguage.startsWith('pt');

    // Seleciona todos os elementos com a classe text-md-left
    const textElements = document.querySelectorAll('.text-md-left');

    // Função para aplicar a substituição de BREAK pelo elemento <a>
    function applyTextReplacement(language) {
        textElements.forEach(function(element) {
            // Pega o conteúdo do atributo data-lang-{language}
            const text = element.getAttribute(`data-lang-${language}`);

            // Substitui BREAK pelo elemento <a> com onclick e id
            const replacedText = text.replace(/BREAK/g, `<a onclick="openSite('btn_suport', 'https://www.policorp.com.br/faq')" id="btn_suport" style="color: white;">https://www.policorp.com.br/faq</a>`);

            // Atualiza o conteúdo do elemento com o texto modificado
            element.innerHTML = replacedText;
        });
    }

    // Aplica a substituição conforme o idioma
    if (isPortuguese) {
        applyTextReplacement('pt');  // Se o idioma for português, usa o data-lang-pt
    } else {
        applyTextReplacement('en');  // Se não for português, usa o data-lang-en
    }
});
