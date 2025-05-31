sample = my_image.addBands(my_lc).stratifiedSample(**{
  'numPoints': 300,
  'classBand': label,
  'region': my_image.geometry(),
  'scale': 10,
  'geometries': True
})
