# Flaky Network Simulator

This repository is used to maintain the *flakynetworksimulator* package hosted on pypip.org.

# Installation

### Inside Adobe

    pip3 install https://git.corp.adobe.com/ACPLocal/flaky-network/tree/main/dist/flakynetworksimulator-0.0.3-py3-none-any.whl
  *You need VPN to install using above command* 

### Install from Pypip

    pip3 install flakynetworksimulator

  

# Quickstart

 1. Install *flakynetworksimulator* package
 2. Create *run.py* file
 3. Paste the following code in run.py file

	    import  flakynetworksimulator.flakynetwork  as  f
	    from time import sleep
	   	fn = f.FlakyNetwork()
	   	fn.start(mode = 0)
	   	sleep(10)
	   	fn.stop()
4. Start the terminal and run the following command `ping 8.8.8.8`
5. Run the python file using another terminal tab  `sudo python3 run.py`
6. Check the terminal 1 if the ping is changed or not
