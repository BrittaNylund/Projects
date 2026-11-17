infc = arcpy.GetParameterAsText(0)
sql_expression = arcpy.GetParameterAsText(1)
buff_dist = arcpy.GetParameterAsText(2)
out_buff = arcpy.GetParameterAsText(3)
output_name = arcpy.GetParameterAsText(4)

#verify that layer has an ID attribute and that its shape type is point
fields = arcpy.ListFields(infc)
has_oid = any(field.type == 'OID' for field in fields)
if has_oid == True:
    # Select a single point to create a buffer around
    selected_point = arcpy.management.SelectLayerByAttribute(
    infc, "NEW_SELECTION", sql_expression)
else:
    arcpy.AddError("The layer does not contain an object ID column.")
    sys.exit(1)

# Create buffer with desired distance around selected point, utilize planar or geodesic methods based on spatial reference
sr = arcpy.Describe(infc).spatialReference
if sr.type == "Projected":
    arcpy.analysis.PairwiseBuffer(selected_point, out_buff, buff_dist, method="PLANAR")
else:
    arcpy.analysis.PairwiseBuffer(selected_point, out_buff, buff_dist, method="GEODESIC")
