from ..services.auth_service import db

def get_menus():
    menus_ref = db.collection('menus')
    docs = menus_ref.stream()
    menus = []
    for doc in docs:
        menu_data = doc.to_dict()
        menu_data['id'] = doc.id
        menus.append(menu_data)
    return menus

def create_menu(data):
    menus_ref = db.collection('menus')
    doc_ref = menus_ref.add(data)
    return {'id': doc_ref[1].id, **data}

def update_menu(menu_id, data):
    menu_ref = db.collection('menus').document(menu_id)
    menu_ref.update(data)
    return {'id': menu_id, **data}

def delete_menu(menu_id):
    db.collection('menus').document(menu_id).delete()

def get_categories():
    cats_ref = db.collection('categories')
    docs = cats_ref.stream()
    categories = []
    for doc in docs:
        cat_data = doc.to_dict()
        cat_data['id'] = doc.id
        categories.append(cat_data)
    return categories

def create_category(data):
    cats_ref = db.collection('categories')
    doc_ref = cats_ref.add(data)
    return {'id': doc_ref[1].id, **data}

def delete_category(cat_id):
    db.collection('categories').document(cat_id).delete()