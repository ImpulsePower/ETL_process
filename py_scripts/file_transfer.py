from os import rename
# Перемещение отработанных файлов
def file_transfer(X):
    rename('terminals_' + X + '.xlsx', 'archive/terminals_' + X + '.xlsx.backup')
    rename('transactions_' + X + '.txt', 'archive/transactions_' + X + '.txt.backup')
    rename('passport_blacklist_' + X + '.xlsx', 'archive/passport_blacklist_' + X + '.xlsx.backup')