This documentation will guide you to deploy your pre-existing flask app on a remote Ubuntu 20.04 Server.

## Step 1: Connect to the remote server via SSH

Open Windows Terminal and enter the following command
  ``` shell
  $ ssh <username>@<IP_address>
  ```

Replace <username> with your Ubuntu server username and <IP_address> with the server's IP Address.
For Example:
``` shell
$ ssh ubuntu@172.15.3.94
```

## Step 2: Update the Ubuntu System
Enter the following command:
``` shell
$ sudo apt update && sudo apt upgrade
```

## Step 3: Install the required software
Install Python, pip, Nginx, and set-up a virtual environment

``` bash
$ sudo apt install python3 python3-pip python3-venv nginx
```

> [!NOTE] Note: The following versions have been used and confirmed to work
> Ubuntu: 20.04.6 LTS
> Kernel: 5.4.0-156
> Python: 3.8.10
> Flask: 2.3.2
> gunicorn: 21.2.0
> pip: 20.0.2

The versions of applications used are as follows

## Step 4: Set Up your Flask App on the Server
- Since this is a small API, we could set-up the app by copying the code from our python file and pasting it on the server.
- The directory structure of the app is:
  ``` markdown
  ├── python-apis
  │   ├── app.py
  ```
- To replicate the structure, make a folder called `python-apis`:
  ``` shell
  $ mkdir python-apis
  ```
- Make the required python files inside the directory:
  ``` shell
  $ cd python-apis
  $ touch app.py
  ```
- Copy the contents of app.py from your machine to the remote server.
  ``` python
  from flask import Flask, request, jsonify
  app = Flask(__name__)

	@app.route('/add', methods=['POST'])
	def add_nums():
	    try:
	        data =  request.get_json()
	        num1 = data['num1']
	        num2 = data['num2']
	        result = num1 + num2
	        return jsonify({'result': result})
	    except KeyError:
	        return jsonify({"error": "Invalid input."})
	
	@app.route('/subtract', methods=['POST'])
	def subtract_numbers():
	    data = request.get_json()
	    num1 = data['num1']
	    num2 = data['num2']
	    result = num1 - num2
	    return jsonify({'result': result})
	
	if __name__ == "__main__":
	    app.run(host='0.0.0.0', debug=True, port=8989)
  ```

## Step 5: Create and Activate the Python Virtual Environment
``` bash
$ python3 -m venv venv
$ source venv/bin/activate
```
Your python virtual environment should now be active, indicated by `(venv)` before your prompt on the server.
Example:
``` bash
(venv) ubuntutest@ubuntu:~/python-apis$
```

## Step 6: Install the required dependencies
``` bash
$ pip install Flask gunicorn
```

## Step 7: Test Gunicorn
Test that your Flask app works using gunicorn:
``` bash
$ ./venv/bin/gunicorn --bind 0.0.0.0:8989 -w 3 app:app
```
Here, the first `app` corresponds to the filename `app.py` and the second `app` corresponds to the `app` module inside `app.py`. Hence, make sure to change the names accordingly.

<div style="page-break-after: always;"></div>

> [!warning] Warning
> Check the port number in the command. Use the same port as you have specified in the Flask App. In this case, the port number is 8989.

## Step 8: Configure Gunicorn systemd service
This step runs the gunicorn command in the background whenever the system is started. So the API is always served and accessible.
You may use your editor of choice instead of nano.

``` bash
$ sudo nano /etc/systemd/system/python-apis.service
```
Add the following content:
``` 
[Unit]
Description=Gunicorn instance to serve your Flask app
After=network.target

[Service]
User=<username>
Group=www-data
WorkingDirectory=/home/<username>/python-apis
ExecStart=/home/<username>/python-apis/./venv/bin/gunicorn --bind 0.0.0.0:8989 -w 3 app:app

[Install]
WantedBy=multi-user.target
```

> [!Attention] Attention
> Replace the username with your ubuntu server username. Make sure to use the gunicorn from the virtual environment and not from your ubuntu installation (if exists). 
> The working directory is the root directory of your Flask App.

Save and close the file.

## Step 9: Configure Nginx
Create an Nginx server block configuration file:
``` bash
$ sudo nano /etc/nginx/sites-available/python-apis
```
Add the following content:
``` nginx
server {
    listen 80;
    server_name your_server_domain_or_ip;

    location / {
        include proxy_params;
        proxy_pass http://your_server_ip:8000;
    }
}
```
Replace `your_server_domain_or_ip` and `your_server_ip` and port number accordingly.

Create a symbolic link to enable the configuration:
``` bash
$ sudo ln -s /etc/nginx/sites-available/python-apis /etc/nginx/sites-enabled
```

Test the Nginx configuration:

``` bash
$ sudo nginx -t
```

Restart Nginx to apply the changes:
``` bash
$ sudo systemctl restart nginx
```

## Step 10: Start Gunicorn Service
Start and enable the Gunicorn systemd service:
``` bash
$ sudo systemctl start python-apis
$ sudo systemctl enable python-apis
```

> [!NOTE] Note
> Make sure the service is up and running by using the following command:
> ``` bash
> $ sudo systemctl status python-apis
> ```
> The output will look something like this:
> ![[Pasted image 20230818113035.png]]
> If the service is not active, return to previous steps and make sure that all the steps have been followed properly.

## Step 11: Adjust the firewall Settings
Allow Nginx on UFW:
``` bash
$ sudo ufw allow 'Nginx Full'
```

## Step 12: Access Your Flask App via Postman
Send an appropriate request via Postman to your API and make sure it returns the appropriate response to confirm that it works.
Example:
![[Pasted image 20230818113551.png]]

To send the query as JSON, Click on `Body -> raw -> Text` and change it to JSON. Send your query.
For Example, for our API:
``` JSON
{
  "num1": 87,
  "num2": 789
}
```
If the response is not received, try disabling the firewall (consider safety requirements before doing so) and then try sending the query via Postman again.
``` bash
$ sudo systemctl disable ufw.service
```
If this works, enable the firewall service and then enable the appropriate ports and try again.

Make sure an appropriate response is received as shown in screenshot.

## Conclusion

Congratulations! You've successfully deployed your Flask app on a remote Ubuntu server using Nginx as a reverse proxy and Gunicorn as the application server.
