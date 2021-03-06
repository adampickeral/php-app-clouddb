Description
===========

This cookbook is designed to be able to describe and deploy PHP web applications. Currently supported:

* PHP
* Apache2 with mod\_php

Note that this cookbook provides the PHP-specific bindings for the `application` cookbook; you will find general documentation in that cookbook.

Other application stacks may be supported at a later date.

Requirements
============

Chef 0.10.0 or higher required (for Chef environment use).

The following Opscode cookbooks are dependencies:

* application
* apache2
* php

Resources/Providers
==========

The LWRPs provided by this cookbook are not meant to be used by themselves; make sure you are familiar with the `application` cookbook before proceeding.

php
---

The `php` sub-resource LWRP deals with deploying PHP webapps from an SCM repository. It uses the `deploy_revision` LWRP to perform the bulk of its tasks, and many concepts and parameters map directly to it. Check the documentation for `deploy_revision` for more information.

PHP applications have no standard convention for database configuration; your application cookbook must provide a template if needed.

# Attribute Parameters

- packages: an Array of PEAR packages to install
- database\_master\_role: if a role name is provided, a Chef search will be run to find a node with than role in the same environment as the current role. If a node is found, its IP address will be used when rendering the context file, but see the "Database block parameters" section below
- local\_settings\_file: the name of the local settings file to be generated by template. Defaults to "LocalSettings.php"
- settings\_template: the name of template that will be rendered to create the local settings file. Defaults to "#{local\_settings\_file}.erb"
- database: a block containing additional parameters for configuring the database connection (see below)
- app\_root: path where the application can be found in relative from path. Default value is "/"

# Database block parameters

The database block can accept any method, which will result in an entry being created in the `@database` Hash which is passed to the context template. See the examples below for more information.

mod\_php\_apache2
-----------------

The `mod_php_apache2` sub-resource LWRP configures Apache and mod\_php to run the application by creating a virtual host.

# Attribute Parameters

- server\_aliases: an Array of server aliases
- webapp\_template: the template to render to create the virtual host configuration. Defaults to "php.conf.erb"

Usage
=====

A sample application that needs a database connection:

    application "phpvirtualbox" do
      path "/usr/local/www/sites/phpvirtualbox"
      owner node[:apache][:user]
      group node[:apache][:user]
      repository "..."
      deploy_key "..."
      revision "4_0_7"
      packages ["php-soap"]

      php do
        database_master_role "database_master"
        local_settings_file "config.php"
      end

      mod_php_apache2
    end

This will result in a `config.php` file getting created from a `config.php.erb` template that must exist in your application cookbook.

You can invoke any method on the database block:

    application "my-app" do
      path "/usr/local/my-app"
      repository "..."
      revision "..."

      php do
        database_master_role "database_master"
        database do
          database 'name'
          quorum 2
          replicas %w[Huey Dewey Louie]
        end
      end
    end

The corresponding entries will be passed to the context template:

    <%= @database['quorum']
    <%= @database['replicas'].join(',') %>

License and Author
==================

Author:: Adam Jacob (<adam@opscode.com>)
Author:: Andrea Campi (<andrea.campi@zephirworks.com.com>)
Author:: Joshua Timberman (<joshua@opscode.com>)
Author:: Seth Chisamore (<schisamo@opscode.com>)

Copyright 2009-2012, Opscode, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
