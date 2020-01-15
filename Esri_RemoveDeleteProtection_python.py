from arcgis.gis import GIS

# AGOL credentials
org = 'https://org.maps.arcgis.com'
username = 'user'
password = 'pass'

corrupt_itemid = '<itemid>' # eg. 6f2ee81da4bb4238af42aea774ac173t

# Do things
agol_env = GIS(org, username, password) 
print('Authenticated: ', agol_env)
print()

corrupt_item = agol_env.content.get(corrupt_itemid)
print(corrupt_item)
print()

corrupt_item.protect(enable=False)
print('Delete protection disabled')
print()

corrupt_item.delete()
print('Deleted')