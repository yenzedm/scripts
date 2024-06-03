try {
    Zabbix.log(4, '[ Telegram webhook ] Started with params: ' + value);
    var result = {
            'tags': {
                'endpoint': 'telegram'
            }
        },
        params = JSON.parse(value),
        req = new HttpRequest(),
        resp;
        
    if (params.HTTPProxy) {
        req.setProxy(params.HTTPProxy);
    }
    req.addHeader('Content-Type: application/json');

    var url = 'https://api.telegram.org/bot' + params.token + '/sendMessage';    
    var data = JSON.stringify({"message_thread_id": params.threadid, "chat_id": params.to, "text": params.subject + '\n' + params.message});
    
    resp = req.post(url, data);
    
    if (req.getStatus() != 200) {
        throw 'Response code: ' + req.getStatus();
    }
    return 'OK';
}
catch (error) {
    Zabbix.log(4, '[ Telegram webhook ] Issue creation failed json : ' + JSON.stringify({"fields": fields}));
    Zabbix.log(3, '[ Telegram webhook ] issue creation failed : ' + error);
    throw 'Failed with error: ' + error;
}
