# Canvas Custom Integration
This is custom Home Assistant Integration for [Canvas](https://canvas.instructure.com/) from Instructure.  

This integration will create several sensor entities for different objects retrieved from the [Canvas API](https://canvas.instructure.com/doc/api/) using the [Canvas Parent API](https://github.com/schwartzpub/canvas_parent_api) python module.

The entities that will be created are:
 - sensor.canvas_students
 - sensor.canvas_courses
 - sensor.canvas_assignments

Currently this integration simply returns the raw output from the [Canvas API]() for these objects.  There is a basic custom card for viewing [Canvas homework assignments](https://github.com/schwartzpub/homeassistant-cards) as well.

## Installing
To install this integration, clone the repository into your Home Assistant custom_components directory:

```bash
[core-ssh ~]$ cd config/custom_components/
[core-ssh ~]$ mkdir canvas
[core-ssh ~]$ cd canvas
[core-ssh ~]$ git clone git@github.com:schwartzpub/canvas_hassio .
```

In Home Assistant, navigate to Settings > Devices & Services and click + Add Integration

Select the Canvas integration.

Enter the following information:
 - Base URL (https://<yourdistrict>.instructure.com)
 - Canvas API Token 

 
### Generating Canvas API Token
If you are a parent, you will have a Canvas Parent account.  To get an API token, you must sign into the Canvas Parent application from a web browser.  This is typically using: https://<yourdistrict>.instructure.com/login/canvas

Once you have signed into your account, navigate to Account > Settings.

Under "Approved Integrations" click "+ New Access Token" to create a new API Token.

Enter a Purpose and Expiration date (blank for no expiration).

Be sure to save your API token, as you will have to generate a new token if this is lost.