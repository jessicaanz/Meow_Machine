# Meow_Machine
Instructions and Code for the Meow Machine Robot for the Robot Studio course at Duke University

## Usage Instructions

### Accessing Raspberry Pi IP Address
Boot up the Raspberry pi while connected to a monitor and run

```
hostname -I
```

This will output the IP address

### SSH Into the Raspberry Pi
From the command prompt run:

```
ssh jessica@"IP Address"
```

Input the password when prompted

### Creating a Virtual Python Enviroment
Run
```
python3 -m venv .venv  
```
```
source .venv/bin/activate    
```
```
sudo usermod -a -G tty jessica
```
```
sudo usermod -a -G dialout jessica
```
