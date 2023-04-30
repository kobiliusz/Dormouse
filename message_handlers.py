import abc, re, html, emojis


class AbstractMessageHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, message):
        pass


class LinkHandler(AbstractMessageHandler):
    url_re = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\." \
             "[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"

    def handle(self, message):
        links = set(re.findall(self.url_re, message))
        for link in links:
            message = message.replace(link, '<a href="{}" target="_blank">{}</a>'.format(link, link))
        return message


class EscapeHandler(AbstractMessageHandler):

    def handle(self, message):
        return html.escape(message)


class StripHandler(AbstractMessageHandler):

    def handle(self, message):
        return message.strip()


class EmojiHandler(AbstractMessageHandler):

    def handle(self, message):
        for emoji_ascii in emojis.emoji_dict:
            message = re.sub(r'(?:^|\s)' + re.escape(emoji_ascii),
                             emojis.emoji_dict[emoji_ascii], message)
        return message


def get_list():

    return [
        StripHandler(),
        EmojiHandler(),
        EscapeHandler(),
        LinkHandler()
    ]
