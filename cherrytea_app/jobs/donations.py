from cherrytea_app.models import DonationPlan, Donation


def gather_valid_plans():
    # plans should be fulfilled if:
    # - today is the day of week they're created for localized to
    # - the timezone of the user they're attached to, and they have
    # - not already been run this 'week'
    pass


def run():
    pass


if __name__ == '__main__':
    run()
