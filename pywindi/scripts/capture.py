from pywindi.winclient import Winclient
from pywindi.scripts.config import config
import threading
import click
from time import sleep
from datetime import datetime
import os

if os.path.exists('ccd_base_config.txt'):
    print(1)
    file = open('ccd_base_config.txt', 'r')
else:
    print(2)
    config('~/Desktop/images/', '(localhost:7624)')
    file = open('ccd_base_config.txt', 'r')

ccd_num, ccd_time, ccd_temp, ccd_bin, ccd_type = 1, 0.0, 0.0, (1.0, 1.0), 'light'
#: path where image is saved.
#image_path = file.readline()[:-1]
image_path = '/home/dimm/Desktop/images/'
#: list of hosts.
#addresses = file.readline()[1:-1].replace(' ', '').split(',')
addresses = ['localhost:7624']
clients = []
image_info = None

def add_address(host, port = 7624):
    addresses.append(host + ':' + str(port))


def delete_address(host, port = 7624):
    addresses.remove(host + ':' + str(port))


def add_clients():
    #: add all of the clients in client list.
    for a in addresses:
        host, port = a.split(':')
        client = Winclient(host, int(port))
        clients.append(client)


def take_image_with_one_client(client, time, temperature, binning, type, address):
    #: set the base properties.
    print('start capturing')
    try:
        ccd = client.get_device('SBIG CCD')
    except Exception as e:
        print(e)
        print('Couldn\'t connect to', address, 'server.')
        return
    ccd.configure(image_directory=image_path + str(address) + '/')
    print(image_path + str(address) + '/')
    ccd.set_binning(binning[0], binning[1])
    ccd.set_temperature(temperature)
    ccd.set_frame_type(type)
    image_info = (ccd.take_image(time), datetime.utcnow())

@click.command()
@click.option('--time', type=float, help='exposure time of image')
@click.option('--temperature', type=float, help='temperature of CCD for image')
@click.option('--binning', type=(float, float), help='binning of CCD for image')
@click.option('--interval', type=float, help='interval between images')
@click.option('--count', type=int, help='number of images to take')
@click.option('--type', type=str, help='type of image to take')
def capturer_cli(time, temperature, binning, interval, count, type):
    ccd_time, ccd_temp, ccd_bin, ccd_type = time, temperature, binning, type
    add_clients()
    for i in range(count):
        threads = []
        for enum, client in enumerate(clients):
            address = addresses[enum]
            t = threading.Thread(target=take_image_with_one_client, args=(client, ccd_time, ccd_temp, ccd_bin, ccd_type, address))
            threads.append(t)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        if not i == count - 1:
            print('Waiting', interval, 'seconds.')
            sleep(interval)
    file.close()


def capturer(time, temperature, binning, interval, count, type):
    '''ccd_time, ccd_temp, ccd_bin, ccd_type = time, temperature, binning, type
    add_clients()
    for i in range(count):
        threads = []
        for enum, client in enumerate(clients):
            address = addresses[enum]
            t = threading.Thread(target=take_image_with_one_client, args=(client, ccd_time, ccd_temp, ccd_bin, ccd_type, address))
            threads.append(t)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        if not i == count - 1:
            print('Waiting', interval, 'seconds.')
            sleep(interval)
        yield image_info
    file.close()'''
    ccd_time, ccd_temp, ccd_bin, ccd_type = time, temperature, binning, type
    add_clients()
    for i in range(count):
        threads = []
        for enum, client in enumerate(clients):
            address = addresses[enum]
            t = threading.Thread(target=take_image_with_one_client, args=(client, ccd_time, ccd_temp, ccd_bin, ccd_type, address))
            threads.append(t)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        if not i == count - 1:
            print('Waiting', interval, 'seconds.')
            sleep(interval)
    file.close()
