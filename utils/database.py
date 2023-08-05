import os
import deta


service = deta.Deta(os.getenv('COLLECTION_KEY'))
db = service.base(os.getenv('BASE_NAME'))
drive = service.drive(os.getenv('DRIVE_NAME'))
