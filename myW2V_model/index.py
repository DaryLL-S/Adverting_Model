import myW2V_model.myadjustment
import myW2V_model.getinfo
import myW2V_model.mykeyword
import myW2V_model.model


def main():
    collection = myW2V_model.getinfo.connect_mongo()
    myW2V_model.getinfo.userinfo(collection)
    myW2V_model.getinfo.merge_data()

    myW2V_model.model.builtmodel()
    myW2V_model.mykeyword.word()
    myW2V_model.myadjustment.final_adjustment()


if __name__ == '__main__':
    main()
