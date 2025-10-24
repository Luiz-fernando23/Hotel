from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
 
class Hoteis(Resource):
 
    path_params = reqparse.RequestParser() 
    path_params.add_argument('cidade', type=str, default="",location='args') 
    path_params.add_argument('estrelas_min', type=float, default=0, location='args') 
    path_params.add_argument('estrelas_max', type=float, default=0, location='args')
    path_params.add_argument('diaria_min', type=float, default=0, location='args') 
    path_params.add_argument('diaria_max', type=float, default=0, location='args') 
    path_params.add_argument("itens",type=float, default=3, location="args") 
    path_params.add_argument("pagina",type=float, default=1, location="args") 
 
    def get(self):
        meus_filtros = Hoteis.path_params.parse_args()
 
        query = HotelModel.query 
 
        if meus_filtros["cidade"]:
            query = query.filter(HotelModel.cidade == meus_filtros["cidade"])
        if meus_filtros["estrelas_min"]:
            query = query.filter(HotelModel.estrelas >= meus_filtros["estrelas_min"])
        if meus_filtros["estrelas_max"]:
            query = query.filter(HotelModel.estrelas <= meus_filtros["estrelas_max"])
        if meus_filtros["diaria_min"]:
            query = query.filter(HotelModel.diaria >= meus_filtros["diaria_min"])
        if meus_filtros["diaria_max"]:
            query = query.filter(HotelModel.diaria <= meus_filtros["diaria_max"])
        
        page = meus_filtros['pagina']
        per_page = meus_filtros['itens']
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
 
        resultado_hotel = [hotel.json() for hotel in pagination.items]
 
        return {
            "hotéis": resultado_hotel,
            "quantidade de itens": pagination.total,
            "quantidade de paginas": pagination.pages,
            "pagina atual": page
        }

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
    argumentos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank.")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404
    
    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel_id '{}' already exists.".format(hotel_id)}, 400
        
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500
        return hotel.json()
    
    @jwt_required()
    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500
        return hotel.json(), 201
        
        
    @jwt_required()
    def delete(self, hotel_id):
       hotel = HotelModel.find_hotel(hotel_id)
       if hotel:
           try:
               hotel.delete_hotel()
           except:
               return {'message': 'An error occured trying to delete hotel.'}, 500
           return {'mensage': 'Hotel deleted.'}
       return{'message': 'Hotel not found.'}, 404