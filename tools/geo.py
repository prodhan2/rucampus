# RU campus: lat/lon (OpenStreetMap) -> game world coordinates
X0, LON0, SX = 1565.0, 88.643191, 127700.0
Y0, LAT0, SY = 223.0, 24.375464, 106030.0
def gx(lon): return X0 + (lon-LON0)*SX
def gy(lat): return Y0 + (LAT0-lat)*SY
