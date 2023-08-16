apt install python3-pip
pip install flask
pip install flask_cors
pip install scikit-image
apt-get update && apt-get install -y python3-opencv
pip install opencv-python
pip install pandas
pip install matplotlib

to start app in EC2
==================
pip3 install gunicorn
nohup gunicorn -b 0.0.0.0:8000 app:app

