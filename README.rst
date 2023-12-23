OCP Cluster Login
=================

``ocp-cluster-login`` is a Python tool designed to facilitate the login
process to OpenShift clusters. It automates the web login flow using
Selenium, making it easier to handle authentication for OpenShift
clusters.

Features
--------

-  Automates OpenShift web login process.
-  Supports Chrome and Firefox web drivers.
-  Checks if a user is already logged in before attempting to log in again.
-  Handles timeouts and browser driver errors.

Prerequisites
-------------

Before you begin, ensure you have met the following requirements: -
Python 3.6 or higher. - Selenium installed. - Selenium WebDriver for
Chrome or Firefox.

Installation
------------

.. code:: bash

   pip install ocp-cluster-login

Usage
-----

.. code:: bash

   ocp-cluster-login [-h] [-s SERVER] [-k] [-t TIMEOUT] [-d {chrome,firefox}]

The tool supports several command line arguments to customize its behavior: 
- ``-s``, ``--server``: Specify the API server URL. Defaults to ``https://api.ocp.domain.com:6443``. 
- ``-k``, ``--insecure-skip-tls-verify``: Skip TLS verification if necessary. 
- ``-t``, ``--timeout``: Set the timeout for waiting for login in seconds. Default is 60 seconds. 
- ``-d``, ``--driver``: Choose the web driver. Supported drivers are ``chrome`` and ``firefox``. Default is ``chrome``.

Contributing
============

We welcome contributions to the OpenShift Interactive Login CLI Tool! If
you’d like to contribute, please follow the guidelines outlined in our
CONTRIBUTING.md file in the GitHub Repository.