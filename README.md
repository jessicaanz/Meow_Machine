# Meow_Machine
Instructions and Code for the Meow Machine Robot for the Robot Studio course at Duke University

## Usage Instructions

### Accessing Raspberry Pi IP Address
Open the windows command prompt and run:

```
arp -a | findstr cd-a6-32
```

This will output the IP address and say if it is dynamic or static

### SSH Into the Raspberry Pi
From the command prompt run:

```
ssh ubuntu@"IP Address"
```

The default password is "Ubuntu", input that when prompted
