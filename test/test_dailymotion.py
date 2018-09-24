from app.scrapers import DailyMotion


def test_parse_response():
    json_data = '{"list":[{"id":"x6ilw2u",' \
                '"title":"Job Interviews - Stand Up Comedy by ' \
                'Piyush Sharma",' \
                '"channel":"fun",' \
                '"owner":"x24pst6"},{"id":"x65slib",' \
                '"title":"Beyhadh actor Piyush Sahdev(Samay) will ' \
                'soon enter' \
                ' colors Devanshi opposite Helly shah",' \
                '"channel":"fun","owner":"x21w079"},{"id":"x5fj9kg",' \
                '"title":"Deepika-Piyush Se Mulaqat - Dhhai Kilo Prem",' \
                '"channel":"fun","owner":"x1isdap"},{"id":"x59m108",' \
                '"title":"Sasural Simar Ka TOOT GAYA PIYUSH VAIDAHI KA' \
                ' RISHTA 26 January 2017 News",' \
                '"channel":"fun","owner":"x1wmonz"},' \
                '{"id":"x6aj8su","title":"Beyhadh actor Piyush Sahdev ' \
                'ARRESTED on Rape charges | FilmiBeat",' \
                '"channel":"fun","owner":"x1x1a21"},{"id":"x4eq3kp",' \
                '"title":"Funny Balloon Tricks By Piyush Seth",' \
                '"channel":"fun","owner":"x1swlum"},{"id":"x6cmk7x",' \
                '"title":"Beyhadh Actor Piyush Sahdev Finally REACTS On' \
                ' His Molestation Case",' \
                '"channel":"fun","owner":"x22ch35"},{"id":"x3i6xr3",' \
                '"title":"Revolver Rani Movie || I Am Brutal Video Song ' \
                '|| Kangana Ranaut, Piyush Mishra, Vir Das",' \
                '"channel":"fun","owner":"x1ocl9w"},{"id":"xhv1dj",' \
                '"title":"Birthday party of t v actor piyush sachdev"' \
                ',"channel":"fun","owner":"xmoljl"},' \
                '{"id":"x6647o3","title":"Piyush Mishra  Aarambh Hai' \
                ' Prachand (Live At Hindu College)",' \
                '"channel":"fun","owner":"x21w0ck"}]}'

    expected_resp = [{
        'link': 'https://www.dailymotion.com/video/x6ilw2u',
        'title': u'Job Interviews - Stand Up Comedy by Piyush Sharma'},
        {'link': 'https://www.dailymotion.com/video/x65slib',
         'title': u'Beyhadh actor Piyush Sahdev(Samay) will soon '
                  u'enter colors Devanshi opposite Helly shah'},
        {'link': 'https://www.dailymotion.com/video/x5fj9kg',
         'title': u'Deepika-Piyush Se Mulaqat - Dhhai Kilo Prem'},
        {'link': 'https://www.dailymotion.com/video/x59m108',
         'title': u'Sasural Simar Ka TOOT GAYA PIYUSH VAIDAHI KA'
                  u' RISHTA 26 January 2017 News'},
        {'link': 'https://www.dailymotion.com/video/x6aj8su',
         'title': u'Beyhadh actor Piyush Sahdev ARRESTED on '
                  u'Rape charges | FilmiBeat'},
        {'link': 'https://www.dailymotion.com/video/x4eq3kp',
         'title': u'Funny Balloon Tricks By Piyush Seth'},
        {'link': 'https://www.dailymotion.com/video/x6cmk7x',
         'title': u'Beyhadh Actor Piyush Sahdev Finally REACTS'
                  u' On His Molestation Case'},
        {'link': 'https://www.dailymotion.com/video/x3i6xr3',
         'title': u'Revolver Rani Movie || I Am Brutal Video'
                  u' Song || Kangana Ranaut, Piyush Mishra, Vir Das'},
        {'link': 'https://www.dailymotion.com/video/xhv1dj',
         'title': u'Birthday party of t v actor piyush sachdev'},
        {'link': 'https://www.dailymotion.com/video/x6647o3',
         'title': u'Piyush Mishra  Aarambh Hai Prachand '
                  u'(Live At Hindu College)'}]
    resp = DailyMotion().parse_response(json_data)
    assert resp == expected_resp
