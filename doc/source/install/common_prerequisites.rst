Prerequisites
-------------

Before you install and configure the replace with the service it implements service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``apt_ostree`` database:

     .. code-block:: none

        CREATE DATABASE apt_ostree;

   * Grant proper access to the ``apt_ostree`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON apt_ostree.* TO 'apt_ostree'@'localhost' \
          IDENTIFIED BY 'APT_OSTREE_DBPASS';
        GRANT ALL PRIVILEGES ON apt_ostree.* TO 'apt_ostree'@'%' \
          IDENTIFIED BY 'APT_OSTREE_DBPASS';

     Replace ``APT_OSTREE_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``apt_ostree`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt apt_ostree

   * Add the ``admin`` role to the ``apt_ostree`` user:

     .. code-block:: console

        $ openstack role add --project service --user apt_ostree admin

   * Create the apt_ostree service entities:

     .. code-block:: console

        $ openstack service create --name apt_ostree --description "replace with the service it implements" replace with the service it implements

#. Create the replace with the service it implements service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        replace with the service it implements public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        replace with the service it implements internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        replace with the service it implements admin http://controller:XXXX/vY/%\(tenant_id\)s
