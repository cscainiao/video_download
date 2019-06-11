import codecs, os

# 文本写入信息


def __write_log(f, flag, time_str, text):
    try:
        with codecs.open(f, 'a', encoding='utf-8') as f:
            f.write('%s   %s   %s\n' % (time_str, flag,  text))
        return True
    except Exception as e:
        __display_log("ERROR", time_str,  "write log crash: %s" % str(e))
        return False


# 屏幕显示信息
def __display_log(flag, time_str, text):
    print('%s   %s   %s' % (time_str, flag, text))


def log(f, flag, time_str, text):
    if __write_log(f, flag, time_str, text):
        __display_log(flag, time_str, text)

