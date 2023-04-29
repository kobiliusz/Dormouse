import abc, re, html


class AbstractMessageHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, message):
        pass


class LinkHandler(AbstractMessageHandler):
    url_re = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\." \
             "[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"

    def handle(self, message):
        links = set(re.findall(self.url_re, message))
        for link in links:
            message = message.replace(link, '<a href="{}">{}</a>'.format(link, link))
        return message


class EscapeHandler(AbstractMessageHandler):

    def handle(self, message):
        return html.escape(message)


class StripHandler(AbstractMessageHandler):

    def handle(self, message):
        return message.strip()


def get_list():

    return [
        StripHandler(),
        EscapeHandler(),
        LinkHandler()
    ]
