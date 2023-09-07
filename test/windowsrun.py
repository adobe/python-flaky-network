import flakywindows as f

dic={
        'mode':'5',   
        'profile':'wi-fi',
        'switch_profile':'3g',
       'download':'15',
       'upload':'15',
       'jitter':'20',
       'drop':'20',
       'random':'100'
}

fn=f.FlakyWindows(p=dic.get('profile'))

if dic.get('mode')=='0':
    #will create outbound throttling
    fn.throttleOutbound(dic.get('upload'))

elif dic.get('mode')=='1':
    #will create inbound throttling
    fn.throttleInbound(dic.get('download'))    

elif dic.get('mode')=='2':
    #will create jitter 
    fn.jitter_new(dic.get('jitter'))

elif dic.get('mode')=='3':
    #will create packet loss
    fn.drop(dic.get('drop'))

elif dic.get('mode')=='4':
    #will allocate random inbound and outbound bandwidth
    fn.randomBandwidth(dic.get('random')) 

elif dic.get('mode')=='5':
    if __name__=="__main__":
    #will create real-life simulation
        fn.real(int(dic.get('download')),int(dic.get('upload')),int(dic.get('drop')),int(dic.get('jitter')))     

else:
    print('Wrong mode specified')    