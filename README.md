# vision
借鉴Scrapy基础架构实现的一种数据处理框架


Set Up
------------

1. Fork this repository on GitHub.
2. Clone *your forked repository* (not our original one) to your hard drive with `https://github.com/GuangTianLi/vision.git`
3. `cd vision`
4. Install with pip `pip install .`

Tutorial
------------

In this tutorial, make sure you installed the vision.

This tutorial will walk you through these tasks:

- [1 Creating a project](#1-creating-a-project)
- [2 Our first Data Report](#2-our-first-data-report)
- [3 How to run our data report](#3-how-to-run-our-data-report)
- [4 Vision Server](#4-vision-server)
    - [4.1 Communication Protocol](#4.1-communication-protocol)
        - [Request format](#request-format)
        - [Response format](#response-format)
    - [4.2 How to run our vision server](#4.2-how-to-run-our-vision-server)
- [5 Settings](#5-settings)
    - [5.1 Designating the settings](#5.1-designating-the-settings)
    - [5.2 Populating the settings](#5.2-populating-the-settings)
        - [5.2.1 Command line options](#5.2.1-command-line-options)
        - [5.2.2 Settings per-datareport](#5.2.2-settings-per-datareport)
        - [5.2.3 Project settings module](#5.2.3-project-settings-module)
        - [5.2.4 Default global settings](#5.2.4-default-global-settings)
    - [5.3 How to access settings](#5.3-how-to-access-settings)
    - [5.4 Built-in settings reference](#5.4-built-in-settings-reference)
        
## 1 Creating a project

Before you start scraping, you will have to set up a new Scrapy project. Enter a directory where you’d like to store your code and run:

`vision startproject tutorial`

This will create a **tutorial** directory with the following contents:

```
tutorial/
    vision.cfg            # deploy configuration file
    tutorial/             # project's Python module, you'll import your code from here
        settings.py       # project settings file
        data_report_file/ # a directory where the data report's files will save
        data_report/      # a directory where you'll later put your data reports
```

## 2 Our first Data Report

Data reports are classes that you define and that Vision uses to create and send file from a set of data.They must subclass vision.DataReport and define how to get data from databases.

This is the code for our first Data Report. Save it in a file named tutorial.py under the tutorial/data_report directory in your project:

```python
# -*- coding: utf-8 -*-

import vision
 
 
class TutorialDataReport(vision.DataReport):
    name = "tutorial"
 
    def make_data_from_db(self):
        """
        Fetch financing event in a period of time from DB.
        Returns
        -------
        data [list]: list of dict
        """
        data = get_your_data()
        yield data
```

            
As you can see, our Data reports subclasses vision.DataReport and defines some attributes and methods:

* name: identifies the Data Report. It must be unique within a project, that is, you can’t set the same name for different Data Report.
* make_data_from_db(): a method that will be called to create the file and must return an iterable of list and list of dict.
    * The data must have the format like this: (fields, content)
        * fields is a list like this:`[column1, column2,....., columnN]`
        * content is a list of dictionary like this:`[{column1:value1, column2:value2, ...., columnN:valueN}, .......]`
       
## 3 How to run our data report

To put our data report to work, go to the project’s top level directory and run:

`vision create tutorial`

## 4 Vision Server

The vision server communicate with other process through socket. You can configure socket by settings module

### 4.1 Communication Protocol

The vision server uses json formatted text as the client and server communication protocol.

#### Request format

```json
{
  'data_report_name': '', // your data report name
  'file_name': '', // if your raw data is from file
  'dont_archive': '' //Default False
  'data_report_add': '' // All produced files will be compressed in here
}
```

#### Response format


```json
{
  'result': '' // The file address, if there is no error
}
```

### 4.2 How to run our vision server

To start our server to work, go to the project’s top level directory and run:

`vision server --start`

## 5 Settings

The Vision settings allows you to customize the behaviour of all Vision components, including the core, create, send, server and data reports themselves.

The infrastructure of the settings provides a global namespace of key-value mappings that the code can use to pull configuration values from. The settings can be populated through different mechanisms, which are described below.

The settings are also the mechanism for selecting the currently active Vision project (in case you have many).

### 5.1 Designating the settings
When you use Vision, you have to tell it which settings you’re using. You can do this by using an environment variable, VISION_SETTINGS_MODULE.

The value of VISION_SETTINGS_MODULE should be in Python path syntax, e.g. myproject.settings. or import your vision.cfg in you project by Vision.

### 5.2 Populating the settings
Settings can be populated using different mechanisms, each of which having a different precedence. Here is the list of them in decreasing order of precedence:

    1. Command line options (most precedence)
    2. Settings per-spider
    3. Project settings module
    4. Default settings per-command
    5. Default global settings (less precedence)
    
The population of these settings sources is taken care of internally, but a manual handling is possible using API calls. 
```python
classs vision.settings.BaseSettings.set(name, value, priority='project')
"""
Store a key/value attribute with a given priority.
Settings should be populated before configuring the DataReportCenter object (through the configure() method), 
otherwise they won’t have any effect.
    
Parameters
----------
name (string) – the setting name
value (any) – the value to associate with the setting

"""
```

#### 5.2.1 Command line options

Arguments provided by the command line are the ones that take most precedence, overriding any other options. You can explicitly override one (or more) settings using the -s (or --set) command line option.

Example:

`vision mydatareport -s LOG_FILE=vision.log`

#### 5.2.2 Settings per-datareport

DaraReports can define their own settings that will take precedence and override the project ones. They can do so by setting their custom_settings attribute:

```python
# -*- coding: utf-8 -*-
 
import vision
 
 
class TutorialDataReport(vision.DataReport):
    name = "mydatareport"
    custom_settings = {
        'SOME_SETTING': 'some value',
    }
```

#### 5.2.3 Project settings module

The project settings module is the standard configuration file for your Vision project, it’s where most of your custom settings will be populated. 

For a standard Vision project, this means you’ll be adding or changing the settings in the settings.py file created for your project.
#### 5.2.4 Default global settings

The global defaults are located in the vision.settings.default_settings module.

### 5.3 How to access settings

In a date report, the settings are available through self.settings:

```python
class TutorialDataReport(vision.DataReport):
    name = "mydatareport"
 
    def make_data_from_db(self):
        print("Existing settings: %s" % self.settings.attributes.keys())
```

### 5.4 Built-in settings reference
Here’s a list of all available Vision settings, in alphabetical order, along with their default values and the scope where they apply.

The scope, where available, shows where the setting is being used, if it’s tied to any particular component. In that case the module of that component will be shown, typically an extension, middleware or pipeline.

It also means that the component must be enabled in order for the setting to have any effect.

DATA_REPORT_MODULES
Default: data_report_center.data_report

This is a model where datareport is.

SVG_FILE
Default: False

It determines whether to create svg file.If it is True,you must define the key if x-axis and y-axis before.

X_AXIS Y_AXIS
It use to graphing.



LOG_ENABLED
Default: False

Whether to enable logging, but it still display log on console.

LOG_LEVEL
Default: DEBUG

Minimum level to log. Available levels are: CRITICAL, ERROR, WARNING, INFO, DEBUG. For more info see Logging.

LOG_STDOUT
Default: False

If True, all standard output (and error) of your process will be redirected to the log. For example if you print 'hello' it will appear in the Vision log.

LOG_FILE
Default: None

File name to use for logging output. If None, standard error will be used.

Selectable settings reference
DATA_REPORT_FILE_NAME
If it exists, the data reports will have the same name,otherwise the project will use:

DATA_REPORT_CSV_FILE_NAME, DATA_REPORT_SVG_FILE_NAME
If it don't exist yet, the project will use:

MyDataReport.name



