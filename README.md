Hello Jett for my assignment I decided to create a PyQt application to tailor the assignment to the job description.

Before the application can run correctly you will need to first create a SSH key pair using the "ssh-keygen -t rsa -b 4096" command in the main folder of the project
This will allow the Dockerfile to copy the public key to the ssh server and later the PyQt application can use the private key for authentication.

Next you will need to build the docker image using the "docker build -t ssh-image ." command
After creating the docker image you can run the docker container using the "docker run -d -p 2222:22 --name ssh-container -v ./python/my_app/img:/app/images" ssh-image"

Next assuming you have python installed you can create a virtual environment with the "python -m venv venv" command
and activating it with "source venv/bin/activate" for linux or mac and with "venv/Scripts/activate" for windows

While in the virtual environment you can use "pip install -r  requirements.txt" to install all necessary dependencies 

Next you can run the python program and to launch the application

You can drag and drop images to upload to the docker container that are saved in its volume so they persist even when stopped

And you can retrieve the last image you uploaded to the container.

