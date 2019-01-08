from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse, abort
import _thread
import serial 

app = Flask( __name__ )
api = Api(app)
connection = serial.Serial( '/dev/ttyUSB0', 9600 )

#actual_stage = { "stage": [ 0 for x in range( 1, 386 ) ] }
#print(actual_scene)
json_data = {
    "type":"single",
    "scenes": [
        [ 0 for x in range ( 1, 386 ) ]
    ]

}
actual_scene = 0

class GetStage( Resource ):
    def get( self ):
        return json_data[ "scenes" ][ actual_scene ]

class UpdateStage( Resource ):
    def post ( self ):
        json_data = request.get_json( force = True )

api.add_resource( GetStage, '/getstage' )
api.add_resource( UpdateStage, '/updatestage' )

def arduinoUpdate():
    while True:
        if json_data[ "type" ] == "single":
            i = 385
            while i:
                connection.write( bytearray( i ) )
                connection.write( bytearray( json_data[ "scenes" ][ 0 ][ i ] ) )
                i -= 1
        
        if json_data[ "type" ] == "anim":
            
            continue 


if __name__ == '__main__':
    _thread.start_new_thread(arduinoUpdate, ())
    app.run( host='0.0.0.0' )

#flask, flask_restful, pyserial