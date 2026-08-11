class GraphQLError(Exception):
    """
    Levantada quando a resposta da API do GitHub contém a chave "errors".
    """

    def __init__(self, message: str, raw_errors: list[dict]):
        super().__init__(message)
        self.raw_errors = raw_errors
