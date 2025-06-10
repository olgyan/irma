import os
import re
from transliterate import translit


def modify_file(filename, func):
    """Opens, changes (with func()) and closes text file."""
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
        text = func(text)
        print(func)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    print(filename)


def modify_files(folder, func):
    """Opens, changes (with func()) and closes all text files in folder."""
    folder = folder.replace(r'\\', '/')
    for filename in os.listdir(folder):
        with open(f'{folder}/{filename}', 'r', encoding='utf-8') as f:
            text = func(f.read())
        with open(f'{folder}/{filename}', 'w', encoding='utf-8') as f:
            f.write(text)
        print(filename)


def open_list(listfile, folder):
    """Takes a text file where filenames are listed and a path to the folder
    where all the files are and opens all the listed files.
    """
    listfile = listfile.replace(r'\\', r'/')
    folder = folder.replace(r'\\', r'/')
    with open(listfile, 'r') as f:
        files_list = f.readlines()
    for filename in files_list:
        try:
            os.startfile(f'{folder}/{filename.strip()}')
        except Exception as e:
            print(filename, e)
            os.startfile(listfile)


def rename_translit(folder_name, ext='pdf'):
    """Transliterates names of all pdf (or other ext) files
    in folder folder_name from Cyrillic to Latin.
    """
    for elem in os.listdir(folder_name):
        if ext == os.path.splitext(
                    os.path.normpath(
                    os.path.join(folder_name, elem
                    )))[1]:
            tfn = translit(elem, language_code='ru', reversed=True)
            tfn = tfn.replace(' ', '_')
            os.rename(f'{folder_name}\{elem}', f'{folder_name}\{tfn}')
            print(f'{tfn} renamed')
        else:
            print(elem)


def join_files(folder, sep='\n', files_list=None, condition=None):
    """Joins all files in folder folder_name to one text file. 
    Inserts separating symbols between them if sep is given.
    """
    if files_list is None:
        files_list = os.listdir(folder)
    for elem in files_list:
        with open(
                os.path.normpath(os.path.join(folder, elem)), "r", 
                encoding="utf-8", errors='ignore'
                ) as f:
            if condition:
                single_file = ''.join([
                line for line in f.readlines() if condition
                ])
            else: single_file = f.read()
                    
        with open(f'{folder}.txt', 'a', encoding="utf-8") as alltogether:
            alltogether.write(single_file)
            alltogether.write(sep)


def split_file(filename, sep='\n*****', keepsep=True):
    """Separates file into a folder (named like the file) of small files.
    If keepsep is True then the sep is included into the files.
    """
    with open(filename, 'r', encoding="utf-8", errors='ignore') as f:
        many_files = f.read().split(sep)
        counter_length = len(str(len(many_files)))
        for i, elem in enumerate(many_files):
            counter = str(i).rjust(counter_length, '0')
            with open(
                    f'c:/irbiswrk/{filename}/{counter}.txt',
                    'w', encoding="utf-8"
                    ) as f:
                f.write(elem)
                if keepsep: f.write(sep)
    

def files_together(folder_name):
    for elem in os.listdir(folder_name):
        with open(
                f'{folder_name}/{elem}',
                "r", encoding="utf-8", errors='ignore'
                ) as f:
            single_file = ''.join([
                    line for line in f.readlines() if bool(re.match(
                    r"#010:|#200:|#215:|#330:|#210:|\*\*\*\*\*",
                    line))])
            single_file = re.sub(
                r'#210: \^C(.+)\^C',
                r'#210: ^C\1\n#210: ^C',
                single_file)
            single_file = re.sub(
                r'#215: \^A(\d+) с.',
                r'#215: ^A\1',
                single_file)
            single_file = re.sub(
                r'\^(.)Издательство \"(.+)\"',
                r'^\1\2',
                single_file)
            single_file = re.sub(
                r'(?:ООО|АО) \"(.+)\"',
                r'\1',
                single_file)
                    
        with open(f'{folder_name}.txt', 'a', encoding="utf-8") as alltogether:
            alltogether.write(single_file)


