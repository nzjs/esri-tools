import arcgis
#from getpass import getpass
#import tempfile
from iteration_utilities import unique_everseen
from iteration_utilities import duplicates

print("Starting deletion script")
print()

# Initialise the AGOL session
gis = arcgis.GIS("https://org.maps.arcgis.com", "adminuser", "pass")
users = gis.users.search('adminuser')

#print(users)

user = users[0]

print('Authenticated: ' + user.username)
print()

# Get list of all items in user's folder
#print("Adding all user item id's to list")
gdbs_to_delete = []
num_items = 0
num_gdb = 0
#user_content = user.items()

root_content = user.items(folder=None, max_items=400)

#Get item ids from root folder first
for item in root_content:
    num_items += 1
    if (item.type.lower() == "file geodatabase"): 
        gdbs_to_delete.append(item)
        num_gdb += 1
        print(item)
    else:
        print("------------------------------------------------------------ Skipping: " + item.title)

print()
print("Number of overall items: " + str(num_items))
print("Number of gdbs/items to delete: " + str(len(gdbs_to_delete)))
print()

# dupes = list(duplicates(gdbs_to_delete))

# print()
# print("Number of duplicate items in gdb list: " + str(len(dupes)))
# print()

print("Deleting items")
for gdb_item in gdbs_to_delete:
    print("Deleting: " + str(gdb_item))
    gdb_item.delete()

#print(source_items_by_id)
#data = list(source_items_by_id.values())
#print(data)
#target.content.clone_items(data, 'CLONED', copy_data=True)

# print('Deleted content')
# print()

