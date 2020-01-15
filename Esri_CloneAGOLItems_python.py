# Purpose: Run this script to clone users, groups and items from source to a target Portal for ArcGIS.
# Note: This script does not copy over services, hence the web layer items continue to have the same URL pointing to
# services in the source server.

from arcgis.gis import GIS
import tempfile

print("Starting clone portal script")
print("----------------------------")
# region: Authenticate
#source_password = getpass("Enter password for source portal: ")
#target_password = getpass("Enter password for target portal: ")
source = GIS("https://sourceorg.maps.arcgis.com", "adminuser", "pass")
target = GIS("https://targetorg.maps.arcgis.com", "adminuser", "pass")
target_admin_username = 'adminuser'
# endregion

# region : Get user accounts in source and target
# get the list of users in source portal. Ignore system accounts
print("\nGetting list of users in source portal")
# source_users = source.users.search('!esri_ & !admin')
source_users = source.users.search('adminuser')
for user in source_users:
    print(user.username + "\t:\t" + str(user.role))

print("\nTotal number of users for cloning: " + str(len(source_users)))

# get the list of users in target portal. Ignore system accounts
# target_users = target.users.search('!esri_ & !admin & !system_publisher')
target_users = target.users.search('adminuser')
print("\nUsers in target portal:")
for user in target_users:
    print(user.username + "\t:\t" + str(user.role))


# region: Copy items: Get list of all items in source
print("\nGetting the list of all items in source portal")
source_items_by_id = {}
for user in source_users:
    num_items = 0
    num_folders = 0
    print("Collecting item ids for {}".format(user.username), end="\t\t")
    user_content = user.items()
    
    #Get item ids from root folder first
    for item in user_content:
        num_items += 1
        source_items_by_id[item.itemid] = item 

    # Get item ids from each of the folders next
    folders = user.folders
    for folder in folders:
        num_folders += 1
        folder_items = user.items(folder=folder['title'])
        for item in folder_items:
            num_items += 1
            source_items_by_id[item.itemid] = item


##Test a single folder before we migrate everything ...
# folders = user.folders # 16=Sandbox folder, 14=Welfare
# for folder in folders[14]: 
#     num_folders += 1
#     folder_items = user.items(folder='NEMA - Welfare')
#     for item in folder_items:
#         num_items += 1
#         source_items_by_id[item.itemid] = item

    print("Number of folders {} # Number of items {}".format(str(num_folders), str(num_items)))
# endregion

# region: Copy items: Copy items
TEXT_BASED_ITEM_TYPES = frozenset(['Web Map', 'Feature Service', 'Map Service','Web Scene',
                                   'Image Service', 'Feature Collection', 
                                   'Feature Collection Template',
                                   'Web Mapping Application', 'Mobile Application', 
                                   'Symbol Set', 'Color Set',
                                   'Windows Viewer Configuration'])

FILE_BASED_ITEM_TYPES = frozenset(['File Geodatabase','CSV', 'Image', 'KML', 'Locator Package',
                                  'Map Document', 'Shapefile', 'Microsoft Word', 'PDF',
                                  'Microsoft Powerpoint', 'Microsoft Excel', 'Layer Package',
                                  'Mobile Map Package', 'Geoprocessing Package', 'Scene Package',
                                  'Tile Package', 'Vector Tile Package'])

ITEM_COPY_PROPERTIES = ['title', 'type', 'typeKeywords', 'description', 'tags',
                        'snippet', 'extent', 'spatialReference', 'name',
                        'accessInformation', 'licenseInfo', 'culture', 'url', ]


print("\n\nCopying items")
print("--------------")
def copy_item(target, source_item):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            item_properties = {}
            for property_name in ITEM_COPY_PROPERTIES:
                item_properties[property_name] = source_item[property_name]

            data_file = None
            
            if source_item.type in TEXT_BASED_ITEM_TYPES:
                # If its a text-based item, then read the text and add it to the request.
                text = source_item.get_data(False)
                item_properties['text'] = text
            
            elif source_item.type in FILE_BASED_ITEM_TYPES:
                # download data and add to the request as a file
                data_file = source_item.download(temp_dir)

            thumbnail_file = source_item.download_thumbnail(temp_dir)
            metadata_file = source_item.download_metadata(temp_dir)

            #find item's owner
            #source_item_owner = source.users.search(source_item.owner)[0]
            source_item_owner = source_users[0]
            
            #find item's folder
            item_folder_titles = [f['title'] for f in source_item_owner.folders 
                                  if f['id'] == source_item.ownerFolder]
            folder_name = None
            if len(item_folder_titles) > 0:
                folder_name = item_folder_titles[0]

            #if folder does not exist for target user, create it
            target_user = target_users[0]
            if folder_name:
                #target_user = target.users.search(source_item.owner)[0]
                #target_user = target_users[0]
                target_user_folders = [f['title'] for f in target_user.folders
                                       if f['title'] == folder_name]
                if len(target_user_folders) == 0:
                    #create the folder
                    #target.content.create_folder(folder_name, source_item.owner)
                    target.content.create_folder(folder_name, target_user)
            
            # Add the item to the target portal, assign owner and folder
            target_item = target.content.add(item_properties, data_file, thumbnail_file, 
                                             metadata_file, target_user, folder_name)
            
            #Set sharing (privacy) information
            share_everyone = source_item.access == 'public'
            share_org = source_item.access in ['org', 'public']
            share_groups = []
            #if source_item.access == 'shared':
             #   share_groups = source_item.groups
            
            target_item.share(share_everyone, share_org, share_groups)
            
            return target_item
        
    except Exception as copy_ex:
        print("\tError copying " + source_item.title)
        print("\t" + str(copy_ex))
        return None

#Construct a dictionary of item id and item
source_target_itemId_map = {}
for key in source_items_by_id.keys():
    source_item = source_items_by_id[key]

    print("Copying {} \tfor\t {}".format(source_item.title, source_item.owner))
    target_item = copy_item(target, source_item)
    if target_item:
        source_target_itemId_map[key] = target_item.itemid
    else:
        source_target_itemId_map[key] = None

#endregion

# region: Copy items: Get item relationships
print("\nEstablishing relationships between items in target portal")
print("---------------------------------------------------------")
RELATIONSHIP_TYPES = frozenset(['Map2Service', 'WMA2Code',
                                'Map2FeatureCollection', 'MobileApp2Code', 'Service2Data',
                                'Service2Service'])
print()
for key in source_items_by_id.keys():
    try:
        source_item = source_items_by_id[key]
        target_itemid = source_target_itemId_map[source_item.itemid]
        target_item = target.content.get(target_itemid)
    except Exception as key_ex:
        print("\t\t Error with KEY for " + key + " : " + str(key_ex))
        continue
    

    print(source_item.title + " # " + source_item.type)
    for relationship in RELATIONSHIP_TYPES:
        try:
            source_related_items = source_item.related_items(relationship)
            for source_related_item in source_related_items:
                print("\t\t" + source_related_item.title + " # " + source_related_item.type +"\t## " + relationship)

                #establish same relationship amongst target items
                print("\t\t" + "establishing relationship in target portal", end="")
                target_related_itemid = source_target_itemId_map[source_related_item.itemid]
                target_related_item = target.content.get(target_related_itemid)
                status = target_item.add_relationship(target_related_item, relationship)
                print(str(status))
        except Exception as rel_ex:
            print("\t\t Error when checking for " + relationship + " : " + str(rel_ex))
            continue
# endregion

print()
print('Finished')