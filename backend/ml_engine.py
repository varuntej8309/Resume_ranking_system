from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MLEngine:
    def __init__(self):
        # Using English stop words to filter out common noise
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def rank_resumes(self, job_description, resumes_data):
        """
        Rank resumes against the job description.
        resumes_data: List of dicts {'filename': str, 'text': str}
        """
        if not resumes_data or not job_description:
            return []

        # Combine JD and resumes into a single corpus for vectorization
        corpus = [job_description] + [r['text'] for r in resumes_data]
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            
            # JD is the first vector, resumes are the rest
            jd_vector = tfidf_matrix[0:1]
            resume_vectors = tfidf_matrix[1:]
            
            # Calculate cosine similarity
            similarities = cosine_similarity(jd_vector, resume_vectors).flatten()
            
            # Map scores back to filenames
            results = []
            for i, score in enumerate(similarities):
                results.append({
                    'filename': resumes_data[i]['filename'],
                    'score': round(float(score) * 100, 2)
                })
                
            # Sort by score descending
            return sorted(results, key=lambda x: x['score'], reverse=True)
            
        except Exception as e:
            print(f"ML Processing error: {str(e)}")
            return []
