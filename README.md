<img src="gsq.jpg" style="width:25%" />

# GSQ's Queensland Geological Features API 
This [API](https://en.wikipedia.org/wiki/Application_programming_interface) delivers the [Geological Survey of Queensland](https://en.wikipedia.org/wiki/Geological_Survey_of_Queensland)'s Structural Framework [Features of Interest](https://www.w3.org/TR/vocab-ssn/#SOSAFeatureOfInterest) data for Queensland according to [Linked Data](https://en.wikipedia.org/wiki/Linked_data) principles.

The primary purpose of this API is to allow for the resolution of the URIs of various Features of Interest. For example, the Feature "Bowen Basin" has the persistent URI **https://linked.data.gov.au/dataset/qldgeofeatures/BowenBasin** allocated to it and clicking on that URI will prompt this API to deliver a home page from it. Or data, depending on the type of request you make.


## Data
***Currently this API only delivers Structural Framework data, not all of GSQ's Features of Interest.***

The source data for this API so far is taken from data already published by GSQ via the [Queensland Globe](https://qldglobe.information.qld.gov.au/), so all of this information is already public.

To access the underlying data directly, see GSQ's *Structural Framework Dataset*:

* https://github.com/geological-survey-of-queensland/qldgeofeatures-dataset


## API
The API framework used to deliver this data is the [pyLDAPI](http://github.com/rdflib/pyLDAPI) which is a "A very small [Python] module that adds Linked Data API functionality to a Python Flask installation.".

In total, this API is installed on a web server and called by an HTTP server (Apache). Some requests (static pages) are served up directly from template HTML files. Other requests, such as for the list of all Basins or the homepage of a particular basin, are served via templates after the relevant data is extracted from the dataset (see 'Data' above).


## Installation
1. Clone the repo to the target server
2. Tune the API's URI
    * replace controller/routes.py's `ages()` function's `.replace()` statement that switches out object's persistent URI base with http://localhost:5000/ and use the URI of the installation API
    * replace model/province.py's Province class's `__init__()` function's `.replace()` statement, as above
    * replace the register.html template's `.replace()` statement as above
3. Install a Python virtual environment 
    * something like this:
  
    ```
    ~$ mkdir venv                       # folder for the virtual env
    ~$ python3 -m venv venv             # creates a virtual env in venv folder
    ~$ source venv/bin/activate         # turns on the venv
    ~$ pip install -r requirements.txt  # installs the API's Python module requirements in the venv
    ~$ deactivate                       # switch out of the venv
    ```
4. Configure the target server's Apache to call the app, using the venv
    * something like this, within the relevant Apache config file:
  
    Example vars:

    ```
    WSGIDaemonProcess geof threads=2 python-path=/var/www/qldgeofeatures-api/venv/:/var/www/qldgeofeatures-api/venv/lib/python3.6/site-packages/

    WSGIProcessGroup geof
    WSGIApplicationGroup %{GLOBAL}

    WSGIScriptAlias /qldgeofeatures /var/www/qldgeofeatures-api/geofeatures/app.wsgi
    <Directory /var/www/qldgeofeatures-api/geofeatures/>
            WSGIScriptReloading On
            Require all granted
    </Directory>
    ```

Now restart Apache and the site should be up at /qldgeofeatures

 
## License
The content of this API is licensed for use under the [Creative Commons 4.0 License](https://creativecommons.org/licenses/by/4.0/). See the [license deed](LICENSE) for details.


## Contacts
*System owner*:  
**Mark Gordon**,
Geological Survey of Queensland,
Department of Resources,
Brisbane, QLD, Australia,
<mark.gordon@resources.qld.gov.au>  

*Contributors*:  
**Vance Kelly**,
Principal Data Manager,
Geological Survey of Queensland,
Department of Resources,
Brisbane, QLD, Australia,  
<vance.kelly@resources.qld.gov.au>
