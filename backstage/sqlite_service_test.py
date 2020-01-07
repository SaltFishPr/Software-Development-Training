from database.user import UserDB
from database.journal import JournalDB
from database.record import RecordDB

print(RecordDB.get_info_by_dict('Record', {}))
