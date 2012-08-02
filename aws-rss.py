#!/usr/bin/python

"""
Simple python scriupt to walk Amazon AWS Status RSS feeds and report any new postings.
(can be used in cron to alert DevOps when a wide scale AWS outage is occuring)
"""

import pickle
import textwrap
import sys

try:
    import feedparser
except:
    # Most common install issue
    print 'ERROR: You need to install the python feedparser library.'
    sys.exit(2)

# List of URLs you're interested in.
# More can be found here: http://status.aws.amazon.com/
rssurls=[
    'http://status.aws.amazon.com/rss/cloudfront.rss',
    'http://status.aws.amazon.com/rss/ec2-us-east-1.rss',
    ]

for url in rssurls:
    # Parse data
    freshdata = feedparser.parse(url)

    # Create unique name for pickle file using title
    picklefile='aws-rss-%s.pkl' % freshdata.feed.title.replace(' ','_')
   
    # Try to load an older pickle file from a prevous run.
    try: 
        input = open(picklefile, 'rb')
        lastdata = pickle.load(input)
    except:
        lastdata=feedparser.parse(None)

    # Compare freshdata to lastdata:
    for entry in freshdata.entries:
        if entry not in lastdata.entries:
            # Print new entries
            print '-'*80
            print freshdata.feed.title
            print 'Date:', entry.published
            print 'Subject:', entry.title
            print ''
            print textwrap.fill(entry.summary,60)
            # FIXME: Consider emailing output instead of using CRON's email

    # Store freshdata to disk
    output = open(picklefile, 'wb')
    pickle.dump(freshdata, output)
    output.close()
