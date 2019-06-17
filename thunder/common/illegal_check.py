# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from thunder.settings import BASE_DIR
from decorators import singleton

# 敏感词 检查算法dfa
class Node(object):
    def __init__(self):
        self.children = None

# The encode of word is UTF-8
# The encode of message is UTF-8
@singleton
class Dfa(object):

    def __init__(self):
        #self.root=None
        path=os.path.join(BASE_DIR, 'thunder/conf/illegal_words')
        self.root=Node()
        fp = open(path,'r')
        for line in fp:
            line = line.strip()
            self.add_word(line)
        fp.close()

    # The encode of word is UTF-8
    def add_word(self,word):
        if not isinstance(word, unicode):
            word = word.decode('utf-8')
        word = word.lower()
        word = word.strip()
        node = self.root
        iEnd=len(word)-1
        for i in xrange(len(word)):
            if node.children == None:
                node.children = {}
                if i!=iEnd:
                    node.children[word[i]]=(Node(),False)
                else:
                    node.children[word[i]]=(Node(),True)

            elif word[i] not in node.children:
                if i!=iEnd:
                    node.children[word[i]]=(Node(),False)
                else:
                    node.children[word[i]]=(Node(),True)
            else: #word[i] in node.children:
                if i==iEnd:
                    Next,bWord=node.children[word[i]]
                    node.children[word[i]]=(Next,True)

            node=node.children[word[i]][0]


    # 判断是否是敏感词
    def contains_illegal_words(self, sMsg):
        if sMsg is None:
            return False
        #dfa = Dfa()
        if not isinstance(sMsg, unicode):
            sMsg = sMsg.decode('utf-8')
        sMsg = sMsg.lower()
        root=self.root
        iLen=len(sMsg)
        for i in xrange(iLen):
            p = root
            j = i
            while (j<iLen and p.children!=None and sMsg[j] in p.children):
                (p,bWord) = p.children[sMsg[j]]
                if bWord:
                    return True
                j = j + 1
        return False

    # 敏感词替换
    def replace_illegal_words(self, sMsg, replacement='*'):
        if sMsg is None:
            return sMsg
        #dfa = Dfa()
        if not isinstance(sMsg, unicode):
            sMsg = sMsg.decode('utf-8')
        if not isinstance(replacement, unicode):
            replacement = replacement.decode('utf-8')
        replace_msg = list(sMsg)
        sMsg = sMsg.lower()
        root=self.root
        iLen=len(sMsg)
        i = 0
        illegal_position = 0
        while(i < iLen):
            p = root
            j = i
            illegal_position = i

            while (j<iLen and p.children!=None and sMsg[j] in p.children):
                (p,bWord) = p.children[sMsg[j]]

                if bWord:
                    illegal_position = j+1
                j = j + 1
            if illegal_position>i:
                j = i
                while (j<illegal_position):
                    replace_msg[j] = replacement
                    j += 1
                i = illegal_position-1
            i += 1
        return ''.join(replace_msg)

# 调用
illegal_words_check = Dfa()
