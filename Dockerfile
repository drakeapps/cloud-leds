FROM balenalib/raspberrypi3:buster

# we should probably base this on the balena python image
# i've had issues with it, so we can do it manually
RUN apt-get update && apt-get install -y \
	python3 python3-pip python3-dev build-essential

# copy the files
COPY . /code/
WORKDIR /code

# requirements
RUN pip3 install -r requirements.txt


CMD python3 test.py

