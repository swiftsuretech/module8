import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<img src=\"https://www.nvidia.com/content/dam/en-zz/Solutions/about-nvidia/logo-and-brand/01-nvidia-logo-horiz-500x200-2c50-d@2x.png\" alt=\"NVIDIA Logo\" style=\"width: 300px; height: auto;\">"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Lab 4: BCM 11 - Credentials & Access\n",
    "\n",
    "## Lab Overview\n",
    "\n",
    "### Audience\n",
    "This workbook is intended for technical training students, specifically system administrators for Base Command Manager.\n",
    "\n",
    "### Objectives\n",
    "In this module, you will:\n",
    "* Access the NVIDIA Launchpad Lab Environment\n",
    "* Connect to the BCM Head Node via SSH and VNC\n",
    "* Review Cluster Node Information\n",
    "\n",
    "### Prerequisites\n",
    "There are no prerequisites for this lab."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Practice 1: Lab Access and Credentials\n",
    "\n",
    "This section covers the methods to access the Base Command Manager environment."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 1: NVIDIA Launchpad Lab Access\n",
    "\n",
    "The lab environment is available through the NVIDIA Launchpad platform using Apache Guacamole.\n",
    "\n",
    "1. **Enter the portal using this URL:**\n",
    "   [Launchpad Guacamole Access](https://nvworkshop:Welcome123@f1e3f9dc-f87b-8382-abafe82a6819142f.nvidialaunchpad.com/guacamole)\n",
    "\n",
    "2. You should be forwarded to the screen below. Your instructor will provide the username and password for your specific environment."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 2: Connecting to Base Command Manager Head Node\n",
    "\n",
    "#### Option A: SSH to BCM Head Node\n",
    "To connect to the BCM head-node directly through SSH:\n",
    "1. Click on **Training-0X-Head-01 (SSH)**.\n",
    "2. Use the provided credentials:\n",
    "   * **Username:** `root`\n",
    "   * **Password:** `bcm123`\n",
    "\n",
    "#### Option B: Connecting via GUI (VNC)\n",
    "To connect to the admin node using VNC:\n",
    "1. Click on **Training-XX-Admin-01 (VNC)**. You will be forwarded to the VM desktop.\n",
    "2. Open the Google Chrome browser."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 3: Base View Access\n",
    "\n",
    "From the Admin Node browser, enter the corresponding URL of the Base View app for your assigned environment:\n",
    "\n",
    "| Environment | Head Node IP | Base View URL |\n",
    "|---|---|---|\n",
    "| Training-01 | 172.16.0.105 | https://172.16.0.105:8081/base-view |\n",
    "| Training-02 | 172.16.0.219 | https://172.16.0.219:8081/base-view |\n",
    "| Training-03 | 172.16.0.102 | https://172.16.0.102:8081/base-view |\n",
    "| Training-04 | 172.16.0.192 | https://172.16.0.192:8081/base-view |\n",
    "| Training-05 | 172.16.0.109 | https://172.16.0.109:8081/base-view |\n",
    "| Training-06 | 172.16.0.152 | https://172.16.0.152:8081/base-view |\n",
    "| Training-07 | 172.16.0.137 | https://172.16.0.137:8081/base-view |\n",
    "| Training-08 | 172.16.0.176 | https://172.16.0.176:8081/base-view |\n",
    "| Training-09 | 172.16.0.156 | https://172.16.0.156:8081/base-view |\n",
    "| Training-10 | 172.16.0.186 | https://172.16.0.186:8081/base-view |\n",
    "| Training-11 | 172.16.0.136 | https://172.16.0.136:8081/base-view |\n",
    "| Training-12 | 172.16.0.154 | https://172.16.0.154:8081/base-view |\n",
    "| Training-13 | 172.16.0.206 | https://172.16.0.206:8081/base-view |\n",
    "| Training-14 | 172.16.0.141 | https://172.16.0.141:8081/base-view |\n",
    "| Training-15 | 172.16.0.214 | https://172.16.0.214:8081/base-view |\n",
    "| Training-16 | 172.16.0.139 | https://172.16.0.139:8081/base-view |\n",
    "| Training-17 | 172.16.0.173 | https://172.16.0.173:8081/base-view |\n",
    "| Training-18 | 172.16.0.119 | https://172.16.0.119:8081/base-view |\n",
    "| Training-19 | 172.16.0.138 | https://172.16.0.138:8081/base-view |\n",
    "| Training-20 | 172.16.0.108 | https://172.16.0.108:8081/base-view |\n",
    "\n",
    "**Default Credentials for Base View & Head Node:**\n",
    "* **Username:** `root`\n",
    "* **Password:** `bcm123`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 4: Cluster Node Information\n",
    "\n",
    "Reference the following MAC addresses for the cluster nodes:\n",
    "\n",
    "| Node | MAC Address |\n",
    "|---|---|\n",
    "| node001 | 4E:56:44:41:01:01 |\n",
    "| node002 | 4E:56:44:41:01:02 |\n",
    "| node003 | 4E:56:44:41:01:03 |\n",
    "| node004 | 4E:56:44:41:01:04 |"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Verify connectivity (Optional)\n",
    "# You can use this cell to ping the head node if you are in the correct network environment.\n",
    "# !ping -c 4 172.16.0.105"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

with open('Lab 4 - BCM 11.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)

