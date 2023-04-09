from loader import admins, admin_nspk_number


class Shift:
    _instance = None
    admins = {adm_id: number for adm_id, number in
              zip(admins, admin_nspk_number)}
    on_shift = []

    @classmethod
    def start(cls, admin_id):
        if not(admin_id in cls.on_shift):
            cls.on_shift.append(admin_id)
            #Возвращает True, если выод на смену удачен
            return True
        else:
            #Возвращает False, если неуадчен
            return False

    @classmethod
    def end(cls, admin_id):
        if admin_id in cls.on_shift:
            cls.on_shift.remove(admin_id)
            return True
        return False

    @classmethod
    def get_active(cls):
        return cls.on_shift

    @classmethod
    def get_active_number(cls):
        active_list = list()
        for i in range(len(cls.on_shift)):
            active_list.append(cls.admins[cls.on_shift[i]])
        return active_list
