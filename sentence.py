class Sentence():
    def __init__(self, *args, **kwargs):
        self.english = kwargs.get("english", "")
        self.french = kwargs.get("french", "")
        self.strength = kwargs.get("strength", 0)
        self.level =  kwargs.get("level", 0)
        self.bookmarked = False
