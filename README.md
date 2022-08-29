# Flaky Network Simulator

This repository is used to maintain the *flakynetworksimulator* package hosted on pypip.org.
> Version 0.0.3

# Problem Statement

```
There wasn't any technique to simulate real-life network conditions while testing a particular sync API. It is often observed that app crashes if there are frequent network drops or bad network conditions. The challenge faced by our team was that there didn't exist any textbook application to simulate actual life network conditions, like when we are traveling or when we are at home, but there are frequent switches between wifi and Mobile Data. 
```

# Installation

### Inside Adobe

    pip3 install https://git.corp.adobe.com/ACPLocal/flaky-network/tree/main/dist/flakynetworksimulator-0.0.3-py3-none-any.whl
  *You need VPN to install using above command* 

### Install from Pypip (Not functional as of now)

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



## Features

> When you define the FlakyNetwork object, you need to declare **DNS** and **Default Profile**
> By default `DNS= 8.8.8.8` & `Default Profile = MOBILE_DATA`
> Refer to implementation guidelines, **it is advised to implement the functions using multithreading**

|Function|  Params| Function |
|--|--|--|
| `throttle()` |tout = timeout | Throttle the network based on the default profile declared in object declaration
| `randomBandwidth()` | bw_var, tout | Varies the bandwidth withing the given % range of parameter 
| `networkSwitch()` | switch_profile, tout | Simulates network switches between specified profile and default profile |
| `normalVariation()` | jitter, bw_dev | Simulates the behaviour of a normally distributed bandwidth and ping
| `random()` | bw_deg, ping_deg | Simulates the behaviour of randomly distributed bandwidth and ping based on degree of flakiness
| `drops()` | dropout | Random network drop offs (% wise)
| `realWorldSimulation()` | tout | Simulates a travelling network for a specified time

## Default Params

|Param| Value  |
|--|--|
|SWITCH_PROFILE| `lte`
|MOBILE_DATA |`4g`
|TEST_DNS |`127.0.0.1`
|PING_DNS |`8.8.8.8`
|DROPOUT  |`0`
|BANDWIDTH_VAR |`0.2`
|PING_COUNT|`5`
|DEFAULT_MODE| `0`
|DEBUG_MODE | `False`
|TOUT | `120`
|JITTERVALUE | `10`
## Tech Stack

| MacOS | Windows | Linux
|--|--|--|
|Python | Python | Python
||C++| 

*Note: Currently python version is in production, windows is in progress and support for linux can be extended if required*

## Normal Variate Profile
![Normal variate Bandwidth](imglink.here)
![Normally Distributed Ping](imglink.here)

## Testing Locally
Follow the steps to test the *flaktnetworksimulator* locally by simulating network on localhost

 1. Create a file `run.py`
 2. Paste the following code for quickstart

    import  flakynetworksimulator.flakynetwork  as  f
    from time import sleep
    fn = f.FlakyNetwork()
    fn.test(mode = 0)
    sleep(10)
    fn.stop()
    

 3. Open a 2 terminals
 4. Run `ping 127.0.0.1` on terminal 1 and `sudo python3 run.py` in terminal 2
 5. Replace `fn.test()` with testing functions
 > Test functions are same as legacy function, just add Test to the function name 
 > For eg. `throttle()` has test function named `thorttleTest()`

# Contributing

Contributions are welcomed! Read the [Contributing Guide](https://git.corp.adobe.com/ACPLocal/flaky-network/blob/main/CONTRIBUTING.md) for more information.

# Licensing

This project is licensed under the MIT License. See [LICENSE](https://git.corp.adobe.com/ACPLocal/flaky-network/blob/main/LICENSE) for more information.