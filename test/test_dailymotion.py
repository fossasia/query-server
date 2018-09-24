from app.scrapers import DailyMotion


def test_parse_response():
    json_data = '{"list":[{"id":"x6ilw2u",' \
                '"title":"Job Interviews - Stand Up Comedy by ' \
                'Piyush Sharma",' \
                '"channel":"fun",' \
                '"owner":"x24pst6"}]}'

    expected_resp = [{
        'link': 'https://www.dailymotion.com/video/x6ilw2u',
        'title': u'Job Interviews - Stand Up Comedy by Piyush Sharma'}
       ]
    resp = DailyMotion().parse_response(json_data)
    assert resp == expected_resp
