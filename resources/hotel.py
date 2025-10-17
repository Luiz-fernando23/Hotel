from flask_restful import Resource, reqparse 
from models.hotel import HotelModel



hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha hotel',
        'estrela':4.3,
        'diaria': 230.23,
        'cidade': 'Rio de janeiro'
    },
        {
        'hotel_id': 'bravo',
        'nome': 'Bravo hotel',
        'estrela':7.3,
        'diaria': 500.21,
        'cidade': 'Santa Catarina '
    },
        {
        'hotel_id': 'charlie',
        'nome': 'Charlie hotel',
        'estrela':4.3,
        'diaria': 230.23,
        'cidade': 'Santa Catarina '
    }
]

class Hoteis(Resource):

    def get(self):
        return {'hoteis': hoteis} 

class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrela')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None
    
    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found.'}, 404
    
    def post(self, hotel_id):

        dados = Hotel.argumentos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()
        hoteis.append(novo_hotel)
        return novo_hotel, 200
    
    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()
        hotel = Hotel.find_hotel(hotel_id)

        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200
        
        hoteis.append(novo_hotel)
        return novo_hotel, 201
        
        

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hoteis if hotel['hotel_id'] != hotel_id]
        return {'mensage': 'Hotel deleted'}