# tinylog_server

## Overview
Flask API for TinyLog

## Installation

### Development
This project makes use of virtual environments to provision your development environment. Once the following requirements have been met further installation is managed automatically by the Makefile.

Requirements before provisioning:
 * python3
 * pip3
 * virtualenv
 * make

### Production
To install use pip:
```
$> pip install tinylog_server
```
    
Requirements before installation:
 * python3
 * pip3
 
## Usage

### Development
The following commands will create a virtual environment (if not already present) for the application and will install the necessary dependencies there before running the requested command.

Run the package:
```
$> make
```
Run the unit tests:
```
$> make test
```
Run the linter: 
```
$> make lint
```

Rebuild your virtual environment:
```
$> make rebuild_venv
```
