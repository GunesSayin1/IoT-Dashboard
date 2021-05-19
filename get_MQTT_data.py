#!/usr/bin/env python
import paho.mqtt.client as mqtt
import odev
import sqlite3
import subprocess
import sys
import os
MQTT_ADDRESS = '192.168.43.188'
MQTT_TOPIC = 'iot/measurements'
DATABASE_FILE = '12312.db'

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)
   

def on_message(client, userdata, message):
    payload=message.payload.decode('utf-8')
    decrypted = odev.decrypt(payload)
    db_conn = userdata['db_conn']
    sql = 'INSERT INTO sensors_data (topic, payload,rasptstamp) VALUES (?, ?,strftime("%Y-%m-%d %H:%M:%S","now","localtime"))'
    cursor = db_conn.cursor()
    cursor.execute(sql, (decrypted[3], decrypted[0]))
    cursor.execute(sql, (decrypted[4], decrypted[1]))
    cursor.execute(sql, (decrypted[5], decrypted[2]))
    db_conn.commit()
    cursor.close()
    # subprocess.call('python C:\\Users\Gunes\\Documents\\IoT_Project_Pi\\get_MQTT_data.py')
    # run("python " + "C:\\Users\\Gunes\\Documents\\IoT_Project_Pi\\get_MQTT_data.py", check=True)
    # subprocess.call(sys.executable + ' "' + os.path.realpath(__file__) + '"')
    os.execv(__file__, sys.argv)
    return decrypted





def main():
    client=mqtt.Client()
    client.username_pw_set(username="gunes", password="123asdss")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_ADDRESS, 1883)
    db_conn = sqlite3.connect(DATABASE_FILE)
    db_conn.text_factory = str
    client.user_data_set({'db_conn': db_conn})
    client.loop_forever()


if __name__ == '__main__':
    main()

