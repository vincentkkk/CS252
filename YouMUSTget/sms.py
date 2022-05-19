from ronglian_sms_sdk import SmsSDK
import random;
 

accId = '8a216da8806f31ad0180d601fed91912'
accToken = 'b12c4fe037354fef88b104cbe199f2fc'
appId = '8a216da8806f31ad0180d60200011919'

def send_message():

    resultList=[]
    A=100000
    B=999999 
    COUNT=1
 
    resultList=random.sample(range(A,B+1),COUNT)
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    mobile = '13952576220'
    datas = (resultList, '1')
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)
    
send_message()


   