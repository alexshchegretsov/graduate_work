class FilmNotFoundException(Exception):
    def __init__(self, message: str = 'Фильм не найден'):
        self.message = message
        super().__init__(self.message)