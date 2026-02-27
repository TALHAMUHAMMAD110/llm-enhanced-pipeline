from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def text_cosine_similarity(text1, text2):
    # Step 1: convert text to vectors
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])

    # Step 2: compute cosine similarity
    similarity = cosine_similarity(vectors[0], vectors[1])

    # Step 3: return score
    return similarity[0][0]
