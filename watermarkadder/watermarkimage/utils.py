import glob
import os
import urllib
from datetime import datetime

import boto3

from PIL import Image as img

from .enums import AWS_ID, AWS_SECRET


def delete_all_temp_files():
    files = glob.glob('watermarkimage/static/temp_files/*')
    for f in files:
        os.remove(f)


def add_watermark_to_image(image_link):
    logo_path = "watermarkimage/static/logos/wokelo_logo.png"

    unique_stamp = int(datetime.now().timestamp() * 1000000)

    input_path = f"watermarkimage/static/temp_files/input_image_{unique_stamp}.png"
    abs_input_path = os.path.abspath(input_path)
    abs_logo_path = os.path.abspath(logo_path)

    urllib.request.urlretrieve(image_link, abs_input_path)
    image = img.open(abs_input_path)
    logo = img.open(abs_logo_path)
    output_path = f"watermarkimage/static/temp_files/output_image_{unique_stamp}.png"
    abs_output_path = os.path.abspath(output_path)

    image_width, image_height = image.size
    # resize the logo to a suitable size (e.g., 100x100)
    logo_width, logo_height = logo.size
    logo_size = (int(image_width * (10 / 100)), int(image_height * (10 / 100)))
    logo = logo.resize(logo_size)

    # calculate the position to place the logo in the top right corner
    logo_x = image_width - int(image_width * (1 / 100)) - logo_width
    logo_y = int(image_height * (5 / 100))

    # paste the logo onto the image
    image.paste(logo, (logo_x, logo_y), mask=logo)

    # dave the modified image
    image.save(abs_output_path)

    # upload output image to server and return the link
    output_image_file = open(abs_output_path, "rb")
    s3_upload_path = f"edited_images/output_image_{unique_stamp}.png"
    output_image_link = upload_file_to_S3(output_image_file,
                                          "wokelo-edited-images", s3_upload_path)

    # delete the temp files
    delete_all_temp_files()
    return output_image_link


def upload_file_to_S3(file, bucket_name, upload_path, content_type="image/png"):
    fileobj = file
    client = boto3.client('s3', aws_access_key_id=AWS_ID, aws_secret_access_key=AWS_SECRET)
    try:
        extra_args = {}
        if content_type:
            extra_args = {'ContentType': content_type}
        client.upload_fileobj(fileobj, bucket_name, upload_path, ExtraArgs=extra_args)
    except Exception as e:
        return ""

    return f"https://{bucket_name}.s3.amazonaws.com/{upload_path}"

