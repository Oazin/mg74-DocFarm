# Plant-Disease-Detection
This project is based on an existing repository for plant disease detection using deep learning. I have modified and extended it to suit my specific needs while preserving the core of the original work.

## Description
This model uses a Convolutional Neural Network (CNN) built with the PyTorch framework to classify leaf images into 39 different categories representing various plant diseases. The training was performed on the widely-used PlantVillage dataset.

## Original Source
This project is an adaptation of the original repository available here: [Link to the original repository](https://github.com/manthan89-py/Plant-Disease-Detection)

The original work was created by [manthan89-py](https://github.com/manthan89-py), whose foundational efforts I gratefully acknowledge. More information about the dataset can be found on the author’s blog (mentioned in the original repository).

## Modifications
* I use the original app to imprement the predication
* Form Telegram ChatBot, the users send picture of a leaves with disease
* The message is trigger in n8n (n8n_DocFarm.json)
* Then the picture is send to the API's endpoint '/upload-photo'
* The method associated to this endpoint use the predication model to find the disease
* The reponse content the title, the description of the disease, the prevention and a link to buy the supplement
* The user receive all this information

## Run Project in your Machine
* You must have **Python3.8** installed in your machine.
* Create a Python Virtual Environment & Activate Virtual Environment [Link](https://docs.python.org/3/tutorial/venv.html)
* Install all the dependencies using below command
    `pip install -r requirements.txt`
* Install Local Tunnel to allow the access of the app on n8n 
    `npm install -g localtunnel`
* Go to the `Flask Deployed App` folder.
* Start the tunnel using following command `lt --port 5000 --subdomain docfarm`
* Run the Flask app using below command `python3 app_v2.py`
* Other alternative : execute Run_DocFarm.exe
* Use the link https://docfarm.loca.lt to access the app
* You'll arrive on the original webapp. 
* Go to the endpoint "/docs" to access to the swagger UI and access to the API endpoint.

## Testing Images

* If you do not have leaf images then you can use test images located in test_images folder
* Each image has its corresponding disease name, so you can verify whether the model is working perfectly or not
