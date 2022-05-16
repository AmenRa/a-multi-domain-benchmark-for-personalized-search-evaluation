from html import unescape


def normalize_str(s):
    try:
        return unescape(str(s.encode("utf-8"), "utf-8"))
    except:
        print(s)
        exit()
