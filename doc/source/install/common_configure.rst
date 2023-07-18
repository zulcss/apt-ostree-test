2. Edit the ``/etc/apt_ostree/apt_ostree.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://apt_ostree:APT_OSTREE_DBPASS@controller/apt_ostree
