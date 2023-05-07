import datetime


def cvetobib(cve):
    cveyear = cve[4:8]
    today = datetime.date.today().isoformat()
    print('@online{{{0},\n  title = {{{0}}},\n  howpublished = "Available from MITRE, {{CVE-ID}} {0}.",\n  publisher = "MITRE",\n  year = {{{1}}},\n  url={{http://cve.mitre.org/cgi-bin/cvename.cgi?name={0}}},\n  urldate={{{2}}}\n}}'.format(cve, cveyear, today))
