import json

content_types = []

types = [
    ('mp4', 'video'),
    ('mkv', 'video'),
    ('vob', 'video'),
    ('wmv', 'video'),
    ('ogg', 'video'),

    ('srt', 'video-attachment'),
    ('ssa', 'video-attachment'),

    ('gif', 'image'),
    ('jpeg', 'image'),
    ('jpg', 'image'),
    ('png', 'image'),

    ('m4a', 'audio'),
    ('mp3', 'audio'),
    ('wav', 'audio'),
    ('aif', 'audio'),
    ('midi', 'audio'),

    ('csv', 'document'),
    ('doc', 'document'),
    ('docx', 'document'),
    ('pptx', 'document'),
    ('rtf', 'document'),
    ('txt', 'document'),
    ('tif', 'document'),
    ('xlsx', 'document'),
    ('tex', 'document'),
    ('pdf', 'document'),

    ('fnt', 'document-attachment'),
    ('ttf', 'document-attachment'),
    ('xla', 'document-attachment'),
    ('xll', 'document-attachment'),

    ('html', 'program'),
    ('c', 'program'),
    ('py', 'program'),
    ('class', 'program'),
    ('php', 'program'),
    ('java', 'program'),
    ('cs', 'program'),
    ('sql', 'program'),
    ('xml', 'program'),
    ('js', 'program'),
    ('cpp', 'program'),
    ('h', 'program'),
    ('sh', 'program'),

    ('yml', 'program-attachment'),
    ('tmp', 'program-attachment'),
    ('log', 'program-attachment'),

    ('exe', 'executable'),
    ('apk', 'executable'),
    ('bat', 'executable'),
    ('jar', 'executable'),
    ('bin', 'executable'),

    ('zip', 'executable-attachment'),
    ('rar', 'executable-attachment'),
    ('tar', 'executable-attachment'),

    ('other', 'other-type'),
]

for pk,t in enumerate(types):
    d = {}
    d['model'] = 'content.ContentType'
    d['pk'] = pk
    d['fields'] = {}
    d['fields']['name'] = t[0]
    d['fields']['type'] = t[1]
    content_types.append(d)

with open("Content-type.json", "w") as outfile:
    json.dump(content_types, outfile,indent=1)