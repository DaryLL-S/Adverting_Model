import myadjustment
import getinfo
import mykeyword
import model


def main():
    collection = getinfo.connect_mongo()
    getinfo.userinfo(collection)
    getinfo.merge_data()

    model.builtmodel()
    mykeyword.word()
    myadjustment.final_adjustment()


if __name__ == '__main__':
    main()
