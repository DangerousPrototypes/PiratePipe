# Shell script to install Bus Pirate firmware auto-build under linux
# Assumes logged in as root or do 'su' first
# The instructions are presented in the format of a shell script, but you should really run each step manually!
# Tested under Ubuntu 14.04 LTS 64bit

cd ~

# Install Python 3.x
apt-get install python3

# Install Python PIP 3.x
apt-get install python3-pip

# Install Python modules
pip3 install requests pprint

# Download the latest autobuild script, example config, and daemon
wget https://raw.githubusercontent.com/DangerousPrototypes/PiratePipe/master/buildv2.py
wget https://raw.githubusercontent.com/DangerousPrototypes/PiratePipe/master/buildv2_tasks_example.py
wget https://raw.githubusercontent.com/DangerousPrototypes/PiratePipe/master/bp-buildv2.init.d

# Copy the configuration file
cp buildv2_tasks_example.py buildv2_tasks.py

# Edit the build configuration file
nano buildv2_tasks.py

# Add build jobs to the tasks configuration file:
#
# 'hardware'/'firmware':
# 	Hardware/Firmware version id. This is returned in the result json as 'hardware'/'firmware'. Used to support multiple builds, use as needed.
#
# 'work_dir':
#	Where to execute git and make commands. '/root/armdev/bus_pirate_ng/source' or '/root/picdev/Bus_Pirate/Firmware/busPirate3X.X'
#
# 'make_command':
#	Make command for this task. For example 'make bin' (ARM) or 'make' (PIC)
#
# 'output_dir':
#	Firmware output directory. For example '/root/armdev/bus_pirate_ng/source' or '/root/picdev/Bus_Pirate/Firmware/busPirate3X.X/dist/default/production'
#
# 'output_file':
#	Name of firmware file in output_dir. For example 'buspirateNG.bin' or 'busPirate3X.X.production.hex'
#
# 'api_url','api_key':
#	URL to POST results JSON file. 'api_key' is included for authentication. Backend stuff depends on your implementation.


# Test the build script

# Copy the daemon to the /etc/init.d folder. The build server will start automatically with linux.

# Customize the file paths in the daemon

# Start the daemon

# Stop the daemon

# Command line options
# root@demoautomakesetup:~# python3 buildv2.py --help
#
# usage: buildv2.py [-h] [--tasks TASKS] [--interval INTERVAL] [--test TEST]
# Dangerous Prototypes auto build v2.0
# optional arguments:
# -h, --help           show this help message and exit
# --tasks TASKS        Build tasks configuration file (default: buildv2_tasks.py)
# --interval INTERVAL  Repeat interval in minutes (default: 10)
# --test=true          Run in test mode, force uploads even if no new commits (default false)
# root@demoautomakesetup:~# 
