from newsplease import NewsPlease

text = NewsPlease().from_url('https://www.w3schools.com/python/python_try_except.asp')
print(text.maintext)
