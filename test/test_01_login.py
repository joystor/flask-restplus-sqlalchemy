import pytest, base64

def test_login_user(client, app):
    """Test the login proces, get client_secret and generate the oauth token"""
    
    user = "admin"
    pswd = "mypwdz"
    client_id = "WfR1rhmADab4QS11L7mx1dHH"
    
    #set cookie for autorization
    client.set_cookie('/', 'session', 'testing-flask-app')
    
    #Test login to get client_secret
    response = client.post(
        '/oauth/login', data={'username':'%s' % user,
              'password':'%s' % pswd,
              'client_id':'%s' % client_id })
    #Test if result code is correct
    assert response.status_code == 200
    #Test if token exist
    assert 'client_secret' in response.json
    print("  - client_secret: %s" % response.json['client_secret'])
    
    #Test get oauth token
    key = '{}:{}'.format(client_id, response.json['client_secret'])
    b64Val = base64.standard_b64encode(key.encode('utf-8'))
    print("  - Authorization Basic : %s" % b64Val)
    oauth_secret = 'Basic %s' % b64Val.decode('utf-8')
    response = client.post(
        '/oauth/token', 
        headers={
            'Authorization': oauth_secret
        },
        data={'username':'%s' % user,
              'password':'%s' % pswd,
              'grant_type':'password'
        })
    #Test if result code is correct
    assert response.status_code == 200
    #Test if token exist
    assert 'access_token' in response.json
    
    pytest.OAUTH_TOKEN = response.json['access_token']
    print("  - oAuth token: %s" % pytest.OAUTH_TOKEN)