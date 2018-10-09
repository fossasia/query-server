from bs4 import BeautifulSoup

from app.scrapers import Aol


def test_parse_response_for_none():
    html_text = """<div id="web">
        <style>#main .sc b,#main .dd b,#main .dd .cite{font-weight: bold;}</style>
        <ol class=" reg adultRegion">
            <li class="first last">
                <div class="dd zrp" style="margin-right:10px">
                    <div class="compText mb-15 fz-m fc-4th">
                        <p class="">We did not find results for: <strong><b>dasjhdabkdasdas</b></strong>. </p>
                    </div>
                    <div class="compText mb-8 fz-s fc-4th">
                        <p class="">Check spelling or type a new query. </p>
                    </div>
                </div>
            </li>
        </ol></div>"""  # noqa
    stub_soup = BeautifulSoup(html_text, 'html.parser')
    resp = Aol().parse_response(stub_soup)
    assert resp is None


def test_parse_response():
    html_text = """<ol class="mb-15 reg searchCenterMiddle">
        <li class="first">
            <div class="dd info fst lst SrLbl" style="margin-bottom:11px;">
                <div class="compTitle fc-4th">
                    <h5 class="title"><span style="color:#585962" class=" td-hu fc-4th ac-4th">Web results:</span></h5> </div>
            </div>
        </li>
        <li>
            <div class="dd algo algo-sr fst Sr" data-b4a="5bbc947cdb7b1">
                <div class="compTitle options-toggle">
                    <h3 class="title"><a class=" ac-algo fz-l ac-21th lh-24" href="//r.search.aol.com/_ylt=Awr9CKp8lLxbW24AcyJpCWVH;_ylu=X3oDMTByb2lvbXVuBGNvbG8DZ3ExBHBvcwMxBHZ0aWQDBHNlYwNzcg--/RV=2/RE=1539114236/RO=10/RU=https%3a%2f%2fgci16.fossasia.org%2f/RK=0/RS=1WaZ_NwVtC4M3F_ShfIKlIWFGMM-" referrerpolicy="origin" target="_blank" data-b4a="5bbc947cdb999">Google Code-In with <b>FOSSASIA</b> 2016/17</a></h3>
                    <div><span class=" fz-ms fw-m fc-12th wr-bw lh-17">gci16.<b>fossasia</b>.org</span></div>
                </div>
                <div class="compText aAbs">
                    <p class="lh-16">About <b>FOSSASIA</b>. <b>FOSSASIA</b> is an open source technology organization in Asia that aims to bring together an inspiring community across borders and ages to form a better future with Open Technologies and ICT. </p>
                </div>
            </div>
        </li>
    </ol>"""  # noqa
    stub_soup = BeautifulSoup(html_text, 'html.parser')
    resp = Aol().parse_response(stub_soup)
    assert resp is not None
