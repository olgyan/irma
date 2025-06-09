import sys
from pathlib import Path

from tqdm import tqdm

from . import get_text

def files_together(folder_name):
    folder = Path(folder_name)
    assert folder.is_dir(), 'нет такой папки'
    
    txt_files = [f for f in folder.iterdir() if f.suffix == '.txt']
    assert txt_files, 'Папка должна содержать файлы .txt'
    
    records = list(
        get_text.outof(file, 'to string')
        for file in tqdm(txt_files, desc="Собираем файлы воедино")
    )
    get_text.into(f'{folder_name}.txt', 'from_records', records)

if __name__ == "__main__":
    if len(sys.argv) > 0:
        files_together(sys.argv[1])
    else:
        folder_name = input('Папка с файлами, которые надо собрать: ')
        files_together(folder_name)
