# convert_to_300_dpi

Programa Python para converter arquivos PDF para resolução de 300 DPI, utilizando a biblioteca Poppler.

## Funcionalidade

- Recebe um arquivo PDF como entrada.
- Converte todas as páginas para uma resolução de 300 DPI.
- Gera um novo arquivo PDF com a resolução atualizada.

## Requisitos

- Python 3.13 ou superior
- Poppler instalado (ou incluído na pasta `poppler` do projeto)
- Dependências Python listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
    ```bash
     git clone https://github.com/zacsampaio/zacspy.git
     ```

2. Instale as dependências:
    ```bash
     pip install -r requirements.txt
    ```

3. Certifique-se que o Poppler está disponível (ou está na pasta poppler).

## Uso
Execute o script passando o arquivo PDF de entrada e o nome do arquivo de saída:
```bash
pyinstaller --onefile --noconsole --name=CONVERT_PDF_X_DPI --icon=apps/convert_to_dpi/icon.ico apps/convert_to_dpi/main.py
```

## Empacotado com PyInstaller

O executável DPI_X_PDF.exe está disponível na pasta dist/ após a build com PyInstaller.

Para criar o executável:
```bash
pyinstaller --onefile --noconsole --name=CONVERT_PDF_X_DPI --icon=apps/convert_to_dpi/icon.ico --add-data "poppler;poppler" apps/convert_to_dpi/main.py
```


