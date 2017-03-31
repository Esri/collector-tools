import argparse
import sys
import urllib
import urllib.parse
import urllib.request
import json
from arcgis.gis import GIS


# Parse Command-line arguments
def parseArguments():
    global args_parser
    parser = argparse.ArgumentParser(
        usage='Add/Update GNSS metadate fields')
    parser.add_argument('-u', '--username', required=True, type=str, help='Organization username')
    parser.add_argument('-p', '--password', required=True, type=str, help='Organization password')
    parser.add_argument('-url', '--url', required=True, type=str, help='Organization url')
    parser.add_argument('-r', '--remove', default=False, type=bool,
                        help='Set True if GNSS metadata fields need to be removed')
    parser.add_argument('itemId', type=str, nargs="+", help='Search string')
    args_parser = parser.parse_args()


# Generate Token based on username and password
def generateToken():
    global token

    datapayload = bytes(urllib.parse.urlencode( \
        {'username': args_parser.username, 'password': args_parser.password, 'referer': args_parser.url, 'f': 'json',
         'expiration': 60}), 'utf-8')
    token_response = urllib.request.urlopen(urllib.parse.urljoin(args_parser.url, '/sharing/rest/GenerateToken?'),
                                            datapayload).read()
    token = json.loads(token_response)['token']
    if not token:
        print('Failed to generate Token .. ')
        sys.exit(-2)