def els_files_together(folder_name):
    for elem in os.listdir(folder_name):
        with open(
                f'{folder_name}/{elem}',
                "r", encoding="utf-8", errors='ignore'
                ) as f:
            single_file = ''.join([
                line for line in f.readlines() 
                if not bool(re.match(
                r"#001:|#005:|#003:|#608:|#691:|#330:|#801:|#5501:",
                line))])
            single_file = ''.join([line for line in f.readlines()])
            
            single_file = re.sub(
                r'#210: \^C(.+)\^C', 
                r'#210: ^C\1\n#210: ^C', 
                single_file)
            single_file = re.sub(
                r'#215: \^A(\d+) с.', 
                r'#215: ^A\1', 
                single_file)
            single_file = re.sub(
                r'\^(.)Издательство \"(.+)\"', 
                r'^\1\2', 
                single_file)
            single_file = re.sub(
                r'(?:ООО|АО) \"(.+)\"', 
                r'\1', 
                single_file)
            single_file = re.sub(
                r'#951:(.+)\^H01', 
                r'#951:\1^H05^TСсылка на документ в ЭБС Znanium', 
                single_file)
            single_file = single_file.replace(
                '*****', 
                '\n'.join(
                    '#900: ^Tl',
                    '#181: ^Ai',
                    '#182: ^Ab', 
                    '#610: ЭБС ZNANIUM (СПО)',
                    '#905: ^A1^B1',
                    '*****'
                    )
                )
            single_file = single_file.replace('\n', '\r\n')
                    
        with open(f'{folder_name}.txt', 'a', encoding="utf-8") as alltogether:
            alltogether.write(single_file)

def remove_fields(files_list, field='#953:'):
    print('Удаляем ненужные поля...')

    for filename in files_list:
        with open(
            f'c:\irbiswrk\{filename}',
            'r', encoding="utf-8", errors='ignore') as f:
            text = f.readlines()
            selected_lines = [line for line in text if field not in line]

        with open(
            f'c:\irbiswrk\{filename}',
            'w',  encoding="utf-8", errors='ignore') as f:
            f.writelines(selected_lines)
            print(f'{filename} обработан!')
        
    print('Готово')


def sort_fields(files_list):
    """for comparing text files"""
    print('Выполняется сортировка...')

    for filename in (files_list):
        with open(
                f'c:\irbiswrk\{filename}',
                'r', encoding="utf-8", errors='ignore'
                ) as f:
            text = f.read()
            entries = text.split('*****')
            sorted_entries = []
            for eachentry in entries:
                selected_lines = [
                line for line in eachentry.splitlines() if all((
                    bool('#907:' not in line), 
                    bool('#910:' not in line), 
                    bool('#999:' not in line)
                ))]
                sorted_entries.append("\r\n".join(sorted(selected_lines)))
                sorted_entries = sorted(sorted_entries)

        with open(
                f'c:\irbiswrk\sorted_{filename}',
                'w',  encoding="utf-8", errors='ignore'
                ) as f:
            f.write('\r\n*****'.join(sorted_entries))
            print(f'{filename} отсортирован!')
        
    print('Готово')

def get_330(folder_name):
    to_save = ('#200:', '#330:', '*****',)
    with open(
            'c:/Users/yanovskaya-oa/Documents/Scripts/330.txt',
            'w', encoding="utf-8"
            ) as alltogether:
        for fol in os.listdir(folder_name):
            for elem in os.listdir(f'{folder_name}/{fol}'):
                print(elem)
                with open(
                        f'{folder_name}/{fol}/{elem}',
                        "r", encoding="utf-8", errors='ignore'
                        ) as f:
                    for line in f.readlines():
                        if line[:5] in to_save:
                            alltogether.write(line)
    
def uncapslock(phrase):
    """Like built-in capitalize() but for multi-sentence texts:
    keep uppercase letters after periods. Does not work if there are
    digits in the phrase.
    """
    if phrase.isupper():
        new = phrase.capitalize()
        if '. ' in new:
            new = re.sub(
                r'(?<=\. )(.)', 
                lambda m: m.group(1).upper(), 
                new)
        if new != phrase:
            print(f'{phrase} > {new}')
    """return Roman numbers to uppercase"""
    new = re.sub(
        r'(\b[IVXivx]+\b)',
        lambda m: m.group(1).upper(), 
        new)

    return new            


def uncapslock_fields(txt):
    fields = re.findall(
        r'(?<=\^.)(.+?)(?=\^|\n)',
        txt)
    for field in fields:
        if field.isupper():
            new = uncapslock(field)
            txt = txt.replace(field, new)
    return txt
    
    
def split_irbis_entries(txt):
    entries = txt.split('\n*****\n')
    for entry in entries:
        name = entry[entry.find('#200: ^A')+8:entry.find('^F')]
        with open(f'c:\irbiswrk\{name}.txt', 'w') as f:
            f.write(entry)
            f.write('\n*****')


def trim_itf(txt):
    """deletes everything after '*****' in IRBIS text file"""
    txt = ''.join(txt.partition('*****')[0:2])
    return txt
