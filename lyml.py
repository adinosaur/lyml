# -*- coding: UTF-8 –*-

import sys

#token type
BAD_TOKEN = 1
TEXT_TOKEN = 2
TAGBEG_TOKEN = 3
TAGEND_TOKEN = 4
PYCODE_TOKEN = 5

#tokenizer status
TOKEN_STATUS_EMPTY = 1
TOKEN_STATUS_TEXT = 2
TOKEN_STATUS_TAG = 3
TOKEN_STATUS_TAG_BEG = 4
TOKEN_STATUS_TAG_END = 5
TOKEN_STATUS_TAG_PYCODE = 6

STATUS = {
    TOKEN_STATUS_TEXT : TEXT_TOKEN,
    TOKEN_STATUS_TAG_BEG : TAGBEG_TOKEN,
    TOKEN_STATUS_TAG_END : TAGEND_TOKEN,
    TOKEN_STATUS_TAG_PYCODE : PYCODE_TOKEN
}

def tokenizer(text):
    status = TOKEN_STATUS_EMPTY
    token_list = []
    value_list = []
    text_len = len(text)
    jump = -1
    for i, c in enumerate(text):
        if i < jump:
            continue
        
        #状态为空时，通过当前读入的字符即可判断应该进入什么状态
        if status == TOKEN_STATUS_EMPTY:
            if c == '<':
                status = TOKEN_STATUS_TAG
            else:
                status = TOKEN_STATUS_TEXT
                value_list.append(c)
        
        if status == TOKEN_STATUS_TEXT:
            if c == '<':
                if not value_list:
                    #此处需要输出错误提示
                    print "tokenizer error, (%s) return" % sys._getframe().f_lineno
                    print "locals", locals()
                    return
                token_value = ''.join(value_list)
                token_type = STATUS.get(status)
                assert token_type is not None
                token_list.append((token_type, token_value))
                status = TOKEN_STATUS_TAG
                value_list = []
            else:
                value_list.append(c)
        
        #TagBeg状态下通过下一个字符时'/'还是'?'可以判断后续状态
        elif status == TOKEN_STATUS_TAG:
            if c == '/':
                status = TOKEN_STATUS_TAG_END
            elif c == '?':
                #<?py ... ?>
                if i + 2 >= text_len:
                    #此处需要输出错误提示
                    print "tokenizer error, (%s) return" % sys._getframe().f_lineno
                    print "locals", locals()
                    return
                if text[i + 1] != 'p' or text[i + 2] != 'y':
                    #此处需要输出错误提示
                    print "tokenizer error, (%s) return" % sys._getframe().f_lineno
                    print "locals", locals()
                    return
                status = TOKEN_STATUS_TAG_PYCODE
                jump = i + 3
            else:
                status = TOKEN_STATUS_TAG_BEG
                value_list.append(c)
        
        elif status == TOKEN_STATUS_TAG_BEG or \
             status == TOKEN_STATUS_TAG_END:
            #Tag状态结束
            if c == '>':
                if not value_list:
                    #此处需要输出错误提示
                    print "tokenizer error, (%s) return" % sys._getframe().f_lineno
                    print "locals", locals()
                    return
                token_value = ''.join(value_list)
                token_type = STATUS.get(status)
                assert token_type is not None
                token_list.append((token_type, token_value))
                status = TOKEN_STATUS_EMPTY
                value_list = []
            else:
                value_list.append(c)
        
        elif status == TOKEN_STATUS_TAG_PYCODE:
            #Tag状态结束
            if c == '>':
                if len(value_list) <= 1:
                    #此处需要输出错误提示
                    print "tokenizer error, (%s) return" % sys._getframe().f_lineno
                    print "locals", locals()
                    return
                #此处必定不会越界
                if value_list[-1] != '?':
                    #此处需要输出错误提示
                    print "tokenizer error, (%s) return" % sys._getframe().f_lineno
                    print "locals", locals()
                    return
                value_list.pop()
                token_value = ''.join(value_list)
                token_type = STATUS.get(status)
                assert token_type is not None
                token_list.append((token_type, token_value))
                status = TOKEN_STATUS_EMPTY
                value_list = []
            else:
                value_list.append(c)
    
    if value_list:
        token_value = ''.join(value_list)
        #只有Text的Token是可以隐式结尾的
        if status == TOKEN_STATUS_TEXT:
            token_type = STATUS.get(status)
            assert token_type
            token_list.append((token_type, token_value))
        else:
            #此处需要输出错误提示
            return
    return token_list

TOKENS = {
    'color1' : '<font color="#FF0000">', 
    'color2' : '<font color="#FF0000">', 
    'color3' : '<font color="#FF0000">',
    'size1' : '<font size="12">', 
    'size2' : '<font size="16">', 
    'size3' : '<font size="20">',
}

def parser(token_list):
    result_list = []
    tag_stack = []
    for token_type, token_value in token_list:
        if token_type == TEXT_TOKEN:
            result = token_value
            result_list.append(result)
        elif token_type == TAGBEG_TOKEN:
            result = TOKENS.get(token_value)
            if not result:
                #此处需要输出错误提示
                print "parse error, (%s) return" % sys._getframe().f_lineno
                print "locals", locals()
                return
            tag_stack.append(token_value)
            result_list.append(result)
        elif token_type == TAGEND_TOKEN:
            if not tag_stack:
                #此处需要输出错误提示
                print "parse error, (%s) return" % sys._getframe().f_lineno
                print "locals", locals()
                return
            last_tag = tag_stack.pop()
            if last_tag != token_value:
                #此处需要输出错误提示
                print "parse error, (%s) return" % sys._getframe().f_lineno
                print "locals", locals()
                return
            result = "</font>"
            result_list.append(result)
        elif token_type == PYCODE_TOKEN:
            #暂时不做处理
            result = token_value
            result_list.append(result)
    return result_list


if __name__ == "__main__":
    text = "hello world <size1>hehe</size1> zaoshui <?py print 'hello'?>"
    
    token_list = tokenizer(text)
    assert token_list

    result_list = parser(token_list)
    assert result_list

    print ''.join(result_list)