# Japanese -> Romanji Test

import pykakasi
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *

# import IPython

# lyrics = """
# ひたひた零れる　赤い赤い錆色
# わたしは煤けたブリキのひと
# 空っぽの身体に　トクン　トクン　脈打つ
# あなたが悪い魔法を解いたのでしょう

# おやすみ　また逢える日まで

# ずっと　ずっと　穴の空いていた胸が
# いまはこんなに痛いよ　痛いよ
# 深く　深く　あなたが残した
# この痛みが心なんだね

# ふわふわ　たてがみ　臆病風になびく
# あなたがわたしを弱くしたの

# 時間は足早　心は裏腹
# 手を振り笑うけど　脚は震える

# ずっと　ずっと　強がっていただけだ
# 本当は　ねえ　怖いよ　怖いよ
# だけど行くよ　あなたがくれたのは
# 弱さ見せない勇気なんかじゃない

# 何も見えない　聞こえもしない
# 物言わない案山子のままいられたら
# この疼きも　何もかも　知らずに済んだはずなのに

# ずっと　ずっと　凍てついていた胸が
# 溶け出して　ああ　痛いよ　痛いよ
# でもね　行くよ　たどり着く場所が
# 虹の彼方じゃなくたって
# いいんだ　きっと　また逢えるから
# また逢えるまで　ねえ　おやすみ
# """.split()

def tokenize(lyric_list):
    char_filters = [UnicodeNormalizeCharFilter()]
    tokenizer = Tokenizer()
    token_filters = [CompoundNounFilter(), LowerCaseFilter()]
    a = Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)

    for verse in lyrics:
        tokenized_sentence = a.analyze(verse)
        katakana = ' '.join([t.extra[4] if t.extra is not None else t.surface for t in tokenized_sentence])

        yield katakana

def to_romanji(lyric_list):
    kks = pykakasi.kakasi()
    kks.setMode("K", "a")
    converter = kks.getConverter()

    transliterated_verse = [converter.do(verse) for verse in tokenize(lyric_list)]

    return transliterated_verse
