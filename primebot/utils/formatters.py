def list_to_str(ini_list):
    str1 = '[%s]' % ', '.join(map(str, ini_list))
    str1 = str1[1:-1]
    return str1


def list_to_bullets(ini_list):
    result = "\n"
    for item in ini_list:
        result = result + "- " + item + "\n"
    return result
