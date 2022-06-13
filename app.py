#from importlib.resources import path
from flask import Flask, render_template, request
import network_automation
import csv
from pathlib import Path
downloads_path = str(Path.home() / "Downloads")
filepath = downloads_path.replace('file:///', 'file://')

#username = admin
#password = admin

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ip_addresses_list = request.form['ip_addresses_list']
        ip_addresses_list = network_automation.string_to_list(ip_addresses_list)

        with open(f'{downloads_path}\911_requirements.csv', 'w', newline='') as csvfile:
            fieldnames = ['hostname', 'ip_address', 'snmp_location']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for ip in ip_addresses_list:
                device = network_automation.get_device_info(username, password, ip)
                writer.writerow({'hostname': device['hostname'], 
                                 'ip_address': device['ip_address'],
                                 'snmp_location': device['snmp_location']})
  
        if username == '' or password == '' or ip_addresses_list == '':
            return render_template('index.html', message='Please enter required fields')
        return render_template('success.html', filepath = filepath)

if __name__ == '__main__':
    #app.debug = True
    app.run()