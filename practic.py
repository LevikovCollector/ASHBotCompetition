from datetime import datetime

with open('log.txt', 'w') as log:
    log.writelines(datetime.today().strftime('%c'))