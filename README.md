# Home Automation
## Background
I started out on my home automation journey in the summer of 2019. I attended a short presentation by a colleague where he was presenting how he was using Home Assistant. I was intrigued by what I saw and decided to to look into it for our own purposes.

Since then I have expanded out from just Home Assistant. I have learnt how to integrate ESP8266 embedded devices (Smart Pugs and Relays) with MQTT - this then exposes these as entities and sensors in Home Assistant. I have also discovered how to use Zigbee devices from almost any manufacturer with Home Assistant. Lately I have now also integrated my House Solar and Battery control system into Home Assistant.

My current vision is to ensue that I make best and most economical use of electricity. I receive my energy from Octopus and the two plans that I have tried are Octopus Go (5p per kWh between 00.30-04.30) and Agile. Both of these are Time of Use Tariff's (ToU) and with Agile the also offer an export plan that varies in price too. By combining the sensor data and control data from Home Assistant with usage and price data from Octopus I hope to be able to set automatic and variable charging cycles for both the House Battery and our Nissan Leaf too.

What I hope to do on this Github site is to share what I have done along with the code and config snippets so others can experiment too.

## Acknowledgements
99% of what I have been able to build would not have been possible if it wasn't for the work of others and by them sharing their knowledge and work. I hope to continue this culture of sharing my own ideas and work so that it may help others like me.  

## Overview
vvvvv

## Logical Integraiton View
Below is a diagram of the data flows and various platforms (internal and external that I). For each platform i will provide some explanation of what it does.