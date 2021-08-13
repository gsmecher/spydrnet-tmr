def check_uniquify_nmr_property(replicas,property_keys,suffix):
    """
    Checks to make sure that the specified properties were 1) uniquified and 2) uniquified correctly

        :param replicas: A map from an original element to its replicas.
        :param property_keys: A set of property keys whose values should have been made unique.
        :param suffix: the suffix appended to the uniquified properties
        :return: True/False

    """
    if isinstance(property_keys, str):
        property_keys = {property_keys}
    else:
        property_keys = set(property_keys)
    property_keys_lower = {x.lower() for x in property_keys}

    incorrect = []
    for original, copies in replicas.items():
        if not check_edif_properties(original, property_keys, property_keys_lower, suffix):
            incorrect.append(original)
        for copy in copies:
            if not check_edif_properties(copy, property_keys, property_keys_lower, suffix):
                incorrect.append(copy)
    if incorrect:
        print("FAILED")
        return False
    else:
        print("PASSED")
        return True

def check_edif_properties(element, property_keys, property_keys_lower, suffix):
    correct = True
    if 'EDIF.properties' in element:
        edif_properties = element['EDIF.properties']
        for property in edif_properties:
            if ('identifier' in property and property['identifier'].lower() in property_keys_lower) or \
                    ('original_identifier' in property and property['original_identifier'] in property_keys):
                if 'value' in property:
                    value = property['value']
                    print(element['EDIF.properties'])
                    if isinstance(value, str):
                        if not check_property(element,value,suffix):
                            correct = False
                            break
    return correct

def check_property(element,value,suffix):
    key = find_key(element,suffix)
    if key in value:
        return True
    return False

def find_key(instance,suffix):
    start_index = instance.name.find(suffix)
    stop_index = start_index + len(suffix) + 2
    if start_index is -1:
        key = ''
    else:
        key = instance.name[start_index:stop_index]
    return key
