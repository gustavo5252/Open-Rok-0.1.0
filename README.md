---

# OpenRok

O OpenRok é um projeto em Python que permite capturar a tela, analisar o texto em imagens e fornecer respostas com base em um banco de dados.

## Funcionalidades

- Captura de tela com seleção de área personalizada.
- Reconhecimento óptico de caracteres (OCR) para extrair texto das imagens.
- Comparação de texto com um banco de dados para encontrar correspondências.
- 
## Objetivo

O OpenRok foi desenvolvido com o objetivo de fornecer assistência para o Quiz Rok, ajudando os jogadores a encontrar respostas rapidamente através do reconhecimento de texto em imagens.

## Instalação

1. Clone o repositório para a sua máquina local:

```bash
git clone https://github.com/gustavo5252/Open-Rok-0.1.0.git
```

2. Instale as dependências necessárias usando o pip:

```bash
pip install -r requirements.txt
```

3. Certifique-se de ter o Tesseract OCR instalado e configurado corretamente:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

## Uso

1. Defina a área de captura clicando em "Área de Captura" no menu e seguindo as instruções.
   - Para selecionar uma Região de Interesse:
     - Pressione a tecla ESPAÇO ou ENTER para confirmar a seleção.
     - Se desejar cancelar a seleção, pressione a tecla `c` e feche a janela.
2. Clique em "Pesquisar" para capturar a área definida e analisar o texto.
3. As informações serão exibidas na interface gráfica, incluindo perguntas, respostas e opções adicionais como copiar o texto.

## Contribuição

- Sinta-se à vontade para abrir issues relatando problemas ou sugestões de melhorias.
- Pull requests são bem-vindos para adicionar novos recursos, resolver problemas ou atualizar o banco de dados.

---
