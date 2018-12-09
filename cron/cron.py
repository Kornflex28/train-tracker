import sys
sys.path.append('..')

from database.Request import Request as dbRequest

import utils.credentials


for request in dbRequest.objects():
    print(request.origin.name)