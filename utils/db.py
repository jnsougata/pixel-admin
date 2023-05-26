import os
import deta

d = deta.Deta(os.getenv('COLLECTION_KEY'))
db = d.base('01PIXEL')
drive = d.drive('PixeL_@11223344')
