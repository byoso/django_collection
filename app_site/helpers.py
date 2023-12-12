import os

from django.conf import settings

SITEFILES_DIR = os.path.join(settings.MEDIA_ROOT, 'sitefiles')


item = {
    'name': '',
    'path': '',
    'type': '',
    'content': None,
}


def folder_to_dict(path):
    elems = os.listdir(path)
    folder_content = []
    for elem in elems:
        item = {}
        item['name'] = elem
        item['path'] = os.path.join(path, elem)
        if os.path.isdir(os.path.join(path, elem)):
            item['type'] = 'folder'
            item['url'] = None
            item['content'] = folder_to_dict(
                os.path.join(path, elem)
                )
        else:
            item['type'] = 'file'
            item['url'] = os.path.join(settings.MEDIA_URL, 'sitefiles', os.path.relpath(os.path.join(path, elem), SITEFILES_DIR))
            item['content'] = None
        folder_content.append(item)
        folder_content.sort(key=lambda x: x['name'])
        folder_content.sort(key=lambda x: x['type'])
    return folder_content
