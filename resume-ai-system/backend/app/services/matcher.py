from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def match_resume_to_jd(resume_text, jd_text):
    docs = [resume_text, jd_text]

    tfidf = TfidfVectorizer()
    matrix = tfidf.fit_transform(docs)

    score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]

    return round(score * 100, 2)