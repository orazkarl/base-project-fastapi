from sqlalchemy import TypeDecorator, String


class ChoiceType(TypeDecorator):
    impl = String
    cache_ok = True
    internal_only = True

    def __init__(self, choices, *args, **kwargs):
        self.choices = choices
        super().__init__()
