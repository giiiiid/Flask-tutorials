import os
import secrets
from PIL import Image
from flask_mail import Message
from flaskblog import mail, app


def save_picture(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/propic', image_fn)

    output_size = (125, 125)
    i = Image.open(form_image)
    i.resize(output_size)
    i.save(image_path)

    return image_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        subject='Password Reset request',
        recipients=[user.email],
        sender='noreply@gmail.com',
    )
    msg.body = f'''
    To reset your password, visit the following link: 
    {url_for('reset_pwd_token', token=token, _external=True)}

    If you did not request to reset your password, kindly ignore this email.
    '''
    mail.send(msg)
