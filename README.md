<img src="gsq.jpg" style="width:25%" />

# GSQ's Features of Interest API 
This [API](https://en.wikipedia.org/wiki/Application_programming_interface) delivers the [Geological Survey of Queensland](https://en.wikipedia.org/wiki/Geological_Survey_of_Queensland)'s Structural Framework [Features of Interest](https://www.w3.org/TR/vocab-ssn/#SOSAFeatureOfInterest) data for Queensland according to [Linked Data](https://en.wikipedia.org/wiki/Linked_data) principles.

The primary purpose of this API is to allow for the resolution of the URIs of various Features of Interest. For example, the FoI "Bowen Basin" has the persistent URI **http://linked.data.gov.au/dataset/qld-structural-framework/feature/BowenBasin** allocated to it and clicking on that URI will prompt this API to deliver a home page from it. Or data, depending on the type of request you make.


## Data
***Currently this API only delivers Structural Framework data, not all of GSQ's Features of Interest.***

The source data for this API so far is taken from data already published by GSQ via the [Queensland Globe](https://qldglobe.information.qld.gov.au/), so all of this information is already public.

To access the underlying data directly, see GSQ's *Structural Framework Dataset*:

* https://github.com/geological-survey-of-queensland/gsq-foi-dataset


## API
The API framework used to deliver this data is the [pyLDAPI](http://github.com/rdflib/pyLDAPI) which is a "A very small [Python] module that adds Linked Data API functionality to a Python Flask installation.".

In total, this API is installed on a web server and called by an HTTP server (Apache). Some requests (static pages) are served up directly from template HTML files. Other requests, such as for the list of all Basins or the homepage of a particular basin, are served via templates after the relevant data is extracted from the dataset (see 'Data' above).

 
## License
The content of this API is licensed for use under the [Creative Commons 4.0 License](https://creativecommons.org/licenses/by/4.0/). See the [license deed](LICENSE) for details.


## Contacts
*owner*:  
**Geological Survey of Queensland**  
*Within the Queensland Department of Natural Resources, Mines & Energy*  
1 William St, Brisbane, Queensland, Australia  
<https://www.business.qld.gov.au/industries/mining-energy-water/resources/geoscience-information/gsq>  
<GSQOpenData@dnrme.qld.gov.au>  

*author*:  
**Nicholas Car**  
[SURROUND Australia Pty Ltd](https://surroundaustralia.com)  
<nicholas.car@surroundaustralia.com>  
<http://orcid.org/0000-0002-8742-7730>  



