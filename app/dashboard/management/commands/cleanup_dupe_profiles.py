'''
    Copyright (C) 2017 Gitcoin Core

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

'''

from django.core.management.base import BaseCommand
from django.db.models import Count

from dashboard.models import Profile


def combine_profiles(p1, p2):
    # p2 is the delete profile, p1 is the save profile
    # switch if p2 has the user
    # TODO: refactor to use https://github.com/mighty-justice/django-super-deduper 
    # instead
    if p2.user:
        p1, p2 = p2, p1

    p1.github_access_token = p2.github_access_token if p2.github_access_token else p1.github_access_token
    p1.slack_token = p2.slack_token if p2.slack_token else p1.slack_token
    p1.slack_repos = p2.slack_repos if p2.slack_repos else p1.slack_repos
    p1.slack_channel = p2.slack_channel if p2.slack_channel else p1.slack_channel
    p1.email = p2.email if p2.email else p1.email
    p1.preferred_payout_address = p2.preferred_payout_address if p2.preferred_payout_address else p1.preferred_payout_address
    p1.max_tip_amount_usdt_per_tx = max(p1.max_tip_amount_usdt_per_tx, p2.max_tip_amount_usdt_per_tx)
    p1.max_tip_amount_usdt_per_week = max(p1.max_tip_amount_usdt_per_week, p2.max_tip_amount_usdt_per_week)
    p1.max_num_issues_start_work = max(p1.max_num_issues_start_work, p2.max_num_issues_start_work)
    p1.trust_profile = any([p1.trust_profile, p2.trust_profile])
    p1.hide_profile = any([p1.hide_profile, p2.hide_profile])
    p1.suppress_leaderboard = any([p1.suppress_leaderboard, p2.suppress_leaderboard])
    # tips, bounties, fulfillments, and interests , activities, actions
    for obj in p2.received_tips.all():
        obj.profile = p1
        obj.save()
    for obj in p2.sent_tips.all():
        obj.profile = p1
        obj.save()
    for obj in p2.bounties_funded.all():
        obj.profile = p1
        obj.save()
    for obj in p2.interested.all():
        obj.profile = p1
        obj.save()
    for obj in p2.fulfilled.all():
        obj.profile = p1
        obj.save()
    for obj in p2.activities.all():
        obj.profile = p1
        obj.save()
    for obj in p2.actions.all():
        obj.profile = p1
        obj.save()
    for obj in p2.token_approvals.all():
        obj.profile = p1
        obj.save()
    for obj in p2.votes.all():
        obj.profile = p1
        obj.save()
    p1.save()
    p2.delete()


class Command(BaseCommand):

    help = 'cleans up users who have duplicate profiles'

    def handle(self, *args, **options):

        dupes = Profile.objects.values('handle').annotate(Count('handle')).filter(handle__count__gt=1)

        for dupe in dupes:
            handle = dupe['handle']
            profiles = Profile.objects.filter(handle=handle)
            print(f"combining {profiles[0].pk} and {profiles[1].pk}")
            combine_profiles(profiles[0], profiles[1])
