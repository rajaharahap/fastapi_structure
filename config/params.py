import os

rootWeb = os.path.dirname(os.path.realpath(__file__))
dir_split = str(rootWeb).split("/")
dir_ = '/'.join(x for x in dir_split[:-1])
loc = {
    "files_legal_opini": dir_ + "/files/legal_opini",
    "files_internal_kebijakan": dir_ + "/files/internal_kebijakan",
}


par = {
}