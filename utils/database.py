import os
import deta

deta_ = deta.Deta(os.getenv('COLLECTION_KEY'))
db = deta_.base('01PIXEL')
drive = deta_.drive('PixeL_@11223344')
