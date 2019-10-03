import os
import requests
import gzip
import shutil
from feedgen.feed import FeedGenerator

if not os.path.isdir('tmp'):
    os.mkdir('tmp')
if not os.path.isdir('feed'):
    os.mkdir('feed')

url = 'https://www.ettv.to/dumps/ettv_daily.txt.gz'
r = requests.get(url)

compressed_file = 'tmp/ettv_daily.txt.gz'
file = 'tmp/ettv_daily.txt'

print('Downloading {} to {}...'.format(url, compressed_file))
with open(compressed_file, 'wb') as gz:
    gz.write(r.content)
print('Done.')

print('Uncompressing {} to {}...'.format(compressed_file, file))

with gzip.open(compressed_file, 'rb') as gz:
    with open(file, 'wb') as f:
        shutil.copyfileobj(gz, f)
print('Done.')


with open(file) as f:
    content = f.readlines()

fg = FeedGenerator()
fg.title('ETTV Daily Dump')
fg.link(href='ettv.druz.fr/rss.xml', rel='self')
fg.description('ETTV daily dump')
fg.language('en')

entries = []
for line in content:
    l = line.rstrip('\n').split('|')
    if l[2] == 'TV':
        entries.append({'title': l[1], 'link': l[3]})
        fe = fg.add_entry()
        fe.id(l[0])
        fe.title(l[1])
        fe.link(href=l[3])

rssfeed = fg.rss_str()
fg.rss_file('feed/rss.xml')

