import re
import HTMLParser
pars = HTMLParser.HTMLParser()

def html_to_text(data): # pragma: no cover
    # remove the newlines
    data = data.replace("\n", " ")
    data = data.replace("\r", " ")
  
    # replace consecutive spaces into a single one
    data = " ".join(data.split())  
  
    # get only the body content
    bodyPat = re.compile(r'<body[^<>]*?>(.*?)</body>', re.I)
    result = re.findall(bodyPat, data)
    data = result[0]
  
    # now remove the java script
    p = re.compile(r'<script[^<>]*?>.*?</script>')
    data = p.sub('', data)
  
    # remove the css styles
    p = re.compile(r'<style[^<>]*?>.*?</style>')
    data = p.sub('', data)
  
    # remove html comments
    p = re.compile(r'')
    data = p.sub('', data)
  
    # remove all the tags
    p = re.compile(r'<[^<]*?>')
    data = p.sub('', data)

    # special hacks for django error output 
   #p = re.compile(r'\\n')
   #data = p.sub("\n", data)
  
    data = pars.unescape(data)
    return data
