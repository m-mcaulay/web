# -*- coding: utf-8 -*-
"""Define the management command to generate EthOS hops.

Copyright (C) 2018 Gitcoin Core

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

from django.core.management.base import BaseCommand

from ethos.models import Hop, ShortCode, TwitterProfile
from ethos.utils import get_twitter_api
import time


class Command(BaseCommand):
    """Define the management command to generate Ethos reminder tweets."""

    help = 'sends a reminder'

    def add_arguments(self, parser):
        """Define the arguments for the command."""
        parser.add_argument('live', type=int)

    def handle(self, *args, **options):
        """Define the command handling to generate hops."""
        hops = Hop.objects.all()
        hop_users = [hop.twitter_profile.username for hop in hops if not hop.next_hop()]
        hop_users = set(hop_users)
        for hop_user in hop_users:
            tweet = f"@{hop_user} happy #ethereal day 2 -- Give your Ethos solid coin to someone great today (2x 'day 2' bonus today only)!\n\n(1 time reminder)"
            print(len(tweet))
            if options['live']:
                twitter_api = get_twitter_api()
                twitter_api.PostUpdate(tweet, media='https://gitcoin.co/ethos/graph.gif?key=optimize')
                time.sleep(10)
            print(hop_user)