# Search for a item id and add GNSS Metadata fields
def searchItems_addGNSSMetadataFields():
    global featureServiceUrl

    # Search ItemIds
    gis = GIS(args_parser.url, args_parser.username, args_parser.password)
    itemId = args_parser.itemId

    try:
        # Iterate through each ItemId and update the domain values
        for id in itemId:
            featurelayerItem = gis.content.search(id)
            featureServiceUrl = featurelayerItem[0].layers[0].url

            # Construct the Payload
            datapayload = bytes(urllib.parse.urlencode({'token': token}), 'utf-8')

            featureLayerResponse = urllib.request.urlopen(urllib.parse.urljoin(featureServiceUrl, '?&f=pjson'),
                                                          datapayload).read()
            featureLayerJson = json.loads(featureLayerResponse)

            # Extract fields from Feature layer service definition
            featureLayerFields = featureLayerJson['fields']

            # New fields which need to be added
            gnssMetadataFields = {'fields': []}

            # Operations list - Add, Update or delete GNSS Metadata fields.
            operations = []

            # Add/Update GNSS Metadata fields
            if not args_parser.remove:                

                # ESRIGNSS_FIXDATETIME
                fixTimeField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_FIXDATETIME']

                if not fixTimeField:
                    gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_FIXDATETIME', 'type': 'esriFieldTypeDate', \
                                                         'alias': 'Fix Time', 'sqlType': 'sqlTypeOther',
                                                         'length': 0, 'nullable': True, 'editable': True, \
                                                         'domain': None, 'defaultValue': None})
                

                # ESRIGNSS_RECEIVER
                recieverField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_RECEIVER']

                if not recieverField:
                    gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_RECEIVER', 'type': 'esriFieldTypeString', \
                                                         'alias': 'Receiver Name', 'sqlType': 'sqlTypeOther',
                                                         'length': 50, 'nullable': True, 'editable': True, \
                                                         'domain': None, 'defaultValue': None})

                # ESRIGNSS_H_RMS
                horizontalAccuracyField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_H_RMS']

                if not horizontalAccuracyField:
                    gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_H_RMS', 'type': 'esriFieldTypeDouble', \
                                                         'alias': 'Horizontal Accuracy (m)', 'sqlType': 'sqlTypeOther',
                                                         'nullable': True, 'editable': True, \
                                                         'domain': None, 'defaultValue': None})
                # ESRIGNSS_V_RMS
                verticalAccuracyField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_V_RMS']

                if not verticalAccuracyField:
                    gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_V_RMS', 'type': 'esriFieldTypeDouble', \
                                                         'alias': 'Vertical Accuracy (m)', 'sqlType': 'sqlTypeOther',
                                                         'nullable': True, 'editable': True, \
                                                         'domain': None, 'defaultValue': None})

                # ESRIGNSS_LATITUDE
                latitudeField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_LATITUDE']

                if not latitudeField:
                    gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_LATITUDE', 'type': 'esriFieldTypeDouble', \
                                                         'alias': 'Latitude', 'sqlType': 'sqlTypeOther',
                                                         'nullable': True, 'editable': True, \
                                                         'domain': None, 'defaultValue': None})

                # ESRIGNSS_LONGITUDE
                longitudeField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_LONGITUDE']

                if not longitudeField:
                    gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_LONGITUDE', 'type': 'esriFieldTypeDouble', \
                                                         'alias': 'Longitude', 'sqlType': 'sqlTypeOther',
                                                         'nullable': True, 'editable': True, \
                                                         'domain': None, 'defaultValue': None})

                # ESRIGNSS_ALTITUDE
                altitudeField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_ALTITUDE']

                if not altitudeField:
                    gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_ALTITUDE', 'type': 'esriFieldTypeDouble', \
                                                         'alias': 'Altitude', 'sqlType': 'sqlTypeOther',
                                                         'nullable': True, 'editable': True, \
                                                         'domain': None, 'defaultValue': None})
                # ESRIGNSS_PDOP
                pdopField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_PDOP']

                if not pdopField:
                    gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_PDOP', 'type': 'esriFieldTypeDouble', \
                                                         'alias': 'PDOP', 'sqlType': 'sqlTypeOther', 'nullable': True,
                                                         'editable': True, \
                                                         'domain': None, 'defaultValue': None})

                # ESRIGNSS_HDOP
                hdopField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_HDOP']

                if not hdopField:
                    gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_HDOP', 'type': 'esriFieldTypeDouble', \
                                                         'alias': 'HDOP', 'sqlType': 'sqlTypeOther', 'nullable': True,
                                                         'editable': True, \
                                                         'domain': None, 'defaultValue': None})

                # ESRIGNSS_VDOP
                vdopField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_VDOP']

                if not vdopField:
                    gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_VDOP', 'type': 'esriFieldTypeDouble', \
                                                         'alias': 'VDOP', 'sqlType': 'sqlTypeOther', 'nullable': True,
                                                         'editable': True, \
                                                         'domain': None, 'defaultValue': None})

                # ESRIGNSS_CORRECTIONAGE
                correctionAgeField = [field for field in featureLayerFields if
                                      field['name'] == 'ESRIGNSS_CORRECTIONAGE']

                if not correctionAgeField:
                    gnssMetadataFields['fields'].append(
                        {'name': 'ESRIGNSS_CORRECTIONAGE', 'type': 'esriFieldTypeDouble', \
                         'alias': 'Correction Age', 'sqlType': 'sqlTypeOther', 'nullable': True, 'editable': True, \
                         'domain': None, 'defaultValue': None})

                # ESRIGNSS_FIXTYPE
                fixTypeField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_FIXTYPE']

                if fixTypeField:
                    # Field does exist check if the domain is set.
                    if fixTypeField[0]['domain'] == None:
                        if (len([operation for operation in operations if operation == 'updateDefinition'])) == 0:
                            operations.append('updateDefinition')

                        fixtypeFieldIndex = featureLayerFields.index(fixTypeField[0])
                        fixTypeDomain = {'type': 'codedValue', 'name': 'ESRI_FIX_TYPE_DOMAIN',
                                         'codedValues': [{'name': 'Fix not valid', 'code': 0}, \
                                                         {'name': 'GPS', 'code': 1},
                                                         {'name': 'Differential GPS', 'code': 2}, \
                                                         {'name': 'RTK Fixed', 'code': 4},
                                                         {'name': 'RTK Float', 'code': 5}]}
                        featureLayerJson['fields'][fixtypeFieldIndex]['domain'] = fixTypeDomain
                    
                else:
                    gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_FIXTYPE', 'type': 'esriFieldTypeInteger', \
                                                         'alias': 'Fix Type', 'sqlType': 'sqlTypeOther',
                                                         'nullable': True, 'editable': True, \
                                                         'domain': {'type': 'codedValue',
                                                                    'name': 'ESRI_FIX_TYPE_DOMAIN', 'codedValues': \
                                                                        [{'name': 'Fix not valid', 'code': 0},
                                                                         {'name': 'GPS', 'code': 1},
                                                                         {'name': 'Differential GPS', 'code': 2}, \
                                                                         {'name': 'RTK Fixed', 'code': 4},
                                                                         {'name': 'RTK Float', 'code': 5}]},
                                                         'defaultValue': None})

                # ESRIGNSS_STATIONID
                stationIdField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_STATIONID']

                if stationIdField:
                    # Field does exist check if the domain is set.
                    if stationIdField[0]['domain'] == None:
                        if (len([operation for operation in operations if operation == 'updateDefinition'])) == 0:
                            operations.append('updateDefinition')
                        stationIdFieldIndex = featureLayerFields.index(stationIdField[0])
                        stationIdDomain = {'type': 'range', 'name': 'ESRI_STATION_ID_DOMAIN', 'range': [0, 1023]}
                        featureLayerJson['fields'][stationIdFieldIndex]['domain'] = stationIdDomain

                else:
                    gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_STATIONID', 'type': 'esriFieldTypeInteger', \
                                                         'alias': 'Station ID', 'sqlType': 'sqlTypeOther',
                                                         'nullable': True, 'editable': True, \
                                                         'domain': {'type': 'range', 'name': 'ESRI_STATION_ID_DOMAIN',
                                                                    'range': [0, 1023]}, 'defaultValue': None})

                # ESRIGNSS_NUMSATS
                numstatsField = [field for field in featureLayerFields if field['name'] == 'ESRIGNSS_NUMSATS']

                if numstatsField:
                    # Field does exist check if the domain is set.
                    if numstatsField[0]['domain'] == None:
                        if (len([operation for operation in operations if operation == 'updateDefinition'])) == 0:
                            operations.append('updateDefinition')
                        numSatellitesFieldIndex = featureLayerFields.index(numstatsField[0])
                        numSatellitesDomain = {'type': 'range', 'name': 'ESRI_NUM_SATS_DOMAIN', 'range': [0, 99]}
                        featureLayerJson['fields'][numSatellitesFieldIndex]['domain'] = numSatellitesDomain

                else:
                    gnssMetadataFields['fields'].append({'name': 'ESRIGNSS_NUMSATS', 'type': 'esriFieldTypeInteger', \
                                                         'alias': 'Number of Satellites', 'sqlType': 'sqlTypeOther',
                                                         'nullable': True, 'editable': True, \
                                                         'domain': {'type': 'range', 'name': 'ESRI_NUM_SATS_DOMAIN',
                                                                    'range': [0, 99]}, 'defaultValue': None})

                # Check if AddToDefinition operation needs to be added.
                initialFeatureLayerFieldsCount = len(featureLayerFields)
                if (len(gnssMetadataFields[
                            'fields']) + initialFeatureLayerFieldsCount) > initialFeatureLayerFieldsCount:
                    operations.append('addToDefinition')
            else:
                operations.append('deleteFromDefinition')
                gnssMetadataFields = {
                    'fields': [{'name': 'ESRIGNSS_FIXDATETIME'},{'name': 'ESRIGNSS_RECEIVER'}, {'name': 'ESRIGNSS_H_RMS'}, {'name': 'ESRIGNSS_V_RMS'},
                               {'name': 'ESRIGNSS_LATITUDE'}, \
                               {'name': 'ESRIGNSS_LONGITUDE'}, {'name': 'ESRIGNSS_ALTITUDE'}, {'name': 'ESRIGNSS_PDOP'},
                               {'name': 'ESRIGNSS_HDOP'}, \
                               {'name': 'ESRIGNSS_VDOP'}, {'name': 'ESRIGNSS_CORRECTIONAGE'},
                               {'name': 'ESRIGNSS_FIXTYPE'}, {'name': 'ESRIGNSS_STATIONID'}, \
                               {'name': 'ESRIGNSS_NUMSATS'}]}

            # Get index of the substring /services/ to construct admin url.
            servicesKeywordIndex = featureServiceUrl.index('/services/')

            for operation in operations:
                # Construct admin url to Update/Add/Delete service definition
                adminUrl = featureServiceUrl[0:servicesKeywordIndex] + '/admin' + featureServiceUrl[
                                                                                  servicesKeywordIndex:] + '/' + operation + '?'

                # Update/Add/Delete Service Definition
                payload = ''
                if operation == 'addToDefinition' or operation == 'deleteFromDefinition':
                    payload = bytes(urllib.parse.urlencode({'token': token, 'f': 'json',
                                                            operation: json.dumps(gnssMetadataFields).encode('utf8',
                                                                                                             errors='replace')}),
                                    'utf-8')
                else:
                    featureLayerJson['editingInfo'] = {'lastEditDate': ''}
                    payload = bytes(urllib.parse.urlencode({'token': token, 'f': 'json',
                                                            operation: json.dumps(featureLayerJson).encode('utf8',
                                                                                                           errors='replace')}),
                                    'utf-8')

                serviceDefinitionResponse = urllib.request.urlopen(adminUrl, payload).read()
                result = json.loads(serviceDefinitionResponse)['success']

                if not result:
                    print('Failed to update Feature layer service definition..')
                else:
                    print('Service definition updated successfully..')

    except Exception as e:
        print('Failed to Update Feature layer service definition')


if __name__ == '__main__':
    parseArguments()
    generateToken()
    searchItems_addGNSSMetadataFields()
