## Overview

![Device in action](https://github.com/jrmedd/contactless-donation-prototype/blob/master/in_action.gif?raw=true)

In the world of UX development, testing new products can be difficult, particularly where transactions are involved, or where concepts are not yet fully developed. Rapid prototyping enables you to create functioning prototypes & simulations for these scenarios.

At [The Landing](http://www.thelanding.org.uk/) in [MediaCityUK](http://www.mediacityuk.co.uk/), home of Salford’s [Eagle Lab](http://www.thelanding.org.uk/spaces-services/eagle-labs/), we created a physical representation of a charitable donation device for user testing, devised by [Pingit](https://www.pingit.com/#!/). Since then we printed and programmed a device to simulate donations with contactless payment.

## Requirements

The application is underpinned by:

* [Flask](http://flask.pocoo.org/) – provides the URL patterns for posting card payments to the MongoDB server, and retrieving payment information.
* [SocketIO](https://socket.io/) (& [flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/)) to tell the app to display a notification upon succesful donations.
* [MongoDB](https://www.mongodb.com/) – for storing card holders and payments.

The hardware:

* [Raspberry Pi Zero W](https://www.raspberrypi.org/products/pi-zero-w/) – This runs a Python script to read the NFC cards (using SPI on the GPIO), spit out messages to trigger a response from the web app, and make HTTP requests to store information on the database.
* [PN532 NFC breakout from Adafruit](https://www.adafruit.com/product/364) – My office has tons of MiFare cards kicking around, which work great as dummy contactless cards with a bit of vinyl on them (see the hardware directory). I wire this up straight to the GPIO on the Pi ([Adafruit provide a good resource on wiring and library installation](https://learn.adafruit.com/raspberry-pi-nfc-minecraft-blocks/hardware-wiring))
* The case is a mix of 3D printing and laser cutting (photos later).

## Usage

* Install necessary libraries (including PN532, and requests libraries on the Pi). The same will go for the web app (flask-cors/socketio etc.)
* Put the Pi on the same network as the server, make sure the server's IP is updated in the hardware monitoring script on the Pi
* Check all of the IP address references throughout (includes **web_app.py** & **hardware_monitor.py**)
* Start Flask app (I use the development server for demos, you could always deploy using Gunicorn/nginx with a little tweaking, but it might not be worth it)
* Browse to the app on the device of your choosing
* Start script on the Pi.
