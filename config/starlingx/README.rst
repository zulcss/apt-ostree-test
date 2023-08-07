To build a StarlingX rootfs you have to do the following:

1. Build the StarlingX packages through the build environment.
2. Find the minikube profile that you are using: "minikube profile list".
3. Load the minikube profile "minikube profile <profile>".
4. Launch the minikube tunnel in another window: "minikube tunnel"
5. After the tunnel has been created, modify the hostname for "stx-debian-stx-repomgr"
   with the IP address of the host in your developer environment.

   echo "<IP address> stx-debian-stx-repomgr"  > /etc/hosts

6. Run the apt-ostree compose create command:

    sudo apt-ostree compose create --repo=<path to ostree repo> \
        --base config/starlingx/ <name of ostree branch>
