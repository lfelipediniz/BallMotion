#!/bin/bash

# =============================================================================
# Simulador de Trajetória 3D de Bola - Script de Execução Automatizado
# =============================================================================
# Script que automaticamente configura o ambiente e executa a simulação
# =============================================================================

set -e

echo "🏀 BallMotion - Simulador de Trajetória 3D de Bola"
echo "=================================================="
echo

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado! Por favor, instale o Python 3.9+ primeiro."
    exit 1
fi

# Verifica arquivos necessários
if [ ! -f "bola.mp4" ]; then
    echo "❌ Arquivo 'bola.mp4' não encontrado!"
    echo "   Certifique-se de que o arquivo de vídeo está na pasta atual."
    exit 1
fi

if [ ! -f "annotations.xml" ]; then
    echo "❌ Arquivo 'annotations.xml' não encontrado!"
    echo "   Certifique-se de que o arquivo de anotações CVAT está na pasta atual."
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ Arquivo 'requirements.txt' não encontrado!"
    exit 1
fi

echo "🔧 Configurando ambiente..."

# Remove ambiente virtual existente se houver problemas
if [ -d "venv" ]; then
    echo "   Removendo ambiente virtual existente..."
    rm -rf venv
fi

# Cria novo ambiente virtual
echo "   Criando ambiente virtual Python..."
python3 -m venv venv

# Ativa ambiente virtual e instala dependências
echo "   Instalando dependências..."
source venv/bin/activate

# Atualiza pip primeiro
venv/bin/python -m pip install --upgrade pip

# Instala requirements
venv/bin/pip install -r requirements.txt

echo "✅ Ambiente configurado com sucesso!"
echo
echo "🚀 Executando simulação..."
echo "   (Use --help para ver todas as opções disponíveis)"
echo

# Executa com parâmetros padrão (usuário pode modificar)
venv/bin/python main.py \
    --video bola.mp4 \
    --xml annotations.xml \
    --out out \
    "$@"

echo
echo "🎉 Simulação concluída com sucesso!"
echo "📁 Verifique os arquivos gerados na pasta 'out/'"
echo "   - series.csv: dados numéricos da trajetória"
echo "   - trajetoria_3d.png: gráfico 3D da trajetória"
echo "   - bola_annotado.mp4: vídeo com anotações"
echo "   - E muito mais!"