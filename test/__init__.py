from PyQt5.QAxContainer import *
from config.errorCode import *
from PyQt5.QtCore import *



class Option(QAxWidget):
    def __init__(self):
        super().__init__()
        print("Option() class start.")

        ### eventloop 모음 ###
        self.login_event_loop = None
        self.get_call_option_price_loop = QEventLoop()
        ## 행사가 관련 변수

        self.stock_code_dict ={}
        ##요청 스크린 번호
        self.screen_my_info = "2000"

        ### 초기 셋팅 함수들 바로 실행 ###
        self.get_ocx_instance()
        self.event_slots()
        self.signal_login_commConnect()
        self.get_account_info()
        #self.detail_account_info()
        self.get_call_option_price()




    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)
        self.OnReceiveTrData.connect(self.trdata_slot)

    def signal_login_commConnect(self):
        self.dynamicCall("CommConnect()")

        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def login_slot(self, err_code):
        print(errors(err_code)[1])

        self.login_event_loop.exit()


    def get_account_info(self):
        account_list = self.dynamicCall('GetLoginInfo(QString)','ACCLIST') #계좌번호 가져오기
        account_num = account_list.split(';')[1]
        self.account_num = account_num

        print(account_num)
    # def detail_account_info(self, sPrevNext="0"):
    #     print("예수금 요청하는 부분")
    #     self.dynamicCall('SetInputValue(String, String)', "계좌번호", self.account_num)
    #     self.dynamicCall('SetInputValue(String, String)', "비밀번호", '0000')
    #     self.dynamicCall('SetInputValue(String, String)', "비밀번호입력매체구분", '00')
    #     self.dynamicCall('SetInputValue(String, String)', "조회구분", '1')
    #     self.dynamicCall("CommRqData(String, String, int, String)", "예수금상세현황요청", "opw00001", sPrevNext, self.screen_my_info)

    def get_call_option_price(self, sPrevNext= "0"):
        print("콜옵션행사가요청")
        self.dynamicCall('SetInputValue(String, String)',"만기년월", 202003)
        self.dynamicCall('CommRqData(String, String, int, String)',"콜옵션행사가요청"	,  "opt50004"	, sPrevNext	,  self.screen_my_info)

        self.get_call_option_price_loop.exec_()

    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):

        '''
        TR 요청을 받는 구역이다 슬롯이다  [OnReceiveTrData() 이벤트]
        :param sScrNo: 스크린 번호
        :param sRQName: 내가 요청했을때 지은 이름
        :param sTrCode: 요청 id , tr코드
        :param sRecordName: 사용안함
        :param sPrevNext: 다음 페이지가 있는지
        :return:
        '''

        #  [GetCommData() 함수]
        # if sRQName == "예수금상세현황요청":
        #     deposit = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode , sRQName, 0 , "예수금")
        #     print("예수금 %s" % int(deposit))
        #
        # def stop_screen_cancel(self, sScrNo=None):
        #     self.dynamicCall("DisconnectRealData(QString)", sScrNo)

        # if sRQName == "콜옵션행사가요청":
        #     stock_code = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode , sRQName, 0 , "종목코드")
        #     print("종목코드",stock_code.strip())
        #     if stock_code in self.stock_code_dict:
        #         print("pass")
        #         pass
        #     else:
        #         print("else")
        #         self.stock_code_dict[stock_code].update({"종목코드": stock_code})
        if sRQName == "콜옵션행사가요청":
            stock_code= self.dynamicCall("GetCommData(String, String, int, String)", sTrCode , sRQName, 0 , "종목코드")
            print("종목코드", stock_code.strip())

            exercise_price = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "행사가")
            print("행사가", type(exercise_price.strip()))

            rows = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)
            for i in range(rows):
                code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목코드")
                code1 = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "행사가")
                #print(type(code))
                print(i)
                print("종목코드",code.strip())
                print("행사가",code1.strip())
                print("======================")


            ##정보 딕셔너리에 업데이트 하기






            self.stop_screen_cancel(self.screen_my_info)
            self.get_call_option_price_loop.exit()



    def stop_screen_cancel(self, sScrNo=None):
            self.dynamicCall("DisconnectRealData(QString)", sScrNo)



