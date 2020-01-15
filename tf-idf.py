import MeCab
import math
import collections
tagger = MeCab.Tagger()


def worddividor(filepath):
    """do mornophical analysis, separate the words.
       if a noun (or name) connects to another noun (or name), combine into one word
    """
    dividors = []
    with open(filepath, "r", encoding="utf-8") as r:
        lines = r.readlines()
        for i in range(len(lines)):
            words_list = []
            node = tagger.parseToNode(lines[i])
            pos = "no"
            while node:
                if "名詞" in node.feature and "数" not in node.feature and "人名" not in node.feature:
                    if pos == "yes":
                        words_list[-1] = words_list[-1] + node.surface
                    else:
                        words_list.append(node.surface)
                        pos = "yes"
                elif "名詞" in node.feature and "数" not in node.feature and "人名" in node.feature:
                    if pos == "name":
                        words_list[-1] = words_list[-1] + node.surface
                    else:
                        words_list.append(node.surface)
                    pos = "name"
                else:
                    words_list.append(node.surface)
                    pos = "no"
                node = node.next
            if words_list:
                dividors.append(words_list)
    return dividors


def tfidf(lists, corpus):
    """calutate the tf-idf points,
       choose the top5 to output
    """
    usedwords = []
    documentlength = len(lists)
    wordslist = list(set(lists))
    turns = collections.Counter(lists)
    turns = dict(turns)
    for i in wordslist:
        count = 0
        for j in corpus:
            if i in j:
                count += 1
        idf = math.log(len(corpus)/(count+1))
        tf = turns[i] / documentlength
        tf_idf = tf * idf
        turns[i] = tf_idf
    result = sorted(turns.items(), key=lambda item: item[1], reverse=True)
    for i in range(len(result)):
        usedwords.append(result[i][0])
    return usedwords[:5]  # 出力単語数


def main():
    filepath = "filepath"  # please input the path of txtfile
    allwords = []
    corpus = worddividor(filepath)
    for i in range(len(corpus)):
        goodkeywords = tfidf(corpus[i], corpus)
        allwords.append(goodkeywords)
    print(allwords)


if __name__ == "__main__":
    main()
