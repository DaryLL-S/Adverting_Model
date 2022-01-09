import adjustment
import getinfo
import mykeyword
import model

if __name__ == '__main__':
    collection = getinfo.connect_mongo()
    getinfo.userinfo(collection)
    getinfo.merge_data()

    model.builtmodel()
    mykeyword.word()
    adjustment.final_adjustment()
