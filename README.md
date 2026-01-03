# Renomeador de Arquivos

Aplicativo em Python com interface gráfica para renomear arquivos em lote,
com pré-visualização da seleção e detecção automática de conflitos de nomes.

## Funcionalidades
- Seleção de pasta
- Substituição de texto em nomes de arquivos
- Opção de incluir subpastas
- Pré-visualização dos arquivos afetados
- Seleção individual de arquivos
- Numeração automática em caso de conflito (ex: arquivo (2).txt)

## Tecnologias
- Python 3
- Tkinter
- PyInstaller

## Como executar
```bash
python renomeador_arquivos.py 

```

## Gerar executável
```bash
python -m PyInstaller --onefile --windowed renomeador_arquivos.py
