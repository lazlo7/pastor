from pastor.paste.constants import BASE64_ALPHABET, SQIDS_ID_MIN_LENGTH
from sqids import sqids


sqids = sqids.Sqids(alphabet=BASE64_ALPHABET, min_length=SQIDS_ID_MIN_LENGTH)
