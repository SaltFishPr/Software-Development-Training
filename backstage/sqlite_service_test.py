from database.user import UserDB
from database.journal import JournalDB
from database.record import RecordDB

journal_list = []
data = {
    'journal_list': journal_list
}

results = JournalDB.get_year_by_name('science')
for temp in results:
    journal = dict()
    journal['name'] = 'science'
    journal['year'] = temp
    journal['stage'] = 'null'
    journal_list.append(journal)

print(journal_list)
