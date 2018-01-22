def filter_data(company_id):
    json_obj = {}
    total_users = {
        1: ['1@gmail.com', 'a'],
        2: ['2@gmail.com', 'b'],
        3: ['3@gmail.com', 'c'],
        4: ['2@gmail.com', 'd'],
        5: ['5@gmail.com', 'a'],
        6: ['6@gmail.com', 'b'],
        7: ['7@gmail.com', 'c'],
        8: ['8@gmail.com', 'd'],
        9: ['9@gmail.com', 'a'],
        10: ['10@gmail.com', 'b'],
        11: ['11@gmail.com', 'c'],
        12: ['12@gmail.com', 'd'],
        13: ['13@gmail.com', 'a']
    }

    company_list = []

    for keys in total_users:
        if total_users[keys][1] == company_id:
            company_list.append(total_users[keys])

    return company_list

def get_header(filename):
    pass