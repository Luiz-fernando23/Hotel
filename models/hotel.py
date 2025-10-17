class HotelModel:
    def __init__(self, hotel_id, nome, estrela, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrela = estrela
        self.diaria = diaria
        self.cidade = cidade

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrela': self.estrela,
            'diaria': self.diaria,
            'cidade': self.cidade
        }