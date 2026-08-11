FROM debian:trixie-slim

# Evita prompts interativos durante a instalação de pacotes
ENV DEBIAN_FRONTEND=noninteractive

# Atualiza os índices de pacotes e instala dependências de compilação,
# bibliotecas de desenvolvimento GTK4/Adw e pacotes de fontes essenciais
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    meson \
    ninja-build \
    gcc \
    pkg-config \
    python3-dev \
    python3-pip \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-4.0 \
    gir1.2-adw-1 \
    libgtk-4-dev \
    libadwaita-1-dev \
    libgirepository1.0-dev \
    gettext \
    dbus \
    dbus-x11 \
    fonts-cantarell \
    fontconfig \
    at-spi2-core \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Atualiza o cache de fontes do container
RUN fc-cache -f -v

# Define o diretório de trabalho padrão dentro do container
WORKDIR /workspace