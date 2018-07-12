from __future__ import unicode_literals, division, absolute_import

import logging


from flexget import plugin
from flexget.entry import Entry
from flexget.event import event
from flexget.utils.cached_input import cached
from flexget.utils.requests import RequestException

log = logging.getLogger('anilist')


class AnilistAnime(object):
    """Creates an entry for each item in your kitsu.io list.
    Syntax:
    anilist:
      username: <value>
    """

    schema = {
        'type': 'object',
        'properties': {
            'username': {'type': 'string'}
        },
        'required': ['username'],
        'additionalProperties': False,
    }

    @cached('anilist', persist='2 hours')
    def on_task_input(self, task, config):
        entries = []
        query = '''
        query ($userName: String) {
            MediaListCollection(userName: $userName, type: ANIME) {
                lists {
                    name
                    status
                    entries {
                        ...mediaListEntry
                    }
                }
                user {
                    id
                    name
                }
            }
        }

        fragment mediaListEntry on MediaList {
            media {
                title {
                    romaji
                    english
                    native
                }
                status
                episodes
                siteUrl
            }
        }
        '''
        variables = {
            'userName': config['username']
        }

        url = 'https://graphql.anilist.co'

        try:
            response = task.requests.post(
                url, json={'query': query, 'variables': variables})
        except RequestException as e:
            error_message = 'Error fetching data from anilist for user: {user}'\
                .format(user=config['username'])
            if hasattr(e, 'response'):
                error_message += ' status: {status}'.format(
                    status=e.response.status_code)
            error_message += " - Is the username correct?"
            log.debug(error_message, exc_info=True)
            raise plugin.PluginError(error_message)

        json_data = response.json()

        if json_data:
            for media_list in json_data['data']['MediaListCollection']['lists']:
                log.debug("Anilist loaded: {list}".format(
                    list=media_list['name']))
                if media_list['status'] == 'COMPLETED':
                    log.debug("Skipping list for status COMPLETED.")
                    continue
                for series in media_list['entries']:
                    title_romaji = series['media']['title']['romaji']
                    title_english = series['media']['title']['english']
                    title_native = series['media']['title']['native']
                    log.debug("Anilist found series: {name}".format(
                        name=title_romaji))
                    alternate_names = []
                    if title_english != title_romaji\
                            and title_english is not None:
                        alternate_names.append(title_english)
                    if title_native != title_romaji\
                            and title_native is not None:
                        alternate_names.append(title_native)
                    entry = Entry(
                        title=title_romaji,
                        configure_series_alternate_name=alternate_names,
                        url=series['media']['siteUrl'],
                        anilist_status=series['media']['status']
                    )
                    if entry.isvalid():
                        entries.append(entry)

        return entries


@event('plugin.register')
def register_plugin():
    plugin.register(AnilistAnime, 'anilist', api_ver=2, interfaces=['task'])
