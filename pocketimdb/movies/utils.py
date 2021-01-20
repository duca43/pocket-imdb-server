def append_movie_feedbacks(movie, user):
    movie.likes = movie.moviefeedback_set.filter(feedback=True).count()
    movie.dislikes = movie.moviefeedback_set.filter(feedback=False).count()
    movie.user_feedback = None
    user_movie_feedbacks = movie.moviefeedback_set.filter(user=user)
    if len(user_movie_feedbacks) > 0:
        movie.user_feedback = user_movie_feedbacks[0].feedback