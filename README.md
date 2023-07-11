apt install python3-pip
pip install flask
pip install flask_cors
pip install scikit-image

to start app in EC2
==================
pip3 install gunicorn
nohup gunicorn -b 0.0.0.0:8000 app:app

