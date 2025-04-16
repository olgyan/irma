import get_text


def remove_fields(file, fields_to_remove=(
    '#001:','#005:','#100:','#105:','#801:'
    )):
    text = get_text.outof(file, 'to lines')
    selected_lines = [line for line in text
        if all(tag not in line for tag in fields_to_remove)]
    get_text.into(file, 'from lines', selected_lines)