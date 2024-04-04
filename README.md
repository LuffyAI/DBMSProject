Programming Languages Version Details:
npm 9.5.1
node v18.6.0
Python 3.10.12
pip 22.0.2 

Ports:
- The Flask server uses port 5000
- The ReactJS server uses port 3000

Information:
- In reactfrontend/package.json, the proxy line effectively links the frontend to the backend.
- By setting secure as false, it works. 

To install the requirements
- On Linux, run pip3 install -r requirements.txt in root directory
- Navigate to reactfrontend and run 'npm install'

To run the application
1) First, launch the frontend. Do npm start in the root directory of reactfrontend. 
2) Second, from the FlaskBackend directory, do python3 server.py




