import io
from io import BytesIO

import qrcode
from barcode import Code128
from barcode.writer import ImageWriter
from flask import Response, request, make_response
from flask_restful import Resource

class BarcodeResource(Resource):
    def get(self):
        user_id = request.args.get("user_id")
        img = qrcode.make(user_id)

        # save QR code image to memory buffer
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        # create Flask response object
        response = make_response(img_buffer.getvalue())
        response.headers['Content-Type'] = 'image/png'
        return response
