"""
qr_generator.py contains QRGenerator class for generating QR code.
"""

import qrcode
import os
import json

# qrcode generator config
QRCODE_VERSION = 1
QRCODE_BOX_SIZE = 10
QRCODE_BORDER = 4

class QRGenerator:
    """
    Class to generate QR code image containing engineer's profile.
    """

    @staticmethod
    def generate(payload):
        """
        Generate QR code image containing payload and save locally.

        :param payload: engineer's profile
        :type payload: dict
        """
        # initialise qr code generator
        qr = qrcode.QRCode(
            version=QRCODE_VERSION,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=QRCODE_BOX_SIZE,
            border=QRCODE_BORDER,
        )
        # add qr code content
        qr.add_data(json.dumps(payload))
        qr.make(fit=True)
        # generate qr image
        qr_image = qr.make_image()
        # save qr image into a static dir
        directory = "src/MasterCSS/static/qr/{}".format(
                    payload['Username'])
        if not os.path.exists(directory):
            os.makedirs(directory)
        qr_image.save("{}/{}.jpg".format(directory, payload['Username']))
