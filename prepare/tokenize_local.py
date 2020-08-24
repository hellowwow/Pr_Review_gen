import tokenize
import nltk
from nltk import tokenize
from nltk import word_tokenize
from nltk import stem
from nltk import corpus
from nltk import pos_tag
import javalang
import pygments
from pygments import lexers
from pygments.lexers import jvm

def english_token(sentence, tokenize_flag=1, is_filter_stopword=1, stem_flag=1, lemma_flag=1):
    # 两种英文分词方式, 2更优
    if tokenize_flag == 1:
        source_tokens = word_tokenize(sentence)
    elif tokenize_flag == 2:
        tokenizer = tokenize.WordPunctTokenizer()
        source_tokens = tokenizer.tokenize(sentence)
    # print(source_tokens)

    # 删除标点符号
    for token in source_tokens[::-1]:
        if len(token) == 1 and token[0].isalpha() == False:
            source_tokens.remove(token)

    # 过滤停用词
    if is_filter_stopword:
        list_stopWords = list(set(corpus.stopwords.words('english')))
        filtered_stop_words = [w for w in source_tokens if not w in list_stopWords]
    else:
        filtered_stop_words = source_tokens
    # print(filtered_stop_words)

    # 两种词干化处理工具，2更优
    stem_tokens = []
    if stem_flag == 1:
        porterStemmer = stem.PorterStemmer()
        for word in filtered_stop_words:
            stem_tokens.append(porterStemmer.stem(word))
    elif stem_flag == 2:
        snowballStemmer = stem.SnowballStemmer('english')
        for word in filtered_stop_words:
            stem_tokens.append(snowballStemmer.stem(word))

    # 将动名词词型还原，2更优
    lemma_tokens = []
    if lemma_flag == 1:
        lemmatizer = stem.WordNetLemmatizer()
        for word in stem_tokens:
            # 将名词还原为单数形式
            n_lemma = lemmatizer.lemmatize(word, pos='n')
            # 将动词还原为原型形式
            v_lemma = lemmatizer.lemmatize(n_lemma, pos='v')
            # print('%8s %8s %8s' % (word, n_lemma, v_lemma))
            lemma_tokens.append(v_lemma)
    elif lemma_flag == 2:
        lemmatizer = stem.wordnet.WordNetLemmatizer()
        tagged_corpus = pos_tag(stem_tokens)
        for token, tag in tagged_corpus:
            if tag[0].lower() in ['n', 'v']:
                lemma_tokens.append(lemmatizer.lemmatize(token, tag[0].lower()))
            else:
                lemma_tokens.append(token)

    return lemma_tokens

def code_prepare(code_diff):
    res = ''
    code_len = len(code_diff)
    i = 0
    while i < code_len:
        flag = 1
        if i < code_len - 1:
            if code_diff[i] == '@' and code_diff[i + 1] == '@':
                for j in range(i + 2, code_len):
                    if code_diff[j] == '@' and code_diff[j - 1] == '@':
                        i = j
                        flag = 0
                        break
        if flag:
            res += code_diff[i]
        i += 1
    return res

def code_token(code_diff):
    # print(code_diff)
    # print('---------------------------------------')
    code_diff = code_prepare(code_diff)
    # print(code_diff)
    # print('==========================================')
    # print(lexers.guess_lexer(code_diff))
    lexer = lexers.get_lexer_by_name("java", stripall=True)
    tokens = list(pygments.lex(code_diff, lexer))
    # tokens = list(javalang.tokenizer.tokenize(code_diff))
    tokens_list = []
    for token in tokens:
        if str(token[0]) != 'Token.Text' and str(token[0]) != 'Token.Punctuation':
            tokens_list.append(token[1].lower())
    return tokens_list

def test():
    # 测试英文令牌化
    example_text = "was ate Five score years ago, a great American, in whose symbolic shadow we stand today, signed the Emancipation Proclamation. This momentous decree came as a great beacon light of hope to millions of Negro slaves who had been seared in the flames of withering injustice. It came as a joyous daybreak to end the long night of bad captivity."
    print(english_token(example_text, 2, 2, 2))

    # 测试代码令牌化
    example_text = 'System.out.println("Hello " + "world");'
    print(code_token(example_text))

if __name__ == '__main__':
    test()