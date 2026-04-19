def print_obj(obj, deepth):
    base_s = "\n" + "   " * deepth
    pre_s = "\n" + "   " * (deepth - 1)
    # print("PRINTING: ", obj, "deepth: ", deepth)
    if(isinstance(obj, dict)):
        if(deepth > 0):
            print(pre_s + "--->", end='')
        for k, v in obj.items():
            print(base_s, k, end='', sep='')
            print_obj(v, deepth + 1)
        
        if(deepth > 0):
            print(pre_s + "#####",end='')
        return True
    if(isinstance(obj, list)):
        if(deepth > 0):
            print(pre_s + "||||", end='')
        for v in obj:
            status = print_obj(v, deepth + 1)
            print(',', end=('\n' if status else ''))
        
        if(deepth > 0):
            print(pre_s + "////",end='')
        
        return True

    
    print(" ", obj, end='')
    return False

data = {
        'phase': 'game', 
        'fractions': ['borgo', 'moloch'], 
        'state': 'selected_hand', 
        'selected': {'name': 'klaun', 'slot': 0}, 
        'active_action': {}, 
        'current_fraction': 'borgo', 
        'next_turns': [
                {'frakcja': 'borgo', 'type': 'wystaw_sztab'}, 
                {'frakcja': 'moloch', 'type': 'wystaw_sztab'}], 
        'players': {
                'borgo': {
                    'hand': {'active_token': None, 'tokens': []}, 
                    'pile': ['nożownik', 'sieciarz', 'ruch', 'oficer', 'super-mutant', 'zwiadowca', 'bitwa', 'super-oficer', 'granat', 'siłacz', 'mutek', 'nożownik', 'nożownik', 'zabojca', 'bitwa', 'siłacz', 'mutek', 'bitwa', 'mutek', 'mutek', 'nożownik', 'sieciarz', 'ruch', 'ruch', 'bitwa', 'mutek', 'zabojca', 'bitwa', 'ruch', 'bitwa', 'sztab', 'medyk', 'oficer', 'zwiadowca', 'mutek']
                    }, 
                'moloch': {
                        'hand': {'active_token': 0, 'tokens': ['klaun']}, 
                        'pile': ['bitwa', 'juggernaut', 'dzialkogaussa', 'odepchniecie', 'mozg', 'opancerzonywartownik', 'odepchniecie', 'opancerzonylowca', 'zwiadowca', 'oficer', 'medyk', 'hybryda', 'bitwa', 'bloker', 'ruch', 'odepchniecie', 'bloker', 'lowca', 'opancerzonylowca', 'medyk', 'odepchniecie', 'wartownik', 'lowca', 'obronca', 'bomba', 'odepchniecie', 'sieciarz', 'bitwa', 'hybryda', 'matka', 'szturmowiec', 'bitwa', 'szerszeń']
                        }
                    }, 
        'board': {
                'board': [
                        [None, None, None, None, None, None, None, None, None], 
                        [None, None, None, None, None, None, None, None, None], 
                        [None, None, None, None, None, None, None, None, None], 
                        [None, None, None, {'frakcja': 'moloch', 'name': 'sztab', 'rotation': 1, 'rany': 0, 'zasieciowany': False}, None, None, None, None, None], 
                        [None, None, None, None, None, None, None, None, None]
                        ], 
                'available_hexes': [
                        [False, False, False, False, False, False, False, False, False], 
                        [False, False, False, False, False, False, False, False, False], 
                        [False, False, False, False, False, False, False, False, False], 
                        [False, False, False, False, False, False, False, False, False], 
                        [False, False, False, False, False, False, False, False, False]
                        ]
                }
        }

# data2 = {"a" : 2, "b" : 1}
print_obj(data, 0)