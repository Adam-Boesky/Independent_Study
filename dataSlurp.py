corpus_file = open("/Users/student/PycharmProjects/IndependentStudy/enEs.txt", "r")
corpus_text = corpus_file.read(-1)

parallels = [["" for x in range(21007)] for y in range(2)]


for i in range(21007):
    # Take the english data:
    parallels[0][i] = corpus_text[5:corpus_text.find("</seg>")]
    corpus_text = corpus_text[corpus_text.find("</seg>") + 6:]
    # Take the spanish data:
    parallels[1][i] = corpus_text[5:corpus_text.find("</seg>")]
    corpus_text = corpus_text[corpus_text.find("</seg>") + 6:]

print(parallels)