import arcpy

infc = arcpy.GetParameterAsText(0)
joinfc = arcpy.GetParameterAsText(1)
outfc = arcpy.GetParameterAsText(2)

infc_sr = arcpy.Describe(infc).spatialReference
join_sr = arcpy.Describe(joinfc).spatialReference

# Spatially join the bus stop layer with the Community Statistical Area layer
if infc_sr.name != join_sr.name:
    arcpy.AddError("The spatial reference of the input layer does not match the join layer")
    sys.exit(1)
else:
    arcpy.analysis.SpatialJoin(infc, joinfc, outfc, match_option="INTERSECT")
