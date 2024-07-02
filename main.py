import os
import random
import string
from flask import Flask, send_from_directory, url_for
import barcode
from barcode.writer import ImageWriter

class BarcodeAPI:
    def __init__(self, host: str = '0.0.0.0', port: int = 5000, domain: str = None) -> None:
        self.host = host
        self.port = port
        self.domain = domain
        self.app = Flask(__name__)
        self.setup_routes()
        self.images_dir = os.path.join(os.getcwd(), 'store', 'images')
        os.makedirs(self.images_dir, exist_ok=True)

    def setup_routes(self) -> None:
        self.app.add_url_rule('/barcode', 'get_barcode', self.get_barcode)
        self.app.add_url_rule('/barcodes/<filename>', 'serve_image', self.serve_image)

    def generate_random_number(self, length: int = 12) -> str:
        return ''.join(random.choices(string.digits, k=length))

    def create_barcode_image(self, number: str, filename: str) -> str:
        BARCODE = barcode.get_barcode_class('code128')
        barcode_obj = BARCODE(number, writer=ImageWriter())
        file_path = os.path.join(self.images_dir, filename)
        barcode_obj.save(file_path)
        return f'{file_path}.png'

    def get_barcode(self) -> str:
        number = self.generate_random_number()
        filename = f'barcode_{number}'
        image_path = self.create_barcode_image(number, filename)
        if self.domain:
            return f'http://{self.domain}/barcodes/{filename}.png'
        else:
            return url_for('serve_image', filename=f'{filename}.png', _external=True)

    def serve_image(self, filename: str):
        return send_from_directory(self.images_dir, filename)

    def run(self) -> None:
        self.app.run(host=self.host, port=self.port)

if __name__ == '__main__':
    api = BarcodeAPI(host='0.0.0.0', port=2084, domain='servers.ikubaysan.com:2084')
    api.run()
