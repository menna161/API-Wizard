import click
from urllib.parse import parse_qsl, urljoin, urlparse
import requests
from bs4 import BeautifulSoup


@click.command()
@click.argument('keyword', metavar='<keyword>')
def main(keyword):
    ' Use DAUM Dictionary via terminal '
    click.echo('Searching...')
    url = f'{DAUM_DICT_HOST}search.do?q={keyword}&dic={LANG}'
    response = requests.get(url)
    (meanings, wordid) = parse(response.text)
    detailed_url = f'https://dic.daum.net/word/view.do?wordid={wordid}'
    detailed_text = None
    click.echo(meanings)
    if ((meanings == 'No results found.') and (wordid == '')):
        return
    while True:
        value = click.prompt(click.style(COMMANDS, fg='white', bg='blue'))
        try:
            command = COMMAND_SET[value]
        except KeyError:
            click.echo("Sorry, I don't understand.")
            continue
        if (value != 'q'):
            if (value == 'e'):
                result = parse_example(example_url(wordid))
                click.echo(result)
            else:
                if (detailed_text is None):
                    detailed_text = requests.get(detailed_url).text
                result = parse_detail(detailed_text, wordid, command)
                click.secho(command, fg='green')
                click.echo(result)
        else:
            break
