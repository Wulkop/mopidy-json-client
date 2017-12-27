import time

class formatter():
    class __formatter:
        def __init__(self):
            self.writerCallback = None

        def format_expand(self, value, indent=0, htchar='\t', lfchar='\n'):
            try:
                nlch = lfchar + htchar * (indent)
                if type(value) is dict:
                    items = [
                        nlch + str(key) + ': ' + self.format_expand(value[key], indent=indent + 1)
                        for key in value
                    ]
                    return '%10s' % (''.join(items))
                elif type(value) is list:
                    items = [
                        self.format_expand(item, indent=indent)
                        for item in value
                    ]
                    return '%s' % ((nlch + '+').join(items))
                elif type(value) is tuple:
                    items = [
                        nlch + self.format_expand(item, htchar, lfchar, indent=indent + 1)
                        for item in value
                    ]
                    return '(%s)' % (','.join(items))
                else:
                    try:
                        return str(value).replace(lfchar, nlch)
                    except:
                        return repr(value)
            except:
                return str(value).replace(lfchar, nlch)

        def format_nice(self, data, format=None):

            try:
                if data is None:
                    return '<None>'

                if format == 'raw':
                    return '%r %r' % (type(data), data)

                if format == 'expand':
                    return self.format_expand(data, indent=1)

                if format == 'tracklist':
                    tracklist = ['\n\t[%3d] %s' % (tl_track.get('tlid', 0),
                                                   self.format_nice(tl_track.get('track')))
                                 for tl_track in data]
                    return ''.join(tracklist)

                if format == 'time_position':
                    secs = data / 1000
                    minutes = secs // 60
                    hours = secs // 3600
                    return ('%02dm%02ds' % (minutes, secs % 60)) \
                        if (hours < 1) else '%dh%02dm%02ds' % ((hours, minutes % 60, secs % 60))

                if format == 'images':
                    str_uris = []
                    for uri, uri_images in data.items():
                        list_images = ['\n\t\t' + self.format_nice(image)
                                       for image in uri_images]
                        str_uris.append('\n\t(URI %s)' % uri + ''.join(list_images))
                    return ''.join(str_uris)

                if format == 'browse':
                    return ''.join(['\n\t' + self.format_nice(item) for item in data])

                if format == 'search':
                    return '\n'.join([self.format_nice(item) for item in data])

                if format == 'lookup':
                    list_info = []
                    for uri, info in data.iteritems():
                        list_info += ['\n[URI %s]' % uri]
                        list_info += ['\n\t' + self.format_nice(item) for item in info]

                    return ''.join(list_info)

                if format == 'history':
                    str_history = ['\n\t[%s] %s' % (time.strftime('%d-%b %H:%M:%S',
                                                                  time.localtime(item[0] / 1000)),
                                                    self.format_nice(item[1]))
                                   for item in data]
                    return ''.join(str_history)

                if format == 'volume':
                    return '%3d [%5s]' % (data,
                                          '#' * (data * 5 / 100))

                if hasattr(data, '__iter__') and '__model__' in data:

                    if data['__model__'] == 'Track':
                        title = data['name']
                        artist = data['artists'][0]['name'] \
                            if 'artists' in data else '<unknown>'
                        uri = data['uri']
                        return '%r - %r (%s)' % (artist, title, uri)

                    if data['__model__'] == 'Album':
                        return '%r [%s] (%s)' % (data.get('name'),
                                                 data.get('date', '--'),
                                                 data.get('uri'))

                    if data['__model__'] == 'Artist':
                        return '%(name)r (%(uri)s)' % data

                    if data['__model__'] == 'Image':
                        return '[%3dx%3d] %s' % (data.get('width', 0),
                                                 data.get('height', 0),
                                                 data.get('uri', ''))

                    if data['__model__'] == 'Ref':
                        return '[%(type)s] %(name)r (%(uri)s)' % data

                    if data['__model__'] == 'SearchResult':
                        list_items = ['\n[SEARCH URI (%s)]' % data.get('uri', '<None>')]
                        for section in ['tracks', 'albums', 'artists']:
                            if section in data:
                                list_items += ['\n\t [%s]' % section.upper()]
                                list_items += ['\n\t\t' + self.format_nice(item)
                                               for item in data[section]]
                        return ''.join(list_items)

                return self.format_expand(data, indent=1)

            except Exception as ex:
                return '%s\nEXCEPTION: %r' % (self.format_nice(data, format='raw'), ex)

        def print_nice(self, label, data, format=None):
            # Print label and formatted data
            resultstring = '%s%s' % (label, self.format_nice(data, format=format))
            print(resultstring)
            if self.writerCallback != None:
                self.writerCallback(resultstring)

        def set_writer_callback(self):
            self.writerCallback = callback
    instance = None
    def __init__(self):
        if not formatter.instance:
            formatter.instance = formatter.__formatter()
