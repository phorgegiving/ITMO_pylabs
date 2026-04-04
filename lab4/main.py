MAX_WEIGHT = 7  # 3x3 типа
INITIAL_SURVIVAL_POINTS = 15
REQUIRED_ITEMS = ['antidot']

available_items = {
    # item: (shortname, size, survival_points)
    'rifle': ('r', 3, 25),
    'pistol': ('p', 2, 15),
    'ammo': ('a', 2, 15),
    'medkit': ('m', 2, 20),
    'inhaler': ('i', 1, 5),
    'knife': ('k', 1, 15),
    'axe': ('x', 3, 20),
    'talisman': ('t', 1, 25),
    'flask': ('f', 1, 15),
    'antidot': ('d', 1, 10),
    'supplies': ('s', 2, 20),
    'crossbow': ('c', 2, 20)
}

def pack_backpack(items, capacity, required_items=None):
    if required_items is None:
        required_items = []
    
    item_names = list(items.keys())
    #short_names = [items[name][0] for name in item_names]
    weights = [items[name][1] for name in item_names]
    values = [items[name][2] for name in item_names] #survival ponts типа
    
    total_items = len(item_names)
    
    max_points = [[0 for _ in range(capacity + 1)] for _ in range(total_items + 1)] 
    selected = [[[] for _ in range(capacity + 1)] for _ in range(total_items + 1)]
    
    for i in range(1, total_items + 1):
        for w in range(1, capacity + 1):
            item_idx = i - 1
            item_weight = weights[item_idx]
            item_value = values[item_idx]
            
            if item_weight <= w:
                take_value = item_value + max_points[i-1][w - item_weight]
                not_take_value = max_points[i-1][w]
                
                if take_value > not_take_value:
                    max_points[i][w] = take_value
                    selected[i][w] = selected[i-1][w - item_weight] + [item_names[item_idx]]
                else:
                    max_points[i][w] = not_take_value
                    selected[i][w] = selected[i-1][w]
            else:
                max_points[i][w] = max_points[i-1][w]
                selected[i][w] = selected[i-1][w]
    
    best_items = selected[total_items][capacity]
    final_score = max_points[total_items][capacity]
    
    for req_item in required_items:
        if req_item not in best_items:
            req_weight = items[req_item][1]
            req_value = items[req_item][2]
            
            temp_items = [item for item in best_items if item != req_item]
            temp_weight = sum(items[item][1] for item in temp_items)
            temp_value = sum(items[item][2] for item in temp_items)
            
            if temp_weight + req_weight <= capacity:
                best_items = temp_items + [req_item]
                final_score = temp_value + req_value
            else:
                remaining_capacity = capacity - req_weight
                if remaining_capacity >= 0:
                    remaining_items = {k: v for k, v in items.items() if k != req_item}
                    remaining_dp = pack_backpack(remaining_items, remaining_capacity)
                    best_items = remaining_dp['items'] + [req_item]
                    final_score = remaining_dp['value'] + req_value
    return {
        'items': best_items,
        'value': final_score,
        'weight': sum(items[item][1] for item in best_items)
    }

def create_inventory_display(selected_items, items_data, inventory_width=3):
    inventory = []
    for item in selected_items:
        shortname = items_data[item][0]
        size = items_data[item][1]
        inventory.extend([shortname] * size)
    
    while len(inventory) < MAX_WEIGHT: #fallback чтобы не сломался инвентраь
        inventory.append('[ ]')
    
    inventory_2d = []
    for i in range(0, len(inventory), inventory_width):
        row = inventory[i:i + inventory_width]
        inventory_2d.append([f'[{item}]' for item in row])
    
    return inventory_2d

def calculate_base_survival(items_data, selected_items):
    base_score = 0
    for item in items_data:
        if item in selected_items:
            base_score += items_data[item][2]
        else:
            base_score -= items_data[item][2]
    
    return base_score + INITIAL_SURVIVAL_POINTS 

def init_inventory():
    print(f"Обязательные предметы: {REQUIRED_ITEMS}")
    result = pack_backpack(available_items, MAX_WEIGHT, REQUIRED_ITEMS)
    
    inventory_display = create_inventory_display(result['items'], available_items)
    final_score = calculate_base_survival(available_items, result['items'])
    
    print("Набор предметов:")
    for item in result['items']:
        shortname, size, value = available_items[item]
        print(f"  {item} ({shortname}): размер {size}, очки {value}")
    
    print(f"Занято места: {result['weight']}/{MAX_WEIGHT}")
    
    for row in inventory_display:
        print(' '.join(row))
    
    print(f"Очки выживания: {final_score}")

if __name__ == '__main__':
    init_inventory()