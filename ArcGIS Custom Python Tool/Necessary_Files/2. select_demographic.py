import arcpy

infc = arcpy.GetParameterAsText(0)
temp_lyr = arcpy.GetParameterAsText(1)
field_name = arcpy.GetParameterAsText(2)
input_value = arcpy.GetParameter(3)
output_name = arcpy.GetParameterAsText(4)

sql_query = "{} >= {}".format(field_name, input_value)

# determine if input layer's demographic field is in decimal format
max_val = None
with arcpy.da.SearchCursor(infc, [field_name]) as cursor:
    for row in cursor:
        if row[0] is not None:
            if max_val is None or row[0] > max_val:
                max_val = round(row[0], 2)
if max_val is not None and max_val < 1 and float(input_value) >= 1:
    arcpy.AddError("The demographic field selected is a decimal fraction.  Please enter a decimal value for percentage.")
    sys.exit(1)

#determine if input layer's demographic field is in percentage format
greater_than_one = None
with arcpy.da.SearchCursor(infc, field_name) as cursor:
    for row in cursor:
        if row[0] is not None and row[0] >= 1:
            greater_than_one = True
            break
if greater_than_one and float(input_value) < 1:
    arcpy.AddError("The demographic field selected is in percentage format.  Please enter a percentage in this format.")
    sys.exit(1)

# Make the feature layer
arcpy.management.MakeFeatureLayer(infc, temp_lyr)

# Select features by attribute
arcpy.management.SelectLayerByAttribute(temp_lyr, "NEW_SELECTION", sql_query)

# Create a new layer from the selection
# Use CopyFeatures to save to disk as a new feature class
arcpy.management.CopyFeatures(temp_lyr, output_name)
