from loader import admins, admin_nspk_number

class Shift:
    def __init__(self):
        self.admins = {adm_id: number for adm_id, number in zip(admins, admin_nspk_number)}
        self.on_shift = list()

    def start(self, admin_id):
        if not(admin_id in self.on_shift):
            self.on_shift.append(admin_id)
            #Возвращает True, если выод на смену удачен 
            return True
        else:
            #Возвращает False, если неуадчен
            return False
        
    def get_active(self):
        return self.on_shift
        
    def get_active_number(self):
        active_list = list()
        for i in self.on_shift:
            active_list.append(self.admins[self.on_shift[i]])
        return active_list
