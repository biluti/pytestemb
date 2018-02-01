# -*- coding: UTF-8 -*-




import pytestemb as test

vector = [  "предыстория",
            "الإنكليزية",
            u"предыстория",
            u"الإنكليزية",
            u"ascii",
            "ascii",
            u"\u0627\u0644\u0625\u0646\u0643\u0644\u064a\u0632\u064a\u0629"
            "\u0627\u0644\u0625\u0646\u0643\u0644\u064a\u0632\u064a\u0629"
            u"\xd8\xa7\xd9\x84\xd8\xa5\xd9\x86\xd9\x83\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd8\xa9",
            "\xd8\xa7\xd9\x84\xd8\xa5\xd9\x86\xd9\x83\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd8\xa9",
            "",
            u"",
            "\xC3",
            u"\xC3",
            """'353530392d31354133093065450100ea/fs/1/84o3q@ms4hoW`Xn0PaNDo5Hc8n@`FF4noAu4nnRd4`al54haon', u'ParentId': u'353530392d31354133093065450100ea/fs/1/88A@nIAo2Gh4`o@o8n@`RDa44cl8`@`nFooiutn`e', u'Type': u'Item', u'URI': u'http://192.168.4.1:57135/PulsarServerPlugin/i/MzUzNTMwMzkyZDMxMzU0MTMzMDkzMDY1NDUwMTAwZWEvZnMvMS84NG8zcUBtczRob1dgWG4wUGFORG81SGM4bkBgRkY0bm9BdTRublJkNGBhbDU0aGFvbg%3D%3D.mp3', [^] u'Title': u'01 - Assassin'""",
            ]



def test_trace():
    for v in vector:
        test.trace_trace({v:v})


if __name__ == "__main__":

    test.add_trace(["txt"])
    test.add_test_case(test_trace)


    test.run()













