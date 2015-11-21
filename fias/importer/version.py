#coding: utf-8
from __future__ import unicode_literals, absolute_import

import datetime
from fias.models import Version

from suds.client import Client


def fetch_version_info(update_all=False):
    client = Client(url="http://fias.nalog.ru/WebServices/Public/DownloadService.asmx?WSDL")
    result = client.service.GetAllDownloadFileInfo()

    for item in result.DownloadFileInfo:
        try:
            ver = Version.objects.get(ver=item['VersionId'])
        except Version.DoesNotExist:
            ver = Version(**{
                'ver': item['VersionId'],
                'dumpdate': datetime.datetime.strptime(item['TextVersion'][-10:], "%d.%m.%Y").date(),
            })
        finally:
            if not ver.pk or update_all:
                setattr(ver, 'complete_xml_url', item['FiasCompleteXmlUrl'])
                setattr(ver, 'complete_dbf_url', item['FiasCompleteDbfUrl'])

                setattr(ver, 'delta_xml_url', item.get('FiasDeltaXmlUrl', None))
                setattr(ver, 'delta_dbf_url', item.get('FiasDeltaDbfUrl', None))

                ver.save()
