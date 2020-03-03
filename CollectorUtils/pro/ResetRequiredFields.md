# Reset Required Fields
**Note: This tool applies to working with Hosted Feature Services in ArcGIS Online or Portal. If you're working with ArcGIS Server Feature Services there is a different workflow to utilize, please go [here](https://support.esri.com/en/Technical-Article/000022706).**

Sets the "required" fields to be null rather than white-space or 0 in the service definition template information.

Supported in ArcGIS Pro 2.0+

Fields are said to be "required" in Collector if the field is not nullable. In the template information in the layer definition file, some of these fields are set to blank white-space (" ","") or to 0. These template values then auto-populate the fields in the Collector app meaning the end-user doesn't have to enter anything, when in reality, they should be forced to enter a value. 

### Using as a Script Tool within ArcGIS Pro

![image](https://user-images.githubusercontent.com/26557666/38632020-4d8b5f12-3d70-11e8-8b6a-2ad4c18fd7f9.png)


**Script takes the following parameters as input**
1. Organization Url 
2. Username 
3. Password
4. Feature Service ItemId

**Instructions to run the script**
1. Connect to the folder containing the "CollectorUtils_Pro" toolbox
2. Double click on the "CollectorUtils_Pro" toolbox that should be shown in the catalog/project area
3. Under GeneralUtils toolbox double click the "Reset Required Fields (Python api)" script tool
4. Enter required input parameters    
5. Click Run

![Alt text](/images/ResetRequiredFields_interface.JPG "Interface")

### Using as a standalone script
Run the [reset_required_fields_python_api.py](scripts/reset_required_fields_python_api.py) script in Python 3.4+ as (omit the '{}' brackets for the arguments):

![capture](https://user-images.githubusercontent.com/24723464/38956897-d9a2efae-430d-11e8-8a82-3505089164bc.PNG)

### Learn more  
See [Require the information you need from the field](https://www.esri.com/arcgis-blog/products/apps/field-mobility/capture-required-information-from-field/) for more about this tool.
